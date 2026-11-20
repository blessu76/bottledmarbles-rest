"""GA4 coverage: every public index.html loads gtag with the one company measurement ID — run: python3 -m unittest discover -s tests

Exceptions are explicit (a new page without gtag fails here until it is added on purpose):
  - redirect stubs (meta refresh + noindex, no analytics by design): /releases/ and the retired-language stubs
  - ALLOWLIST: legal pages, intentionally bare pending Davy's decision
Source of the snippet: scripts/chrome.py ga_head() (used by build_landing.py and build_journal.py _head, so legal pages get it too).
Modelled on idle-rest/tests/test_gtag_coverage.py.
"""
import re
import unittest

from helpers import REPO

GA_ID = "G-XG4BH800J0"
SKIP_TOP = ("content", "scripts", "tests", "assets", "node_modules", ".git")
ALLOWLIST = {
    # legal pages stay bare until Davy decides: privacy/terms say the site has no analytics (tests/test_legal.py guards it)
    "privacy/index.html", "terms/index.html", "ko/privacy/index.html", "ko/terms/index.html",
}


def public_html():
    for p in sorted(REPO.rglob("*.html")):
        rel = p.relative_to(REPO)
        if rel.parts[0] in SKIP_TOP:
            continue
        yield rel.as_posix(), p.read_text(encoding="utf-8")


def is_redirect_stub(text):
    head = text.split("</head>")[0]
    return 'http-equiv="refresh"' in head and 'content="noindex' in head


class GtagCoverage(unittest.TestCase):
    def test_every_public_page_has_gtag_or_is_an_allowed_exception(self):
        missing = []
        seen = 0
        for rel, text in public_html():
            if rel in ALLOWLIST or is_redirect_stub(text):
                continue
            seen += 1
            if "googletagmanager.com/gtag/js" not in text or "gtag('config'" not in text:
                missing.append(rel)
        # test_publish strips the journal from its clone, so the floor is the 12 landing pages, not the full site
        self.assertGreaterEqual(seen, 12, "too few public pages found — the walk is broken")
        self.assertEqual(missing, [], "public pages without the GA4 snippet (fix the generator, not the HTML; or add to ALLOWLIST on purpose)")

    def test_all_gtag_pages_use_the_one_measurement_id(self):
        other = []
        for rel, text in public_html():
            if "googletagmanager.com/gtag/js" not in text:
                continue
            ids = set(re.findall(r"G-[A-Z0-9]{8,}", text))
            if ids != {GA_ID}:
                other.append((rel, sorted(ids)))
        self.assertEqual(other, [])

    def test_gtag_snippet_skips_localhost(self):
        for rel, text in public_html():
            if "googletagmanager.com/gtag/js" not in text:
                continue
            self.assertIn("'127.0.0.1'", text, rel)
            self.assertIn("'localhost'", text, rel)

    def test_allowlist_entries_exist_and_stay_bare(self):
        for rel in ALLOWLIST:
            p = REPO / rel
            self.assertTrue(p.exists(), "stale ALLOWLIST entry: %s" % rel)
            self.assertNotIn("googletagmanager", p.read_text(encoding="utf-8"), "%s now has gtag — drop it from ALLOWLIST" % rel)


if __name__ == "__main__":
    unittest.main()
