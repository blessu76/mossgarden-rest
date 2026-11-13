"""ops/journal_gate.py: random afternoon slot (12:00-17:59 KST, never the same hour as yesterday), state file, publish gating."""
import json
import random
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import helpers
from helpers import REPO

SCRIPT = REPO / "ops" / "journal_gate.py"
OPS = REPO / "ops"


class JournalGate(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mossgarden-slot-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.slot = self.tmp / "q" / "slot.json"
        self.calls = self.tmp / "calls"

    def run_gate(self, now, publish="echo 'publish_daily: pushed some-slug'", **extra):
        cmd = "echo x >> %s; %s" % (self.calls, publish)
        env = helpers.isolated_env(self.tmp / "home", MOSSGARDEN_SLOT_FILE=str(self.slot), MOSSGARDEN_NOW=now, MOSSGARDEN_PUBLISH_CMD=cmd, **extra)
        return subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, env=env)

    def state(self):
        return json.loads(self.slot.read_text())

    def n_calls(self):
        return len(self.calls.read_text().split()) if self.calls.exists() else 0

    def write(self, **kw):
        self.slot.parent.mkdir(parents=True, exist_ok=True)
        self.slot.write_text(json.dumps(kw))

    def test_draw_in_range_and_never_yesterdays_hour(self):
        for i in range(24):
            prev_hour = 12 + i % 6
            self.write(date="2026-11-12", time="%02d:%02d" % (prev_hour, i % 60), published=True)
            r = self.run_gate("2026-11-13 08:00")           # before any slot: only draws
            self.assertEqual(r.returncode, 0, r.stderr)
            t = self.state()["time"]
            h, m = int(t[:2]), int(t[3:])
            self.assertTrue(12 <= h <= 17 and 0 <= m <= 59, t)
            self.assertNotEqual(h, prev_hour)

    def test_date_rollover_moves_current_to_prev(self):
        self.write(date="2026-11-12", time="14:20", published=True)
        self.run_gate("2026-11-13 09:00")
        s = self.state()
        self.assertEqual((s["date"], s["prev_date"], s["prev_time"], s["published"]), ("2026-11-13", "2026-11-12", "14:20", False))
        self.assertNotEqual(s["time"][:2], "14")
        self.assertEqual(self.n_calls(), 0)

    def test_first_run_without_state_file(self):
        self.run_gate("2026-11-13 09:00")
        s = self.state()
        self.assertEqual((s["date"], s["prev_time"], s["published"]), ("2026-11-13", None, False))

    def test_no_publish_before_slot_time(self):
        self.write(date="2026-11-13", time="15:30", published=False)
        self.run_gate("2026-11-13 15:29")
        self.assertEqual(self.n_calls(), 0)
        self.run_gate("2026-11-13 15:30")
        self.assertEqual(self.n_calls(), 1)
        self.assertTrue(self.state()["published"])

    def test_already_published_is_ignored(self):
        self.write(date="2026-11-13", time="13:00", published=True)
        self.run_gate("2026-11-13 16:00")
        self.assertEqual(self.n_calls(), 0)

    def test_skip_and_failure_keep_false_and_retry(self):
        for out in ("echo 'publish_daily: SKIP — working tree is not clean'", "echo boom; exit 1"):
            self.write(date="2026-11-13", time="13:00", published=False)
            self.run_gate("2026-11-13 13:15", publish=out)
            self.assertFalse(self.state()["published"], out)
        self.write(date="2026-11-13", time="13:00", published=False)
        self.run_gate("2026-11-13 13:30", publish="echo 'publish_daily: nothing to publish'")
        self.assertTrue(self.state()["published"])

    def test_gives_up_after_1845(self):
        self.write(date="2026-11-13", time="13:00", published=False)
        self.run_gate("2026-11-13 18:46")
        self.assertEqual(self.n_calls(), 0)
        self.run_gate("2026-11-13 18:45")
        self.assertEqual(self.n_calls(), 1)

    def test_seed_is_deterministic(self):
        times = []
        for n in range(2):
            self.slot.unlink(missing_ok=True)
            self.run_gate("2026-11-13 08:00", MOSSGARDEN_SEED="7")
            times.append(self.state()["time"])
        self.assertEqual(times[0], times[1])

    def test_draw_function(self):
        import sys
        sys.path.insert(0, str(OPS))
        import journal_gate as jg
        rng = random.Random(1)
        for _ in range(200):
            t = jg.draw("14:05", rng)
            self.assertTrue("12:00" <= t <= "17:59" and t[:2] != "14", t)

    def test_plist_template_has_the_afternoon_ticks(self):
        text = (OPS / "rest.ipe.mossgarden-publish.plist.template").read_text()
        self.assertIn("ops/journal_gate.sh", text)
        self.assertEqual(text.count("<key>Hour</key>"), 28)
        self.assertNotIn("<integer>19</integer>", text)


if __name__ == "__main__":
    unittest.main()
