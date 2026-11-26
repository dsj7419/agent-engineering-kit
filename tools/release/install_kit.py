#!/usr/bin/env python3
"""Preview or install the portable kit without overwriting existing files."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def payload(root, with_tools):
    """Select only portable files, excluding release infrastructure and caches."""
    names = ['AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'LICENSE']
    engineering = ('CONSTITUTION.md', 'AGENT_WORKFLOW.md', 'AUDIT_PROTOCOL.md',
                   'REFACTORING_PROTOCOL.md', 'REVIEW_PROTOCOL.md', 'STACK_PROFILES.md',
                   'METRICS_POLICY.md', 'STANDARDS_ALIGNMENT.md', 'UPGRADING.md')
    names.extend('docs/engineering/' + name for name in engineering)
    state = ('ARCHITECTURE.md', 'CURRENT_STATE.md', 'DOMAIN_MODEL.md', 'QUALITY_GATES.md',
             'SECURITY.md', 'TECHNICAL_DEBT.md', 'METRICS_PROFILE.md', 'quality-gates.example.json',
             'adr/000-template.md', 'audits/AUDIT_TEMPLATE.md', 'audits/SYMBOL_INVENTORY.csv',
             'plans/PLAN_TEMPLATE.md', 'reviews/REVIEW_TEMPLATE.md')
    names.extend('docs/state/' + name for name in state)
    if with_tools:
        names.extend('tools/engineering/' + name for name in
                     ('README.md', 'run_gates.py', 'test_run_gates.py'))
    paths = [root / name for name in names]
    for path in paths:
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'missing or unsafe portable source: {path.relative_to(root)}')
    return paths


def destination(target, relative):
    """Reject symbolic links and non-directory ancestors in destination paths."""
    path = target
    for part in relative.parts[:-1]:
        path = path / part
        if (path.is_symlink() or not path.resolve().is_relative_to(target)
                or (path.exists() and not path.is_dir())):
            raise ValueError(f'unsafe destination ancestor: {path}')
    path = target / relative
    if (path.is_symlink() or not path.resolve().is_relative_to(target)
            or (path.exists() and not path.is_file())):
        raise ValueError(f'unsafe destination: {path}')
    return path


def plan(root, target, with_tools):
    """Classify all destinations before writing anything."""
    rows = []
    for source in payload(root, with_tools):
        relative = (Path('docs/engineering/KIT-LICENSE.txt') if source.name == 'LICENSE'
                    else source.relative_to(root))
        dest = destination(target, relative)
        if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'unsafe source: {source}')
        status = 'ADD'
        if dest.exists():
            status = 'IDENTICAL' if source.read_bytes() == dest.read_bytes() else 'CONFLICT'
        rows.append((source, relative, status))
    return rows


def install(rows, target):
    """Create only new files using exclusive writes; never replace existing files."""
    for source, relative, status in rows:
        if status != 'ADD':
            continue
        dest = destination(target, relative)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest = destination(target, relative)
        with source.open('rb') as incoming, dest.open('xb') as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        print(f'CREATED {relative.as_posix()}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path, help='Existing project directory')
    parser.add_argument('--apply', action='store_true', help='Actually create files (default: preview)')
    parser.add_argument('--with-tools', action='store_true', help='Include optional quality-gate runner')
    args = parser.parse_args(argv)
    try:
        if args.target.is_symlink() or not args.target.is_dir():
            raise ValueError('target must be an existing directory, not a symbolic link')
        target = args.target.resolve()
        if target == ROOT or target.is_relative_to(ROOT) or ROOT.is_relative_to(target):
            raise ValueError('target must not overlap the kit source tree')
        rows = plan(ROOT, target, args.with_tools)
        if not rows:
            raise ValueError('empty install payload')
        for _, relative, status in rows:
            print(f'{status:9} {relative.as_posix()}')
        if any(status == 'CONFLICT' for _, _, status in rows):
            print('Conflicts: no files written. Merge manually and review the resulting diff.', file=sys.stderr)
            return 2
        if args.apply:
            install(rows, target)
        else:
            print('Preview only. Use --apply to create files.')
        return 0
    except (OSError, ValueError) as error:
        print(f'BLOCKED: {error}. If applying, inspect for partial new files.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
