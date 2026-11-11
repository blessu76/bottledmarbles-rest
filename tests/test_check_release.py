import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO

import check_release as cr  # noqa: E402


def entry(build, version="1.0.0", date="2026-11-11", notes=None):
    if notes is None:
        notes = {"en": ["n1"], "ko": ["n1"]}
    return {"id": "%s-%s" % (version, build), "version": version, "build": str(build),
            "status": "testflight", "date": date, "notes": notes}


class ReleaseGate(unittest.TestCase):
    def make_root(self, entries):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        (d / "content").mkdir()
        (d / "games.json").write_text(json.dumps({"langs": ["en", "ko"]}), encoding="utf-8")
        (d / "content" / "releases.json").write_text(json.dumps({"releases": entries}), encoding="utf-8")
        return d

    def test_repo_entries_are_complete(self):
        self.assertEqual(cr.check_all(REPO), [])

    def test_repo_has_build_1_and_2(self):
        entries, errs = cr.load_releases(REPO)
        self.assertEqual(errs, [])
        self.assertEqual({str(e["build"]) for e in entries}, {"1", "2"})

    def test_missing_build_fails(self):
        d = self.make_root([entry(2)])
        self.assertTrue(any("no entry" in x for x in cr.check(d, "99")))

    def test_missing_file_fails(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        (d / "games.json").write_text(json.dumps({"langs": ["en", "ko"]}), encoding="utf-8")
        self.assertTrue(any("missing" in x for x in cr.check(d, "2")))

    def test_empty_ko_notes_fail(self):
        d = self.make_root([entry(2, notes={"en": ["n1"], "ko": []})])
        self.assertTrue(any("notes.ko" in x for x in cr.check(d, "2")))

    def test_non_string_notes_fail(self):
        d = self.make_root([entry(2, notes={"en": [1], "ko": ["n1"]})])
        self.assertTrue(any("notes.en" in x for x in cr.check(d, "2")))

    def test_duplicate_build_fails(self):
        d = self.make_root([entry(2), entry(2)])
        self.assertTrue(any("expected one" in x for x in cr.check(d, "2")))
        self.assertTrue(any("expected one" in x for x in cr.check_all(d)))

    def test_latest_flag(self):
        d = self.make_root([entry(2), entry(1)])
        self.assertEqual(cr.check(d, "2", latest=True), [])
        self.assertTrue(any("not the newest" in x for x in cr.check(d, "1", latest=True)))

    def test_testflight_needs_date(self):
        d = self.make_root([entry(2, date="")])
        self.assertTrue(any("needs a date" in x for x in cr.check(d, "2")))

    def test_bad_id_fails(self):
        e = entry(2)
        e["id"] = "wrong"
        d = self.make_root([e])
        self.assertTrue(any("should be" in x for x in cr.check(d, "2")))

    def test_check_all_refuses_empty(self):
        d = self.make_root([])
        self.assertTrue(any("no entries" in x for x in cr.check_all(d)))

    def test_parse_build(self):
        self.assertEqual(cr.parse_build("2"), "2")
        self.assertEqual(cr.parse_build("1.0.0+2"), "2")
        self.assertIsNone(cr.parse_build("abc"))


if __name__ == "__main__":
    unittest.main()
