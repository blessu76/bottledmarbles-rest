"""Journal: front matter, en/ko pairing, future-date refusal, sitemap rows, committed pages match the build."""
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
import build_journal as bj

POST = "---\ntitle: T\ndate: %s\ntime: %s\nsummary: S\n---\nBody **bold** and `code`.\n\n## Head\n\n- one\n- two\n"


def make_root(date="2026-11-13", time="10:00", ko_time=None):
    d = Path(tempfile.mkdtemp())
    p = d / "content" / "journal" / "a-post"
    p.mkdir(parents=True)
    (p / "en.md").write_text(POST % (date, time), encoding="utf-8")
    (p / "ko.md").write_text(POST % (date, ko_time or time), encoding="utf-8")
    return d


class JournalTest(unittest.TestCase):
    def root(self, **kw):
        d = make_root(**kw)
        self.addCleanup(shutil.rmtree, d, True)
        return d

    def test_builds_both_languages(self):
        pages = bj.render(self.root())
        self.assertEqual(sorted(pages), ["journal/a-post/index.html", "journal/index.html", "ko/journal/a-post/index.html", "ko/journal/index.html"])
        self.assertIn("<strong>bold</strong>", pages["journal/a-post/index.html"])
        self.assertIn("<li>two</li>", pages["ko/journal/a-post/index.html"])

    def test_future_date_refused(self):
        with self.assertRaises(SystemExit):
            bj.load(self.root(date="2099-01-01"))

    def test_en_ko_time_mismatch_refused(self):
        with self.assertRaises(SystemExit):
            bj.load(self.root(ko_time="11:00"))

    def test_missing_language_refused(self):
        d = self.root()
        (d / "content" / "journal" / "a-post" / "ko.md").unlink()
        with self.assertRaises(SystemExit):
            bj.load(d)

    def test_bad_time_refused(self):
        with self.assertRaises(SystemExit):
            bj.parse(POST % ("2026-11-13", "25:61"))

    def test_sitemap_has_hreflang_pairs(self):
        rows = "".join(bj.sitemap_rows(self.root()))
        self.assertIn("/journal/a-post/", rows)
        self.assertIn("/ko/journal/a-post/", rows)
        self.assertIn('hreflang="x-default"', rows)

    def test_committed_pages_match_build(self):
        for rel, text in bj.render(REPO).items():
            self.assertEqual((REPO / rel).read_text(encoding="utf-8"), text, rel)


if __name__ == "__main__":
    unittest.main()
