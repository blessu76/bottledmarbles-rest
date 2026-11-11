#!/usr/bin/env python3
"""Release-note gate for TestFlight builds — stdlib only. Exit 0 = ready, exit 1 = something is missing.

  python3 scripts/check_release.py --build 2          # build 2 has a complete entry in content/releases.json
  python3 scripts/check_release.py --build 2 --latest # ... and build 2 is also the newest entry (app = TF = notes)
  python3 scripts/check_release.py --all              # every entry is complete

The app repo's (foundry-f029) deploy_ios.sh calls this script (from the site repo, no --root) before every
TestFlight upload, so a build can no longer go out without its release note (Davy 11-07: app version =
TF build = release note, no bypass). The in-app release notes are the source of truth for what testers
read; content/releases.json is this site's data copy of the same notes — there is no release page here yet.

For an entry whose `build` is N it checks:
  1. exactly one entry with that build number;
  2. version is set and id is "<version>-<build>"; a "testflight" status carries a date;
  3. notes are filled in for every language in games.json (en ko) — non-empty lists of non-empty strings.
--latest additionally requires no entry with a higher build number (a note for a newer build means the app is behind).
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def parse_build(raw):
    """'2' or '1.0.0+2' -> '2'; None if it is neither."""
    m = re.match(r"^(?:\d+(?:\.\d+)*\+)?(\d+)$", str(raw).strip())
    return str(int(m.group(1))) if m else None


def langs(root):
    """Languages the site publishes — games.json is the single source of truth."""
    try:
        g = json.loads((Path(root) / "games.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise SystemExit("check_release: cannot read games.json: %s" % ex)
    ls = tuple(g.get("langs", ()))
    if not ls:
        raise SystemExit('check_release: games.json has no "langs"')
    return ls


def load_releases(root):
    """-> (entries, problems)"""
    f = Path(root) / "content" / "releases.json"
    if not f.is_file():
        return [], ["content/releases.json: missing"]
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as ex:
        return [], ["content/releases.json: %s" % ex]
    rel = data.get("releases")
    if not isinstance(rel, list):
        return [], ['content/releases.json: top-level "releases" must be a list']
    errs, entries = [], []
    for i, e in enumerate(rel):
        if not isinstance(e, dict) or not str(e.get("build", "")).strip():
            errs.append('content/releases.json: entry %d needs a "build"' % i)
        else:
            entries.append(e)
    return entries, errs


def check_entry(e, n, ls):
    """-> problems for one entry (build n)."""
    errs = []
    if not e.get("version"):
        errs.append("build %s: version missing" % n)
    elif e.get("id") != "%s-%s" % (e["version"], n):
        errs.append("build %s: id %r should be %r" % (n, e.get("id"), "%s-%s" % (e["version"], n)))
    if e.get("status") == "testflight" and not e.get("date"):
        errs.append("build %s: status testflight needs a date" % n)
    notes = e.get("notes") if isinstance(e.get("notes"), dict) else {}
    missing = []
    for lang in ls:
        items = notes.get(lang)
        if not isinstance(items, list) or not items or not all(isinstance(x, str) and x.strip() for x in items):
            missing.append("notes.%s" % lang)
    if missing:
        errs.append("build %s: missing or empty %s" % (n, ", ".join(missing)))
    return errs


def check(root, build, latest=False):
    """-> problems (empty = the note for build is complete)."""
    n = parse_build(build)
    if n is None:
        return ["--build must be a build number such as 2 or 1.0.0+2, got %r" % build]
    ls = langs(root)
    entries, errs = load_releases(root)
    hits = [e for e in entries if str(e.get("build", "")) == n]
    if not hits:
        return errs + ["build %s: no entry in content/releases.json (add one with notes for %s)" % (n, " + ".join(ls))]
    if len(hits) > 1:
        errs.append("build %s: %d entries in content/releases.json, expected one" % (n, len(hits)))
    errs += check_entry(hits[0], n, ls)
    if latest:
        newer = sorted({str(x["build"]) for x in entries
                        if str(x.get("build", "")).isdigit() and int(x["build"]) > int(n)}, key=int)
        if newer:
            errs.append("build %s: not the newest note — content/releases.json already has build %s" % (n, ", ".join(newer)))
    return errs


def check_all(root):
    """-> problems (empty = there is at least one entry and every entry is complete)."""
    ls = langs(root)
    entries, errs = load_releases(root)
    if not entries and not errs:
        return ["content/releases.json: no entries"]
    by_build = {}
    for e in entries:
        by_build.setdefault(str(e.get("build", "")), []).append(e)
    for n, es in by_build.items():
        if len(es) > 1:
            errs.append("build %s: %d entries in content/releases.json, expected one" % (n, len(es)))
        else:
            errs += check_entry(es[0], n, ls)
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check that the TestFlight release note(s) in content/releases.json are complete.")
    ap.add_argument("--build", help="build number, e.g. 2 or 1.0.0+2")
    ap.add_argument("--all", action="store_true", help="check that every entry is complete")
    ap.add_argument("--latest", action="store_true", help="also require this build to be the newest entry in releases.json")
    ap.add_argument("--root", default=str(HERE.parent), help="site repo root (default: this repo)")
    a = ap.parse_args(argv)
    if bool(a.build) == a.all:
        ap.error("use exactly one of --build N or --all")
    errs = check_all(a.root) if a.all else check(a.root, a.build, latest=a.latest)
    if errs:
        print("release notes NOT ready:")
        for x in errs:
            print("  - " + x)
        return 1
    print("release notes OK (%s)" % ("all entries" if a.all else "build %s" % parse_build(a.build)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
