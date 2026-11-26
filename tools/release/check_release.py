#!/usr/bin/env python3
"""Run the kit's own local verification, not target-project quality gates."""
import ast
import os
import subprocess
import sys
from pathlib import Path

from install_kit import payload

ROOT = Path(__file__).resolve().parents[2]


def main():
    required = ('LICENSE', 'README.md', 'AGENTS.md', 'CLAUDE.md', 'GEMINI.md',
                'SECURITY.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'CITATION.cff',
                'INSTALL.ps1', 'install.sh', '.github/workflows/ci.yml', 'VERSION',
                'docs/engineering/METRICS_POLICY.md', 'docs/engineering/STANDARDS_ALIGNMENT.md',
                'docs/engineering/UPGRADING.md', 'docs/state/METRICS_PROFILE.md',
                'examples/java-order/README.md', 'tools/release/check_java_example.py')
    for name in required:
        if not (ROOT / name).is_file():
            print(f'Missing release file: {name}', file=sys.stderr)
            return 1
    try:
        payload(ROOT, True)
    except ValueError as error:
        print(f"Invalid portable payload: {error}", file=sys.stderr)
        return 1
    version = (ROOT / 'VERSION').read_text().strip()
    for name in ('README.md', 'CITATION.cff', 'CHANGELOG.md'):
        if version not in (ROOT / name).read_text(encoding='utf-8'):
            print(f'Version missing: {name}', file=sys.stderr)
            return 1
    for folder in ('tools', 'examples', 'benchmarks'):
        for path in (ROOT / folder).rglob('*.py'):
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    jobs = [('tools/engineering', '.'), ('tools/release', '.'), ('examples/python-order', 'tests')]
    for directory, tests in jobs:
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', tests, '-v'],
                                cwd=ROOT / directory, env=env, timeout=120)
        if result.returncode:
            return 1
    print('Release checks passed (local environment only).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
