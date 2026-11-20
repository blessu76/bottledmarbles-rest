"""Privacy / terms: ipe.rest/legal is the source of truth. This site only keeps redirect stubs at /privacy/ /terms/ /ko/privacy/ /ko/terms/,
and every footer, llms.txt and sitemap link points at ipe.rest (ko -> /ko/legal/…, the rest -> /legal/…)."""
import re
import unittest

from helpers import REPO

import build_landing as bl  # noqa: E402
import build_redirects as br  # noqa: E402
import chrome  # noqa: E402

BASE = "https://bottledmarbles.ipe.rest"
IPE = "https://ipe.rest"
STUBS = {
    "privacy/index.html": IPE + "/legal/privacy/",
    "terms/index.html": IPE + "/legal/terms/",
    "ko/privacy/index.html": IPE + "/ko/legal/privacy/",
    "ko/terms/index.html": IPE + "/ko/legal/terms/",
}
LEGAL_HREF = r'href="https://ipe\.rest/(?:ko/)?legal/(?:privacy|terms)/"'


class Legal(unittest.TestCase):
    def test_four_stubs_match_build_and_point_to_ipe_rest(self):
        pages = br.render()
        for rel, url in STUBS.items():
            self.assertIn(rel, pages)
            self.assertEqual((REPO / rel).read_text(encoding="utf-8"), pages[rel], rel)
            text = pages[rel]
            self.assertIn('<link rel="canonical" href="%s">' % url, text, rel)
            self.assertIn('http-equiv="refresh" content="0; url=%s"' % url, text, rel)
            self.assertIn('location.replace("%s"+location.search+location.hash)' % url, text, rel)
            self.assertIn('<a href="%s">' % url, text, rel)
            self.assertIn('content="noindex,follow"', text, rel)
            self.assertNotIn("hreflang", text, rel)
            self.assertNotIn("googletagmanager", text, rel)
            self.assertNotIn("<main", text, rel)   # a stub, not a page: no legal copy on this site

    def test_stub_html_lang_and_total_stub_count(self):
        pages = br.render()
        self.assertEqual(len(pages), 14)   # 5 retired languages x (home, journal) + 4 legal stubs
        for rel in STUBS:
            want = "ko" if rel.startswith("ko/") else "en"
            self.assertEqual(re.search(r'<html lang="([^"]+)"', pages[rel]).group(1), want, rel)

    def test_chrome_legal_paths(self):
        self.assertEqual(chrome.legal_path("privacy", "en"), IPE + "/legal/privacy/")
        self.assertEqual(chrome.legal_path("terms", "ko"), IPE + "/ko/legal/terms/")
        for lang in ("ja", "zh-Hant", "pt-BR", "tr", "de"):   # untranslated -> English policy
            self.assertEqual(chrome.legal_path("privacy", lang), IPE + "/legal/privacy/", lang)

    def test_footer_links_by_language_point_to_ipe_rest(self):
        landing = bl.render(REPO)
        ko_footer = re.search(r"<footer.*?</footer>", landing["ko/index.html"], re.S).group(0)
        self.assertIn('href="%s/ko/legal/privacy/"' % IPE, ko_footer)
        self.assertIn('href="%s/ko/legal/terms/"' % IPE, ko_footer)
        ja_footer = re.search(r"<footer.*?</footer>", landing["ja/index.html"], re.S).group(0)
        self.assertIn('href="%s/legal/privacy/"' % IPE, ja_footer)
        self.assertIn('href="%s/legal/terms/"' % IPE, ja_footer)
        for rel, h in landing.items():
            if rel.endswith("index.html"):
                self.assertEqual(len(re.findall(LEGAL_HREF, h)), 2, rel)

    def test_sitemap_has_no_legal_urls(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotRegex(sm, r"/(?:ko/)?(?:privacy|terms|legal)/")
        self.assertEqual(sm, bl.render(REPO)["sitemap.xml"])

    def test_llms_txt_links_to_ipe_rest(self):
        txt = (REPO / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("[Privacy Policy](%s/legal/privacy/)" % IPE, txt)
        self.assertIn("[Terms of Use](%s/legal/terms/)" % IPE, txt)
        self.assertNotIn(BASE + "/privacy/", txt)
        self.assertNotIn(BASE + "/terms/", txt)


if __name__ == "__main__":
    unittest.main()
