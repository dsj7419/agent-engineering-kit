"""Self-tests for the optional runner using isolated synthetic commands."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from run_gates import ROOT, execute_gate, load_config, run_selected


def gate(name="example", command=None, level=1, required=True, timeout=5):
    return {"id": name, "level": level, "required": required, "cwd": ".",
            "timeout_seconds": timeout, "argv": command or [sys.executable, "-c", "pass"]}


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "gates.json"

    def manifest(self, gates, configured=True):
        self.path.write_text(json.dumps({"schema_version": 1, "configured": configured,
                                         "gates": gates}), encoding="utf-8")
        return self.path

    def test_unconfigured(self):
        with self.assertRaisesRegex(ValueError, "UNCONFIGURED"):
            load_config(self.manifest([], False), ROOT)

    def test_duplicate_ids(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            load_config(self.manifest([gate(), gate()]), ROOT)

    def test_outside_cwd(self):
        bad = gate()
        bad["cwd"] = ".."
        with self.assertRaisesRegex(ValueError, "cwd"):
            load_config(self.manifest([bad]), ROOT)

    def test_invalid_level(self):
        with self.assertRaisesRegex(ValueError, "level"):
            load_config(self.manifest([gate(level=True)]), ROOT)

    def test_pass_and_skip(self):
        gates = load_config(self.manifest([gate(), gate("later", level=3)]), ROOT)
        results, success = run_selected(gates, ROOT, 1)
        self.assertTrue(success)
        self.assertEqual([r["status"] for r in results], ["PASSED", "NOT_RUN"])

    def test_fail_and_optional(self):
        failing = [sys.executable, "-c", "raise SystemExit(7)"]
        results, success = run_selected([gate(command=failing)], ROOT, 1)
        self.assertFalse(success)
        self.assertEqual(results[0]["exit_code"], 7)
        results, success = run_selected([gate(), gate("optional", failing, required=False)], ROOT, 1)
        self.assertTrue(success)
        self.assertEqual(results[1]["status"], "FAILED")

    def test_missing_executable(self):
        result = execute_gate(gate(command=[str(Path(self.temp.name) / "missing-executable")]), ROOT, 1)
        self.assertEqual(result["status"], "BLOCKED")

    def test_timeout(self):
        result = execute_gate(gate(command=[sys.executable, "-c", "import time; time.sleep(3)"],
                                   timeout=1), ROOT, 1)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("timeout", result["reason"])

    def test_empty_selection(self):
        with self.assertRaisesRegex(ValueError, "no required"):
            run_selected([gate(level=3), gate("optional", required=False)], ROOT, 1)

    def test_cli_report_no_overwrite(self):
        report = Path(self.temp.name) / "report.json"
        command = [sys.executable, str(ROOT / "tools/engineering/run_gates.py"),
                   "--config", str(self.manifest([gate()])), "--level", "1", "--report", str(report)]
        first = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(first.returncode, 0, first.stderr)
        data = json.loads(report.read_text(encoding="utf-8"))
        self.assertTrue(data["required_selected_passed"])
        self.assertEqual(data["gates"][0]["status"], "PASSED")
        second = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(second.returncode, 2)
        self.assertEqual(data, json.loads(report.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
