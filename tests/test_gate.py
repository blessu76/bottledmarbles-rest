"""ops/gate_publish.py: slot draw, same-hour exclusion, date rollover, already-published ignored, retry on failure."""
import datetime as dt
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import REPO

spec = importlib.util.spec_from_file_location("gate", str(REPO / "ops" / "gate_publish.py"))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def at(s):
    return "2026-%s:00+09:00" % s


class GateTest(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)
        self.state = self.d / "slot.json"
        self.mark = self.d / "ran"

    def run_gate(self, now, cmd=None):
        cmd = cmd or "echo x >> %s" % self.mark
        return gate.main(["--state", str(self.state), "--now", at(now), "--publish-cmd", cmd])

    def runs(self):
        return len(self.mark.read_text().split()) if self.mark.exists() else 0

    def read(self):
        return json.loads(self.state.read_text())

    def test_draw_is_in_window_and_never_same_hour_as_yesterday(self):
        for day in range(1, 29):
            for prev_h in range(12, 18):
                t = gate.draw_time("2026-11-%02d" % day, "%02d:30" % prev_h)
                self.assertTrue("12:00" <= t <= "17:59", t)
                self.assertNotEqual(int(t[:2]), prev_h)

    def test_rollover_moves_today_into_prev(self):
        self.state.write_text(json.dumps({"date": "2026-11-13", "time": "15:10", "prev_date": None, "prev_time": None, "published": True}))
        self.run_gate("11-14T12:00")
        s = self.read()
        self.assertEqual((s["date"], s["prev_date"], s["prev_time"], s["published"]), ("2026-11-14", "2026-11-13", "15:10", False))
        self.assertNotEqual(s["time"][:2], "15")

    def test_waits_until_slot_then_publishes_once(self):
        self.state.write_text(json.dumps({"date": "2026-11-14", "time": "14:20", "prev_date": None, "prev_time": None, "published": False}))
        self.run_gate("11-14T14:15")
        self.assertEqual(self.runs(), 0)
        self.run_gate("11-14T14:30")
        self.assertEqual(self.runs(), 1)
        self.assertTrue(self.read()["published"])
        self.run_gate("11-14T14:45")
        self.assertEqual(self.runs(), 1)

    def test_already_published_is_ignored(self):
        self.state.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "prev_date": None, "prev_time": None, "published": True}))
        self.run_gate("11-14T17:45")
        self.assertEqual(self.runs(), 0)

    def test_failed_publish_stays_open_and_retries(self):
        self.state.write_text(json.dumps({"date": "2026-11-14", "time": "12:00", "prev_date": None, "prev_time": None, "published": False}))
        self.assertEqual(self.run_gate("11-14T12:15", cmd="exit 3"), 3)
        self.assertFalse(self.read()["published"])
        self.assertEqual(self.run_gate("11-14T12:30"), 0)
        self.assertTrue(self.read()["published"])

    def test_missing_state_draws_fresh_slot(self):
        self.run_gate("11-14T12:00", cmd="true")
        s = self.read()
        self.assertEqual(s["date"], "2026-11-14")
        self.assertIsNone(s["prev_time"])


if __name__ == "__main__":
    unittest.main()
