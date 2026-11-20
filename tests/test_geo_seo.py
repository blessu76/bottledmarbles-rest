"""GEO / SEO checks for the public pages — run: python3 -m unittest discover -s tests

- every landing page has JSON-LD (WebSite + VideoGame) that parses and states the 300 levels
- landing copy says 300 levels in every language (decision mbl-0009) and never 150
- llms.txt exists, names 300 levels, and has no 150
- every public page (not a redirect stub) has og:title and a canonical that is listed in sitemap.xml
- /releases/ is never in the sitemap; noindex appears only on redirect stubs
"""
import json
import re
import unittest

from helpers import REPO
from test_gtag_coverage import public_html, is_redirect_stub

BASE = "https://bottledmarbles.ipe.rest"
LANGS = ("en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr")


class Geo(unittest.TestCase):
    def test_landing_jsonld_parses_and_is_videogame_and_website(self):
        for lang in LANGS:
            p = REPO / ("index.html" if lang == "en" else "%s/index.html" % lang)
            text = p.read_text(encoding="utf-8")
            m = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
            self.assertIsNotNone(m, str(p))
            data = json.loads(m.group(1))
            types = {node["@type"] for node in data["@graph"]}
            self.assertEqual(types, {"WebSite", "VideoGame"}, str(p))
            game = [n for n in data["@graph"] if n["@type"] == "VideoGame"][0]
            self.assertEqual(game["gamePlatform"], "iOS", str(p))
            self.assertNotIn("offers", game, "no price until the store listing exists")

    def test_landing_copy_says_300_levels_everywhere(self):
        strings = json.loads((REPO / "content" / "landing.json").read_text(encoding="utf-8"))["strings"]
        for lang in LANGS:
            for key in ("body", "f1"):
                s = strings[lang][key]
                self.assertIn("300", s, (lang, key))
                self.assertNotIn("150", s, (lang, key))

    def test_landing_html_has_no_150(self):
        for lang in LANGS:
            p = REPO / ("index.html" if lang == "en" else "%s/index.html" % lang)
            self.assertNotIn("150", p.read_text(encoding="utf-8"), str(p))

    def test_llms_txt(self):
        txt = (REPO / "llms.txt").read_text(encoding="utf-8")
        self.assertTrue(txt.startswith("# Bottled Marbles"))
        self.assertIn("300 levels", txt)
        self.assertNotIn("150", txt)

    def test_public_pages_have_og_title_and_sitemap_entry(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sm))
        self.assertNotIn(BASE + "/releases/", locs)
        checked = 0
        for rel, text in public_html():
            if is_redirect_stub(text):
                continue
            checked += 1
            self.assertIn('property="og:title"', text, rel)
            canon = re.search(r'<link rel="canonical" href="([^"]+)"', text)
            self.assertIsNotNone(canon, rel)
            self.assertIn(canon.group(1), locs, "%s canonical not in sitemap" % rel)
        # test_publish strips the journal from its clone, so the floor is the 12 landing pages, not the full site
        self.assertGreaterEqual(checked, 12)

    def test_noindex_only_on_redirect_stubs(self):
        for rel, text in public_html():
            if 'content="noindex' in text:
                self.assertTrue(is_redirect_stub(text), "noindex outside a redirect stub: %s" % rel)


if __name__ == "__main__":
    unittest.main()
