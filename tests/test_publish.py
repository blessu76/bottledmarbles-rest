"""scripts/publish_next.py end to end against a local bare remote (no network, no real queue)."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO

POST = "---\ntitle: %s\nsummary: S\ndate: 2026-11-14\ntime: 00:00\n---\nBody.\n"


def git(cwd, *a):
    return subprocess.check_output(["git", "-c", "user.name=t", "-c", "user.email=t@t"] + list(a), cwd=str(cwd), universal_newlines=True)


@unittest.skipIf(os.environ.get("BM_PUBLISHING"), "already inside a publish run")
class PublishTest(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)
        seed = self.d / "seed"
        shutil.copytree(str(REPO), str(seed), ignore=shutil.ignore_patterns(".git", "__pycache__"))
        shutil.rmtree(str(seed / "content" / "journal"), True)       # start with no posts, then publish from the queue
        shutil.rmtree(str(seed / "journal"), True)
        shutil.rmtree(str(seed / "ko" / "journal"), True)
        git(seed, "init", "-q", "-b", "main")
        git(seed, "add", "-A")
        git(seed, "commit", "-qm", "seed")
        subprocess.check_call(["git", "clone", "-q", "--bare", str(seed), str(self.d / "remote.git")])
        subprocess.check_call(["git", "clone", "-q", str(self.d / "remote.git"), str(self.d / "clone")])
        self.queue = self.d / "queue"
        for n, slug in (("02", "first-post"), ("03", "second-post")):
            p = self.queue / ("%s-%s" % (n, slug))
            p.mkdir(parents=True)
            for l in ("en", "ko"):
                (p / ("%s.md" % l)).write_text(POST % slug, encoding="utf-8")
        self.env = dict(os.environ, BM_QUEUE_DIR=str(self.queue))

    def run_pub(self, *extra):
        return subprocess.run([sys.executable, str(REPO / "scripts" / "publish_next.py"), "--repo", str(self.d / "clone")] + list(extra),
                              env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def test_publishes_one_stamps_now_pushes_and_dequeues(self):
        r = self.run_pub()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("LOW STOCK", r.stdout)
        self.assertTrue((self.d / "clone" / "journal" / "first-post" / "index.html").is_file())
        self.assertNotIn("00:00", (self.d / "clone" / "content" / "journal" / "first-post" / "en.md").read_text())
        self.assertIn("journal: first-post", git(self.d / "remote.git", "log", "-1", "--format=%s", "main"))
        self.assertFalse((self.queue / "02-first-post").exists())
        self.assertTrue((self.queue / "03-second-post").exists())
        self.assertEqual(len(list((self.queue / ".published").iterdir())), 1)

    def test_dry_run_changes_nothing(self):
        r = self.run_pub("--dry-run")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(git(self.d / "clone", "status", "--porcelain").strip(), "")
        self.assertTrue((self.queue / "02-first-post").exists())

    def test_empty_queue_exits_3(self):
        shutil.rmtree(str(self.queue))
        self.assertEqual(self.run_pub().returncode, 3)

    def test_broken_post_rolls_back_and_keeps_queue(self):
        (self.queue / "02-first-post" / "ko.md").unlink()
        r = self.run_pub()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertEqual(git(self.d / "clone", "status", "--porcelain").strip(), "")
        self.assertTrue((self.queue / "02-first-post").exists())


if __name__ == "__main__":
    unittest.main()
