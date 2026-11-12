import re
import unittest

from helpers import REPO

BASE = "https://bottledmarbles.ipe.rest"
PAGES = {"index.html": BASE + "/"}


class SeoBasics(unittest.TestCase):
    def test_robots_points_to_sitemap(self):
        txt = (REPO / "robots.txt").read_text()
        self.assertIn("Sitemap: %s/sitemap.xml" % BASE, txt)

    def test_sitemap_lists_pages(self):
        xml = (REPO / "sitemap.xml").read_text()
        for url in PAGES.values():
            self.assertIn("<loc>%s</loc>" % url, xml)

    def test_pages_have_canonical_and_og(self):
        for path, url in PAGES.items():
            html = (REPO / path).read_text()
            self.assertIn('<link rel="canonical" href="%s">' % url, html, path)
            for p in ("og:title", "og:description", "og:type", "og:url"):
                self.assertTrue(re.search(r'<meta property="%s" content="[^"]+"' % p, html), (path, p))


if __name__ == "__main__":
    unittest.main()
