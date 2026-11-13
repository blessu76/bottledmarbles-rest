"""Landing pages: 12 languages, exact tags, hreflang set, picker, and the committed files match the build."""
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO

import build_landing as bl  # noqa: E402

LANGS = ("en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr")
SUPPORTED = LANGS


def page_lang(rel):
    return "en" if rel == "index.html" else rel.split("/")[0]


class Landing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = bl.render(REPO)

    def test_twelve_pages_with_exact_tags(self):
        self.assertEqual({page_lang(r) for r in self.pages if r.endswith("index.html")}, set(LANGS))
        for rel, h in self.pages.items():
            if not rel.endswith("index.html"):
                continue
            lang = page_lang(rel)
            self.assertIn('<html lang="%s" data-lang="%s">' % (lang, lang), h, rel)

    def test_hreflang_has_every_language_and_x_default(self):
        for rel, h in self.pages.items():
            if not rel.endswith("index.html"):
                continue
            got = re.findall(r'rel="alternate" hreflang="([^"]+)"', h)
            self.assertEqual(sorted(got), sorted(set(LANGS) | {"x-default"}), rel)
            for l in LANGS:
                self.assertIn('rel="alternate" hreflang="%s"' % l, h, rel)
            self.assertIn('hreflang="x-default" href="https://bottledmarbles.ipe.rest/"', h, rel)

    def test_no_retired_or_wrong_tags(self):
        blob = "".join(self.pages.values())
        for bad in ("zh-TW", "zh-HK", "zh-Hans", 'hreflang="zh"', 'hreflang="pt"', 'lang="zh"', 'lang="pt"',
                    'hreflang="ru"', 'hreflang="ar"', 'hreflang="hi"'):
            self.assertNotIn(bad, blob, bad)

    def test_picker_is_a_labelled_select_in_fixed_order(self):
        for rel, h in self.pages.items():
            if not rel.endswith("index.html"):
                continue
            lang = page_lang(rel)
            sel = re.search(r'<select id="langsel".*?</select>', h, re.S).group(0)
            self.assertRegex(h, r'<label for="langsel">[^<]+</label>', rel)
            self.assertEqual(re.findall(r'<option value="[^"]*" lang="([^"]+)"', sel), list(LANGS), rel)
            self.assertEqual(re.findall(r'lang="([^"]+)" selected', sel), [lang], rel)
            self.assertIn("<noscript>", h, rel)
            self.assertEqual(len(re.findall(r"<noscript>.*?</noscript>", h, re.S)[0].split("<a ")) - 1, len(LANGS), rel)

    def test_legal_links_only_in_footer(self):
        for rel, h in self.pages.items():
            if not rel.endswith("index.html"):
                continue
            header = re.search(r"<header.*?</header>", h, re.S).group(0)
            footer = re.search(r"<footer.*?</footer>", h, re.S).group(0)
            self.assertNotRegex(header, r'href="/(privacy|terms)/"', rel)
            self.assertEqual(len(re.findall(r'href="/(?:privacy|terms)/"', footer)), 2, rel)
            self.assertEqual(len(re.findall(r'href="/(?:privacy|terms)/"', h)), 2, rel)

    def test_assets_are_cache_busted(self):
        for rel, h in self.pages.items():
            if rel.endswith("index.html"):
                self.assertRegex(h, r'/assets/landing\.css\?v=\d+[a-z]?"', rel)
                self.assertRegex(h, r'/assets/landing\.js\?v=\d+[a-z]?"', rel)

    def test_sitemap_lists_every_page(self):
        sm = self.pages["sitemap.xml"]
        # 12 landing pages + the journal rows (journal tests cover those)
        self.assertGreaterEqual(sm.count("<url>"), len(LANGS))
        self.assertEqual(sm.count('hreflang="x-default"'), sm.count("<url>"))
        for l in LANGS:
            self.assertIn("<loc>https://bottledmarbles.ipe.rest/%s</loc>" % ("" if l == "en" else l + "/"), sm)

    def test_committed_files_match_build(self):
        for rel, text in self.pages.items():
            self.assertEqual((REPO / rel).read_text(encoding="utf-8"), text, rel)

    def test_resolve_matches_kit_rules(self):
        cases = {
            "zh-TW": "zh-Hant", "zh-HK": "zh-Hant", "zh-MO": "zh-Hant", "zh-Hant-TW": "zh-Hant",
            "zh-CN": "en", "zh-Hans": "en", "zh": "en", "zh-SG": "en",
            "pt": "pt-BR", "pt-PT": "pt-BR", "es-419": "es", "es-MX": "es",
            "in": "id", "id-ID": "id", "ko-KR": "ko", "ja": "ja", "ru": "en", "ar-EG": "en", "hi": "en",
            "fr_CA": "fr", "": "en", "xx": "en",
        }
        for tag, want in cases.items():
            self.assertEqual(bl.resolve(tag, SUPPORTED), want, tag)

    def test_build_refuses_missing_strings(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        (d / "content").mkdir()
        (d / "games.json").write_text('{"langs": ["en", "ko"]}', encoding="utf-8")
        (d / "content" / "landing.json").write_text('{"strings": {"en": {"name": "English"}}}', encoding="utf-8")
        with self.assertRaises(SystemExit):
            bl.render(d)


if __name__ == "__main__":
    unittest.main()
