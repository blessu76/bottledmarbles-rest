#!/usr/bin/env python3
"""Publishes the next queued journal post — stdlib only (Python 3.9+). Called by ops/gate_publish.py, never by hand on a schedule.

Runs inside the dedicated publish clone (cwd or --repo, default ~/.ipe/bottledmarbles-publish/repo), never the working checkout.
  1. lock · git pull --ff-only
  2. take the first folder of the queue (~/.ipe/queue/bottledmarbles/<NN-slug>/{en,ko}.md), slug = name without the "NN-" prefix
  3. stamp date/time = the real KST moment now (never back-dated), copy into content/journal/<slug>/
  4. build journal + landing (sitemap) · scripts/check.sh must be green · commit only the allowed paths · push
  5. queue folder -> queue/.published/ ; <3 posts left -> low-stock warning on stdout
Any failure rolls the clone back (reset --hard + clean of the allowed paths) and leaves the queue untouched.
Exit: 0 published · 3 queue empty · 1 failure.  --dry-run: stop after the build/check, roll back, change nothing.
"""
import argparse
import datetime as dt
import fcntl
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

KST = dt.timezone(dt.timedelta(hours=9))
HOME = Path(os.path.expanduser("~"))
QUEUE = Path(os.environ.get("BM_QUEUE_DIR", str(HOME / ".ipe" / "queue" / "bottledmarbles")))
LOW_STOCK = 3
ALLOWED = re.compile(r"^(content/journal/[a-z0-9-]+/(en|ko)\.md|journal/.*index\.html|ko/journal/.*index\.html|sitemap\.xml)$")
ROOM = ["--trailer", "Publisher: scripts/publish_next.py"]


def sh(args, cwd, check=True):
    r = subprocess.run(args, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    if check and r.returncode:
        raise RuntimeError("%s -> %d\n%s" % (" ".join(args), r.returncode, r.stdout[-1500:]))
    return r.stdout


def stamp(text, date, time):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise RuntimeError("queue post has no front matter")
    lines = [l for l in m.group(1).split("\n") if l.split(":", 1)[0].strip() not in ("date", "time")]
    lines += ["date: %s" % date, "time: %s" % time]
    return "---\n%s\n---\n%s" % ("\n".join(lines), m.group(2))


def next_post():
    dirs = sorted(d for d in QUEUE.iterdir() if d.is_dir() and not d.name.startswith(".")) if QUEUE.is_dir() else []
    return dirs


def rollback(repo):
    sh(["git", "reset", "--hard", "HEAD"], repo, check=False)
    sh(["git", "clean", "-fdq", "--", "content/journal", "journal", "ko/journal"], repo, check=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=os.environ.get("BM_PUBLISH_DIR", str(HOME / ".ipe" / "bottledmarbles-publish" / "repo")))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true", help="tests")
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    QUEUE.mkdir(parents=True, exist_ok=True)
    lock = open(str(QUEUE / ".lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("publish_next: another run holds the lock")
        return 1
    dirs = next_post()
    if not dirs:
        print("publish_next: queue empty — write more posts")
        return 3
    src = dirs[0]
    slug = re.sub(r"^\d+-", "", src.name)
    now = dt.datetime.now(KST)
    date, time = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
    try:
        if not a.no_push:
            sh(["git", "pull", "--ff-only"], repo)
        if (repo / "content" / "journal" / slug).exists():
            raise RuntimeError("slug %s already published" % slug)
        dst = repo / "content" / "journal" / slug
        dst.mkdir(parents=True)
        for l in ("en", "ko"):
            f = src / ("%s.md" % l)
            if not f.is_file():
                raise RuntimeError("%s/%s.md missing" % (src.name, l))
            (dst / ("%s.md" % l)).write_text(stamp(f.read_text(encoding="utf-8"), date, time), encoding="utf-8")
        sh([sys.executable, "scripts/build_journal.py"], repo)
        sh([sys.executable, "scripts/build_landing.py"], repo)
        os.environ["BM_PUBLISHING"] = "1"  # tests/test_publish.py skips itself inside this run (no recursion)
        sh(["bash", "scripts/check.sh"], repo)
        sh(["git", "add", "-A"], repo)
        staged = [p for p in sh(["git", "diff", "--cached", "--name-only"], repo).split("\n") if p]
        bad = [p for p in staged if not ALLOWED.match(p)]
        if bad:
            raise RuntimeError("paths outside the allowed set: %s" % bad)
        if a.dry_run:
            print("publish_next: dry run OK (%s, %d files)" % (slug, len(staged)))
            rollback(repo)
            return 0
        title = re.search(r"^title:\s*(.*)$", (dst / "en.md").read_text(encoding="utf-8"), re.M).group(1)
        sh(["git", "commit", "-m", "journal: %s (%s %s KST)" % (title, date, time)] + ROOM, repo)
        if not a.no_push:
            sh(["git", "push", "origin", "HEAD"], repo)
    except Exception as e:  # noqa: BLE001
        print("publish_next: FAILED — %s" % e, file=sys.stderr)
        rollback(repo)
        return 1
    done = QUEUE / ".published"
    done.mkdir(exist_ok=True)
    shutil.move(str(src), str(done / ("%s-%s" % (date, src.name))))
    left = len(dirs) - 1
    print("publish_next: published %s at %s %s KST; %d left in queue" % (slug, date, time, left))
    if left < LOW_STOCK:
        print("publish_next: LOW STOCK — only %d queued (want >= %d)" % (left, LOW_STOCK))
    return 0


if __name__ == "__main__":
    sys.exit(main())
