"""Exercise the Windows wrappers with real, competing PATH applications."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from install_kit import payload

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(os.name == 'nt', 'Windows PowerShell wrappers require Windows')
class PowerShellInstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.shells = [path for name in ('powershell.exe', 'pwsh.exe')
                       if (path := shutil.which(name))]
        self.assertTrue(self.shells, 'No PowerShell executable available')
        self.broken = self.base / 'broken Python'
        self.broken.mkdir()
        (self.broken / 'python.exe').write_bytes(b'not a Windows executable')

    def invoke(self, shell, target, *flags, working_python=True):
        directories = [str(self.broken)]
        if working_python:
            directories.append(str(Path(sys.executable).parent))
        directories.append(str(Path(os.environ['SystemRoot']) / 'System32'))
        env = {**os.environ, 'PATH': os.pathsep.join(directories),
               'PYTHONDONTWRITEBYTECODE': '1'}
        return subprocess.run(
            [shell, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
             str(ROOT / 'INSTALL.ps1'), '-Target', str(target), '-WithTools', *flags],
            env=env, capture_output=True, text=True, timeout=30)

    def test_multiple_python_matches_preview_and_apply(self):
        for index, shell in enumerate(self.shells):
            with self.subTest(shell=shell):
                target = self.base / f'project with spaces {index}'
                target.mkdir()
                preview = self.invoke(shell, target)
                self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
                self.assertEqual(list(target.iterdir()), [])
                applied = self.invoke(shell, target, '-Apply')
                self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
                expected = {}
                for source in payload(ROOT, True):
                    relative = (Path('docs/engineering/KIT-LICENSE.txt')
                                if source.name == 'LICENSE' else source.relative_to(ROOT))
                    expected[relative.as_posix()] = source.read_bytes()
                actual = {p.relative_to(target).as_posix(): p.read_bytes()
                          for p in target.rglob('*') if p.is_file()}
                self.assertEqual(actual, expected)

    def test_no_working_python_writes_nothing(self):
        for index, shell in enumerate(self.shells):
            with self.subTest(shell=shell):
                target = self.base / f'blocked project {index}'
                target.mkdir()
                result = self.invoke(shell, target, '-Apply', working_python=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Python 3.9+', result.stderr)
                self.assertEqual(list(target.iterdir()), [])

    def test_installer_conflict_exit_is_preserved(self):
        for index, shell in enumerate(self.shells):
            with self.subTest(shell=shell):
                target = self.base / f'existing project {index}'
                target.mkdir()
                (target / 'GEMINI.md').write_text('existing project instructions')
                result = self.invoke(shell, target, '-Apply')
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual([p.name for p in target.iterdir()], ['GEMINI.md'])
                self.assertEqual((target / 'GEMINI.md').read_text(),
                                 'existing project instructions')


if __name__ == '__main__':
    unittest.main()
