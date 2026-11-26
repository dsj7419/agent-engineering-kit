"""Integration tests for the portable installer in disposable directories."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'tools/release/install_kit.py'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name) / 'project with spaces'
        self.target.mkdir()

    def run_installer(self, *flags):
        return subprocess.run([sys.executable, str(SCRIPT), '--target', str(self.target), *flags],
                              capture_output=True, text=True, timeout=15)

    def test_preview_no_writes(self):
        self.assertEqual(self.run_installer().returncode, 0)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_apply_and_repeat(self):
        self.assertEqual(self.run_installer('--apply').returncode, 0)
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), (ROOT / 'AGENTS.md').read_bytes())
        self.assertFalse((self.target / 'README.md').exists())
        for relative in ('docs/engineering/METRICS_POLICY.md', 'docs/engineering/STANDARDS_ALIGNMENT.md',
                         'docs/state/METRICS_PROFILE.md'):
            self.assertEqual((self.target / relative).read_bytes(), (ROOT / relative).read_bytes())
        self.assertFalse((self.target / 'tools').exists())
        result = self.run_installer('--apply')
        self.assertEqual(result.returncode, 0)
        self.assertIn('IDENTICAL', result.stdout)
        self.assertNotIn('CREATED', result.stdout)

    def test_conflict_prevents_all_writes(self):
        (self.target / 'GEMINI.md').write_text('existing user instruction')
        self.assertEqual(self.run_installer('--apply').returncode, 2)
        self.assertEqual((self.target / 'GEMINI.md').read_text(), 'existing user instruction')
        self.assertFalse((self.target / 'AGENTS.md').exists())

    def test_optional_tools(self):
        self.assertEqual(self.run_installer('--apply', '--with-tools').returncode, 0)
        self.assertTrue((self.target / 'tools/engineering/run_gates.py').is_file())
        self.assertFalse((self.target / 'docs/state/quality-gates.json').exists())
        self.assertFalse((self.target / '.github').exists())

    def test_missing_required_source_prevents_install(self):
        source = self.target.parent / 'incomplete-kit'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        (source / 'docs/engineering/CONSTITUTION.md').unlink()
        result = subprocess.run([sys.executable, str(source / 'tools/release/install_kit.py'),
                                 '--target', str(self.target), '--apply'],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertIn('missing or unsafe portable source', result.stderr)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_payload_excludes_unexpected_files(self):
        source = self.target.parent / 'kit-copy'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        (source / 'docs/engineering/private-notes.md').write_text('not part of kit')
        result = subprocess.run([sys.executable, str(source / 'tools/release/install_kit.py'),
                                 '--target', str(self.target), '--apply'],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0)
        self.assertFalse((self.target / 'docs/engineering/private-notes.md').exists())

    def test_non_directory_ancestor(self):
        (self.target / 'docs').write_text('not a folder')
        self.assertEqual(self.run_installer('--apply').returncode, 2)
        self.assertFalse((self.target / 'AGENTS.md').exists())

    def test_symlink_ancestor(self):
        outside = self.target.parent / 'outside'
        outside.mkdir()
        try:
            (self.target / 'docs').symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('symbolic links unavailable on this host')
        self.assertEqual(self.run_installer('--apply').returncode, 2)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
