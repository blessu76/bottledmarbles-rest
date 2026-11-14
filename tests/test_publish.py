"""scripts/publish_next.py end to end against a local bare remote (no network, no real queue)."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO

LANGS = ("en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr")
POST = "---\ntitle: %s\nsummary: S\ndate: 2026-11-14\ntime: 00:00\ncopy_review: iris 2026-11-14\n---\nBody.\n"


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
        for l in LANGS[1:]:
            shutil.rmtree(str(seed / l / "journal"), True)
        git(seed, "init", "-q", "-b", "main")
        git(seed, "add", "-A")
        git(seed, "commit", "-qm", "seed")
        subprocess.check_call(["git", "clone", "-q", "--bare", str(seed), str(self.d / "remote.git")])
        subprocess.check_call(["git", "clone", "-q", str(self.d / "remote.git"), str(self.d / "clone")])
        self.queue = self.d / "queue"
        for n, slug in (("02", "first-post"), ("03", "second-post")):
            p = self.queue / ("%s-%s" % (n, slug))
            p.mkdir(parents=True)
            for l in LANGS:
                (p / ("%s.md" % l)).write_text(POST % slug, encoding="utf-8")
        self.env = dict(os.environ, BM_QUEUE_DIR=str(self.queue))

    def run_pub(self, *extra):
        return subprocess.run([sys.executable, str(REPO / "scripts" / "publish_next.py"), "--repo", str(self.d / "clone")] + list(extra),
                              env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def test_publishes_one_stamps_now_pushes_and_dequeues(self):
        r = self.run_pub()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("LOW STOCK", r.stdout)
        for l in LANGS:
            page = self.d / "clone" / ("journal" if l == "en" else l + "/journal") / "first-post" / "index.html"
            self.assertTrue(page.is_file(), l)
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

    def assert_blocked(self, r):
        self.assertEqual(r.returncode, 4, r.stdout)
        self.assertIn("WARNING", r.stdout)
        self.assertEqual(git(self.d / "clone", "status", "--porcelain").strip(), "")
        self.assertTrue((self.queue / "02-first-post").exists())
        self.assertTrue((self.queue / "03-second-post").exists())       # never skips ahead to the next post
        self.assertFalse((self.d / "clone" / "content" / "journal" / "second-post").exists())

    def test_missing_language_skips_with_warning(self):
        (self.queue / "02-first-post" / "tr.md").unlink()
        r = self.run_pub()
        self.assert_blocked(r)
        self.assertIn("tr.md missing", r.stdout)

    def test_missing_copy_review_skips_with_warning(self):
        f = self.queue / "02-first-post" / "ja.md"
        f.write_text(f.read_text(encoding="utf-8").replace("copy_review: iris 2026-11-14\n", ""), encoding="utf-8")
        r = self.run_pub()
        self.assert_blocked(r)
        self.assertIn("ja.md has no", r.stdout)

    def test_en_ko_originals_need_no_copy_review_and_date_is_optional(self):
        d = self.queue / "02-first-post"
        for l in LANGS:
            f = d / ("%s.md" % l)
            t = f.read_text(encoding="utf-8").replace("copy_review: iris 2026-11-14\n", "copy_review: iris\n" if l not in ("en", "ko") else "")
            f.write_text(t, encoding="utf-8")
        import importlib
        sys.path.insert(0, str(REPO / "scripts"))
        pn = importlib.import_module("publish_next")
        self.assertEqual(pn.readiness(d), [])

    def test_allowed_regex_covers_12_languages_only(self):
        import importlib
        sys.path.insert(0, str(REPO / "scripts"))
        pn = importlib.import_module("publish_next")
        for l in LANGS:
            self.assertTrue(pn.ALLOWED.match("content/journal/a-b/%s.md" % l), l)
        for l in LANGS[1:]:
            self.assertTrue(pn.ALLOWED.match("%s/journal/a-b/index.html" % l), l)
        self.assertFalse(pn.ALLOWED.match("content/journal/a-b/xx.md"))
        self.assertFalse(pn.ALLOWED.match("assets/landing.js"))


if __name__ == "__main__":
    unittest.main()
