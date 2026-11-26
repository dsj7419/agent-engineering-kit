#!/usr/bin/env python3
"""Run public B001 checks; only execute trusted or externally isolated candidates."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / 'examples/python-order/tests'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    if not (candidate / 'order/application.py').is_file():
        parser.error('candidate must contain order/application.py')
    env = {**os.environ, 'PYTHONPATH': str(candidate), 'PYTHONDONTWRITEBYTECODE': '1',
           'AEK_EXAMPLE_ROOT': str(candidate)}
    commands = [[sys.executable, '-m', 'unittest', 'discover', '-s', str(candidate / 'tests'), '-v'],
                [sys.executable, '-m', 'unittest', 'discover', '-s', str(BASELINE), '-v'],
                [sys.executable, str(HERE / 'discount_acceptance.py'), '-v']]
    statuses = []
    for command in commands:
        try:
            statuses.append(subprocess.run(command, cwd=candidate, env=env, timeout=60).returncode)
        except (OSError, subprocess.TimeoutExpired) as error:
            print(f'BLOCKED: {error}', file=sys.stderr)
            statuses.append(2)
    print(f'candidate_suite={statuses[0]} original_checks={statuses[1]} acceptance={statuses[2]}')
    return 0 if all(status == 0 for status in statuses) else 1


if __name__ == '__main__':
    sys.exit(main())
