import re
import unittest

from helpers import REPO
import build_redirects as br


class Redirects(unittest.TestCase):
    def test_targets_follow_kit_rules(self):
        self.assertEqual(br.target("pt", ""), "/pt-BR/")
        self.assertEqual(br.target("zh", "journal/"), "/zh-Hant/journal/")
        for old in ("ar", "hi", "ru"):
            self.assertEqual(br.target(old, ""), "/")
            self.assertEqual(br.target(old, "journal/"), "/journal/")

    def test_ten_stubs_with_refresh_js_canonical_noindex(self):
        pages = br.render()
        self.assertEqual(sorted(pages), sorted("%s/%sindex.html" % (o, r) for o in br.LEGACY for r in br.PATHS))
        for rel, text in pages.items():
            old = rel.split("/")[0]
            rest = rel[len(old) + 1:-len("index.html")]
            url = br.SITE + br.target(old, rest)
            self.assertIn('http-equiv="refresh" content="0; url=%s"' % url, text, rel)
            self.assertIn('<link rel="canonical" href="%s">' % url, text, rel)
            self.assertIn('content="noindex,follow"', text, rel)
            self.assertIn('location.replace("%s"+location.search+location.hash)' % br.target(old, rest), text, rel)
            self.assertIn('<a href="%s">' % url, text, rel)
            self.assertNotIn("hreflang", text)

    def test_committed_files_match_build(self):
        for rel, text in br.render().items():
            self.assertEqual((REPO / rel).read_text(encoding="utf-8"), text, rel)

    def test_sitemap_has_no_retired_language_addresses(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"://[^/<\s]+/(?:pt|zh|ar|hi|ru)(?:[/?#<\s\"']|$)", sm), [])


if __name__ == "__main__":
    unittest.main()
