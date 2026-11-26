"""Small example-specific static import allowlist; not a general analyzer."""
import ast
import os
import unittest
from pathlib import Path

ORDER = Path(os.environ.get('AEK_EXAMPLE_ROOT', str(Path(__file__).resolve().parents[1]))) / 'order'
ALLOWED = {'domain': {'dataclasses'}, 'application': {'typing', 'domain'},
           'infrastructure': set(), 'main': {'application', 'domain', 'infrastructure'}}


def imported_modules(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module in (None, 'order'):
                for alias in node.names:
                    yield alias.name
            else:
                yield node.module.removeprefix('order.')


class ArchitectureTests(unittest.TestCase):
    def test_import_boundaries(self):
        for file in ORDER.glob('*.py'):
            if file.stem == '__init__':
                self.assertEqual(list(imported_modules(ast.parse(file.read_text(encoding='utf-8')))), [])
                continue
            with self.subTest(file=file.name):
                actual = set(imported_modules(ast.parse(file.read_text(encoding='utf-8'))))
                self.assertIn(file.stem, ALLOWED, 'register new module explicitly')
                self.assertLessEqual(actual, ALLOWED[file.stem])

    def test_detector_catches_relative_and_absolute_imports(self):
        for source in ('from . import infrastructure', 'from .infrastructure import X',
                       'from order import infrastructure', 'import order.infrastructure'):
            with self.subTest(source=source):
                self.assertTrue(set(imported_modules(ast.parse(source))) - ALLOWED['domain'])
