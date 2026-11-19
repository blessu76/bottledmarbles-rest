"""Journal feeds + visible publish time: Atom feeds exist per language, entry times carry +09:00, <time>/article:published_time agree, ALLOWED admits feeds."""
import importlib
import os
import shutil
import unittest
import xml.etree.ElementTree as ET

from helpers import REPO
import build_journal as bj
from test_journal import make_root

LANGS = bj.LANGS
ATOM = "{http://www.w3.org/2005/Atom}"


class JournalFeedTest(unittest.TestCase):
    def root(self, **kw):
        d = make_root(**kw)
        self.addCleanup(shutil.rmtree, d, True)
        return d

    def test_feed_paths(self):
        self.assertEqual(bj.feed_path("en"), "/journal/feed.xml")
        self.assertEqual(bj.feed_path("ko"), "/ko/journal/feed.xml")
        self.assertEqual(bj.feed_path("zh-Hant"), "/zh-Hant/journal/feed.xml")

    # publish_next's clone starts with no journal (test_publish seeds it empty) — committed-state checks run in the real repo only
    @unittest.skipIf(os.environ.get("BM_PUBLISHING"), "already inside a publish run")
    def test_committed_feeds_exist_for_12_languages_not_for_stubs(self):
        for l in LANGS:
            rel = bj.feed_path(l).strip("/")
            self.assertTrue((REPO / rel).is_file(), rel)
        for stub in ("pt", "zh", "ar", "hi", "ru"):
            self.assertFalse((REPO / stub / "journal" / "feed.xml").exists(), stub)

    def test_entry_times_are_kst_with_offset(self):
        root = self.root(date="2026-11-13", time="10:05")
        feed = ET.fromstring(bj.render(root)["journal/feed.xml"])
        entries = feed.findall(ATOM + "entry")
        self.assertEqual(len(entries), 1)
        e = entries[0]
        self.assertEqual(e.find(ATOM + "published").text, "2026-11-13T10:05:00+09:00")
        self.assertEqual(e.find(ATOM + "updated").text, "2026-11-13T10:05:00+09:00")
        self.assertEqual(feed.find(ATOM + "updated").text, "2026-11-13T10:05:00+09:00")
        self.assertEqual(e.find(ATOM + "title").text, "T")

    def test_feed_is_valid_atom_per_language(self):
        pages = bj.render(self.root())
        for l in LANGS:
            feed = ET.fromstring(pages[bj.feed_path(l).strip("/")])
            self.assertEqual(feed.tag, ATOM + "feed", l)
            self.assertEqual(feed.get("{http://www.w3.org/XML/1998/namespace}lang"), l)
            self.assertIsNotNone(feed.find(ATOM + "id"), l)

    @unittest.skipIf(os.environ.get("BM_PUBLISHING"), "already inside a publish run")
    def test_committed_feed_entries_all_have_offset_times(self):
        for l in LANGS:
            feed = ET.parse(REPO / bj.feed_path(l).strip("/")).getroot()
            for e in feed.findall(ATOM + "entry"):
                for tag in ("published", "updated"):
                    self.assertRegex(e.find(ATOM + tag).text, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00\+09:00$", l)

    def test_time_element_and_published_meta_match_datetime(self):
        pages = bj.render(self.root(date="2026-11-13", time="10:05"))
        post = pages["journal/a-post/index.html"]
        self.assertIn('<time datetime="2026-11-13T10:05:00+09:00">', post)
        self.assertIn('<meta property="article:published_time" content="2026-11-13T10:05:00+09:00">', post)
        self.assertIn('"datePublished": "2026-11-13T10:05:00+09:00"', post)
        self.assertIn("November 13, 2026 10:05 KST", post)
        index = pages["ko/journal/index.html"]
        self.assertIn('<time datetime="2026-11-13T10:05:00+09:00">2026년 11월 13일 10:05 KST</time>', index)

    def test_every_post_and_index_page_links_its_feed(self):
        pages = bj.render(self.root())
        for l in LANGS:
            href = 'type="application/atom+xml" title="'
            for rel in (("journal" if l == "en" else l + "/journal") + "/index.html",
                        (("journal" if l == "en" else l + "/journal") + "/a-post/index.html")):
                self.assertEqual(pages[rel].count(href), 1, rel)
                self.assertIn('href="https://bottledmarbles.ipe.rest%s"' % bj.feed_path(l), pages[rel], rel)

    def test_allowed_regex_admits_feeds_only_in_journal_dirs(self):
        pn = importlib.import_module("publish_next")
        for p in ("journal/feed.xml", "ko/journal/feed.xml", "pt-BR/journal/feed.xml", "zh-Hant/journal/feed.xml"):
            self.assertTrue(pn.ALLOWED.match(p), p)
        for p in ("feed.xml", "journal/feed.xml.bak", "ko/feed.xml", "xx/journal/feed.xml", "assets/feed.xml"):
            self.assertFalse(pn.ALLOWED.match(p), p)


if __name__ == "__main__":
    unittest.main()
