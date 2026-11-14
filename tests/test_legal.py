"""/privacy/ and /terms/ (en + ko): committed files match the build, structure, links, sitemap, footer links per language."""
import re
import unittest

from helpers import REPO

import build_landing as bl  # noqa: E402
import build_legal as lg  # noqa: E402
import chrome  # noqa: E402

BASE = "https://bottledmarbles.ipe.rest"
PATHS = {"privacy/index.html": "/privacy/", "terms/index.html": "/terms/",
         "ko/privacy/index.html": "/ko/privacy/", "ko/terms/index.html": "/ko/terms/"}


class Legal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = lg.render(REPO)

    def test_four_pages_match_committed_files(self):
        self.assertEqual(set(self.pages), set(PATHS))
        for rel, text in self.pages.items():
            self.assertEqual((REPO / rel).read_text(encoding="utf-8"), text, rel)

    def test_canonical_hreflang_and_cache_busted_assets(self):
        for rel, h in self.pages.items():
            url = BASE + PATHS[rel]
            self.assertIn('<link rel="canonical" href="%s">' % url, h, rel)
            doc = "privacy" if "privacy" in rel else "terms"
            self.assertEqual(sorted(re.findall(r'rel="alternate" hreflang="([^"]+)"', h)), ["en", "ko", "x-default"], rel)
            self.assertIn('hreflang="x-default" href="%s/%s/"' % (BASE, doc), h, rel)
            self.assertRegex(h, r'/assets/landing\.css\?v=\d+[a-z]?"', rel)
            self.assertRegex(h, r'/assets/landing\.js\?v=\d+[a-z]?"', rel)
            lang = "ko" if rel.startswith("ko/") else "en"
            self.assertIn('<html lang="%s" data-lang="%s">' % (lang, lang), h, rel)

    def test_header_select_two_languages_and_legal_only_in_footer(self):
        for rel, h in self.pages.items():
            header = re.search(r"<header.*?</header>", h, re.S).group(0)
            footer = re.search(r"<footer.*?</footer>", h, re.S).group(0)
            self.assertEqual(re.findall(r'<option value="[^"]*" lang="([^"]+)"', header), ["en", "ko"], rel)
            nav = re.search(r'<nav class="topnav".*?</nav>', header, re.S).group(0)
            self.assertNotRegex(nav, r'/(?:privacy|terms)/', rel)
            self.assertEqual(len(re.findall(r'href="/(?:ko/)?(?:privacy|terms)/"', footer)), 2, rel)

    def test_facts_and_operator_contact(self):
        for rel, h in self.pages.items():
            self.assertIn('mailto:ipe.haven@gmail.com', h, rel)
            self.assertIn("Davy Kim (ipe Studio)", h, rel)
            self.assertNotRegex(h, r"Google Analytics|_ga\b|gtag|Claimball|\[미검증\]", rel)
        for rel in ("privacy/index.html", "ko/privacy/index.html"):
            self.assertIn("16", self.pages[rel], rel)

    def test_footer_links_by_language(self):
        self.assertEqual(chrome.legal_path("privacy", "en"), "/privacy/")
        self.assertEqual(chrome.legal_path("terms", "ko"), "/ko/terms/")
        for lang in ("ja", "zh-Hant", "pt-BR", "tr"):   # untranslated -> English pages
            self.assertEqual(chrome.legal_path("privacy", lang), "/privacy/")
        landing = bl.render(REPO)
        self.assertIn('href="/ko/privacy/"', landing["ko/index.html"])
        self.assertIn('href="/privacy/"', landing["ja/index.html"])

    def test_sitemap_has_four_legal_urls_with_hreflang(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        for p in PATHS.values():
            self.assertIn("<loc>%s%s</loc>" % (BASE, p), sm)
        self.assertEqual(sm, bl.render(REPO)["sitemap.xml"])


if __name__ == "__main__":
    unittest.main()
