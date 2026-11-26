"""Regression checks for portable adaptive policy and release packaging."""
import csv
import json
import unittest
from pathlib import Path

from install_kit import payload

ROOT = Path(__file__).resolve().parents[2]


class PolicyReleaseTests(unittest.TestCase):
    def test_policy_documents_in_portable_payload(self):
        files = {p.relative_to(ROOT).as_posix() for p in payload(ROOT, False)}
        self.assertLessEqual({'docs/engineering/METRICS_POLICY.md',
                              'docs/engineering/STANDARDS_ALIGNMENT.md',
                              'docs/engineering/UPGRADING.md',
                              'docs/state/METRICS_PROFILE.md'}, files)

    def test_metrics_template_does_not_activate_gates(self):
        manifest = json.loads((ROOT / 'docs/state/quality-gates.example.json').read_text())
        self.assertIs(manifest['configured'], False)
        self.assertEqual(manifest['gates'], [])
        self.assertFalse((ROOT / 'docs/state/quality-gates.json').exists())

    def test_audit_inventory_records_metric_evidence(self):
        with (ROOT / 'docs/state/audits/SYMBOL_INVENTORY.csv').open(newline='') as file:
            fields = next(csv.reader(file))
        self.assertEqual(len(fields), len(set(fields)))
        self.assertLessEqual({'metric_tool_version', 'metric_units_and_rule_ids',
                              'cohesion_coupling_evidence', 'metric_disposition',
                              'review_status', 'finding_ids'}, set(fields))

    def test_bootstrap_references_portable_documents(self):
        import re
        text = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        portable = {p.relative_to(ROOT).as_posix() for p in payload(ROOT, False)}
        references = set(re.findall(r'`(docs/[^`]+\.md)`', text))
        self.assertTrue(references)
        self.assertLessEqual(references, portable)

    def test_bootstrap_guardrail_markers(self):
        # Textual regression checks, not proof of agent compliance.
        text = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        always = text.split('**Always:**', 1)[1].split('**Fast path', 1)[0]
        self.assertIn('docs/state/QUALITY_GATES.md', always)
        self.assertIn('docs/state/CURRENT_STATE.md', always)
        self.assertIn('Full path — default when uncertain', text)
        self.assertIn('Escalate to the full path', text)
        self.assertIn('never justify a risk downgrade', text)

    def test_versioned_entry_points(self):
        version = (ROOT / 'VERSION').read_text().strip()
        for name in ('AGENTS.md', 'docs/engineering/CONSTITUTION.md',
                     'docs/state/CURRENT_STATE.md', 'RELEASE_CHECKLIST.md'):
            with self.subTest(name=name):
                self.assertIn(version, (ROOT / name).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
