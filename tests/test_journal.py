"""Journal: front matter, en/ko pairing, future-date refusal, sitemap rows, committed pages match the build."""
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO
import build_journal as bj

LANGS = bj.LANGS
POST = "---\ntitle: T\ndate: %s\ntime: %s\nsummary: S\ncopy_review: iris 2026-11-13\n---\nBody **bold** and `code`.\n\n## Head\n\n- one\n- two\n"


def make_root(date="2026-11-13", time="10:00", ko_time=None, langs=LANGS):
    d = Path(tempfile.mkdtemp())
    p = d / "content" / "journal" / "a-post"
    p.mkdir(parents=True)
    for l in langs:
        (p / ("%s.md" % l)).write_text(POST % (date, ko_time if (l == "ko" and ko_time) else time), encoding="utf-8")
    shutil.copy(REPO / "content" / "landing.json", d / "content" / "landing.json")
    return d


class JournalTest(unittest.TestCase):
    def root(self, **kw):
        d = make_root(**kw)
        self.addCleanup(shutil.rmtree, d, True)
        return d

    def test_builds_all_12_languages(self):
        pages = bj.render(self.root())
        want = set()
        for l in LANGS:
            base = "journal" if l == "en" else l + "/journal"
            want |= {base + "/index.html", base + "/a-post/index.html"}
        self.assertEqual(set(pages), want)
        self.assertIn("<strong>bold</strong>", pages["journal/a-post/index.html"])
        self.assertIn("<li>two</li>", pages["ko/journal/a-post/index.html"])

    def test_header_select_nav_and_footer_legal(self):
        for rel, h in bj.render(self.root()).items():
            header = h.split("</header>")[0]
            footer = h.split("<footer")[1]
            self.assertNotRegex(header, r'href="/(privacy|terms)/"', rel)
            self.assertEqual(len(re.findall(r'href="/(?:privacy|terms)/"', footer)), 2, rel)
            self.assertEqual(len(re.findall(r'href="/(?:privacy|terms)/"', h)), 2, rel)
            self.assertRegex(header, r'<label for="langsel">[^<]+</label><select id="langsel"')
            self.assertIn('aria-current="true"', header, rel)
            self.assertEqual(re.findall(r'<option value="[^"]*" lang="([^"]+)"', h), list(LANGS), rel)
            self.assertNotIn('class="langs"', h.split("</header>")[1], rel)

    def test_hreflang_canonical_jsonld(self):
        pages = bj.render(self.root())
        for l in LANGS:
            rel = ("journal" if l == "en" else l + "/journal") + "/a-post/index.html"
            h = pages[rel]
            self.assertEqual(re.findall(r'<link rel="alternate" hreflang="([^"]+)"', h), list(LANGS) + ["x-default"], rel)
            self.assertIn('hreflang="x-default" href="https://bottledmarbles.ipe.rest/journal/a-post/"', h)
            self.assertIn('<link rel="canonical" href="https://bottledmarbles.ipe.rest%s">' % bj.jpath(l, "a-post"), h)
            self.assertIn('"inLanguage": "%s"' % l, h)
            self.assertIn('<html lang="%s"' % l, h)

    def test_untranslated_post_en_fallback_card_and_partial_hreflang(self):
        d = self.root(langs=("en", "ko"))
        pages = bj.render(d)
        self.assertNotIn("ja/journal/a-post/index.html", pages)
        ja = pages["ja/journal/index.html"]
        self.assertIn('href="/journal/a-post/" hreflang="en" lang="en"', ja)
        self.assertEqual(re.findall(r'<link rel="alternate" hreflang="([^"]+)"', pages["journal/a-post/index.html"]).count("ja"), 0)
        self.assertIn('<option value="/ja/journal/" lang="ja">', pages["journal/a-post/index.html"])  # no post in ja -> journal index
        rows = "".join(bj.sitemap_rows(d))
        self.assertIn("/ko/journal/a-post/", rows)
        self.assertNotIn("/ja/journal/a-post/", rows)
        self.assertIn("/ja/journal/</loc>", rows)

    def test_copy_review_format(self):
        with self.assertRaises(SystemExit):
            bj.parse(POST.replace("iris 2026-11-13", "bob") % ("2026-11-13", "10:00"))

    def test_copy_review_date_optional(self):
        bj.parse(POST.replace("iris 2026-11-13", "iris") % ("2026-11-13", "10:00"))

    def test_future_date_refused(self):
        with self.assertRaises(SystemExit):
            bj.load(self.root(date="2099-01-01"))

    def test_en_ko_time_mismatch_refused(self):
        with self.assertRaises(SystemExit):
            bj.load(self.root(ko_time="11:00"))

    def test_missing_english_refused(self):
        d = self.root()
        (d / "content" / "journal" / "a-post" / "en.md").unlink()
        with self.assertRaises(SystemExit):
            bj.load(d)

    def test_stray_file_refused(self):
        d = self.root()
        (d / "content" / "journal" / "a-post" / "xx.md").write_text("x", encoding="utf-8")
        with self.assertRaises(SystemExit):
            bj.load(d)

    def test_bad_time_refused(self):
        with self.assertRaises(SystemExit):
            bj.parse(POST % ("2026-11-13", "25:61"))

    def test_sitemap_has_hreflang_pairs(self):
        rows = "".join(bj.sitemap_rows(self.root()))
        self.assertIn("/journal/a-post/", rows)
        self.assertIn("/ko/journal/a-post/", rows)
        self.assertIn("/tr/journal/a-post/", rows)
        self.assertEqual(rows.count("<url>"), 2 * len(LANGS))
        self.assertIn('hreflang="x-default"', rows)

    def test_committed_pages_match_build(self):
        for rel, text in bj.render(REPO).items():
            self.assertEqual((REPO / rel).read_text(encoding="utf-8"), text, rel)


if __name__ == "__main__":
    unittest.main()
