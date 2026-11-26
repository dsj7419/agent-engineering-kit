#!/usr/bin/env python3
"""Compile and execute the Java cohesion example in a disposable directory."""
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    javac, java = shutil.which('javac'), shutil.which('java')
    if not javac or not java:
        raise SystemExit('BLOCKED: a Java 17+ JDK is required')
    sources = sorted((ROOT / 'examples/java-order/src').rglob('*.java'))
    if not sources:
        raise SystemExit('BLOCKED: Java example sources missing')
    with tempfile.TemporaryDirectory() as output:
        subprocess.run([javac, '--release', '17', '-Xlint:all', '-Werror', '-d', output,
                        *map(str, sources)], check=True, timeout=60)
        subprocess.run([java, '-cp', output, 'example.order.OrderTest'], check=True, timeout=30)


if __name__ == '__main__':
    main()
