"""assets/landing.js language detection + redirect rules, run in node with a fake window (skipped when node is missing)."""
import json
import shutil
import subprocess
import unittest

from helpers import REPO

NODE = shutil.which("node")

RUNNER = r"""
const fs = require("fs"), vm = require("vm");
const c = JSON.parse(process.argv[process.argv.length - 1]);
let redirect = null;
const store = c.saved ? { ipe_lang: c.saved } : {};
const ctx = {
  location: { pathname: c.path, search: c.search || "", hash: c.hash || "", replace: (u) => { redirect = u; }, set href(u) { redirect = u; } },
  navigator: { languages: c.languages, language: (c.languages || [])[0], userAgent: c.ua || "Mozilla/5.0 Safari" },
  localStorage: c.blocked ? { getItem() { throw new Error("x"); }, setItem() { throw new Error("x"); } } : { getItem: (k) => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; } },
  document: { querySelector: () => null },
};
vm.runInNewContext(fs.readFileSync(c.js, "utf8"), ctx);
console.log(JSON.stringify({ redirect }));
"""


def run(path, languages, **kw):
    case = dict(path=path, languages=languages, js=str(REPO / "assets" / "landing.js"), **kw)
    out = subprocess.check_output([NODE, "-e", RUNNER, json.dumps(case)], universal_newlines=True)
    return json.loads(out)["redirect"]


@unittest.skipUnless(NODE, "node not installed")
class LangJsTest(unittest.TestCase):
    def test_root_follows_browser_language(self):
        self.assertEqual(run("/", ["ja-JP", "en"]), "/ja/")
        self.assertEqual(run("/", ["zh-TW"]), "/zh-Hant/")
        self.assertEqual(run("/", ["zh-CN"]), "/zh-Hant/")   # zh-* -> zh-Hant (Davy 2026-11-14 brief)
        self.assertEqual(run("/", ["pt-PT"]), "/pt-BR/")
        self.assertEqual(run("/", ["in"]), "/id/")
        self.assertEqual(run("/", ["it-IT", "de-AT"]), "/de/")  # first matching language wins
        self.assertEqual(run("/index.html", ["fr"]), "/fr/")

    def test_no_match_or_english_stays(self):
        self.assertIsNone(run("/", ["it", "ru"]))
        self.assertIsNone(run("/", ["en-US"]))
        self.assertIsNone(run("/", []))

    def test_journal_roots_keep_their_path(self):
        self.assertEqual(run("/journal/", ["ko-KR"]), "/ko/journal/")
        self.assertEqual(run("/journal/four-marbles-per-bottle/", ["ja"], search="?v=1", hash="#x"), "/ja/journal/four-marbles-per-bottle/?v=1#x")

    def test_language_urls_never_redirect(self):
        for path in ("/ko/", "/ja/", "/zh-Hant/", "/ko/journal/", "/de/journal/x/"):
            self.assertIsNone(run(path, ["ja"]), path)
            self.assertIsNone(run(path, ["en"], saved="ja"), path)

    def test_other_paths_untouched(self):
        self.assertIsNone(run("/privacy/", ["ja"]))
        self.assertIsNone(run("/terms/", ["ja"]))

    def test_saved_choice_beats_browser_language(self):
        self.assertEqual(run("/", ["ja"], saved="ko"), "/ko/")
        self.assertIsNone(run("/", ["ja"], saved="en"))        # explicit English choice sticks
        self.assertEqual(run("/", ["ja"], saved="xx"), "/ja/")   # garbage in storage is ignored

    def test_blocked_storage_falls_back_to_detection(self):
        self.assertEqual(run("/", ["es-MX"], blocked=True), "/es/")

    def test_bots_never_redirect(self):
        for ua in ("Googlebot/2.1", "Mozilla/5.0 (compatible; bingbot)", "Yahoo! Slurp", "Chrome-Lighthouse", "some-spider", "Crawler X"):
            self.assertIsNone(run("/", ["ja"], ua=ua), ua)


if __name__ == "__main__":
    unittest.main()
