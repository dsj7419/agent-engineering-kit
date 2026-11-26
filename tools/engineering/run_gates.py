#!/usr/bin/env python3
"""Execute explicitly approved project quality gates and report process outcomes."""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def resolve_cwd(root, value):
    """Restrict configured working directories to the repository tree."""
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("cwd must be a nonempty repository-relative path")
    directory = (root / value).resolve()
    if not directory.is_relative_to(root.resolve()) or not directory.is_dir():
        raise ValueError(f"invalid or out-of-repository cwd: {value}")
    return directory


def validate_gate(gate, root, seen):
    """Validate a command without executing it."""
    if not isinstance(gate, dict):
        raise ValueError("each gate must be an object")
    if set(gate) != {"id", "level", "argv", "cwd", "timeout_seconds", "required"}:
        raise ValueError("gate requires exactly id, level, argv, cwd, timeout_seconds, required")
    name = gate["id"]
    if not isinstance(name, str) or not name.strip() or name in seen:
        raise ValueError("gate IDs must be nonempty and unique")
    seen.add(name)
    if type(gate["level"]) is not int or gate["level"] not in (1, 2, 3):
        raise ValueError(f"{name}: level must be 1, 2 or 3")
    args = gate["argv"]
    if not isinstance(args, list) or not args or not all(
        isinstance(arg, str) and "\0" not in arg for arg in args
    ) or not args[0].strip():
        raise ValueError(f"{name}: argv must be a nonempty array of strings")
    timeout = gate["timeout_seconds"]
    if type(timeout) is not int or not 1 <= timeout <= 86400:
        raise ValueError(f"{name}: timeout_seconds must be an integer from 1 to 86400")
    if type(gate["required"]) is not bool:
        raise ValueError(f"{name}: required must be true or false")
    resolve_cwd(root, gate["cwd"])


def load_config(path, root):
    """Reject unconfigured or malformed manifests before running commands."""
    config = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or set(config) != {"schema_version", "configured", "gates"}:
        raise ValueError("invalid manifest fields")
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ValueError("unsupported manifest schema_version")
    if config["configured"] is not True:
        raise ValueError("manifest is UNCONFIGURED; approve project commands first")
    gates = config["gates"]
    if not isinstance(gates, list) or not gates:
        raise ValueError("manifest must contain at least one gate")
    seen = set()
    for gate in gates:
        validate_gate(gate, root, seen)
    return gates


def execute_gate(gate, root, level):
    """Execute one selected gate; output is streamed to the invoking console."""
    result = {**gate, "status": "NOT_RUN", "exit_code": None, "reason": None,
              "started_at": None, "duration_seconds": None}
    if gate["level"] > level:
        result["reason"] = "above requested verification level"
        return result
    print(f'\n[{gate["id"]}] cwd={gate["cwd"]} argv={json.dumps(gate["argv"])}', flush=True)
    result["started_at"] = utc_now()
    start = time.monotonic()
    try:
        completed = subprocess.run(
            gate["argv"], cwd=resolve_cwd(root, gate["cwd"]),
            stdin=subprocess.DEVNULL, shell=False, timeout=gate["timeout_seconds"],
            check=False,
        )
        result["exit_code"] = completed.returncode
        result["status"] = "PASSED" if completed.returncode == 0 else "FAILED"
    except subprocess.TimeoutExpired:
        result.update(status="BLOCKED", reason="process timeout; descendant cleanup not guaranteed")
    except (OSError, ValueError) as error:
        result.update(status="BLOCKED", reason=str(error))
    result["duration_seconds"] = round(time.monotonic() - start, 3)
    print(f'[{gate["id"]}] {result["status"]} exit={result["exit_code"]} '
          f'{result["reason"] or ""}', flush=True)
    return result


def run_selected(gates, root, level):
    """Require at least one selected required gate and aggregate real outcomes."""
    if not any(gate["required"] and gate["level"] <= level for gate in gates):
        raise ValueError("no required gates selected at this level")
    results = [execute_gate(gate, root, level) for gate in gates]
    success = all(row["status"] == "PASSED" for row in results
                  if row["required"] and row["level"] <= level)
    return results, success


def main(argv=None):
    """Run the trusted manifest and optionally write a new JSON report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "docs/state/quality-gates.json")
    parser.add_argument("--level", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.report is not None and args.report.exists():
            raise ValueError("report already exists; choose a new path")
        gates = load_config(args.config, ROOT)
        started = utc_now()
        results, success = run_selected(gates, ROOT, args.level)
        report = {"schema_version": 1, "started_at": started, "finished_at": utc_now(),
                  "repository_root": str(ROOT), "config": str(args.config.resolve()),
                  "level": args.level, "required_selected_passed": success, "gates": results}
        if args.report is not None:
            with args.report.open("x", encoding="utf-8") as output:
                json.dump(report, output, indent=2)
                output.write("\n")
        print("Required selected gates:", "PASSED" if success else "UNRESOLVED", flush=True)
        return 0 if success else 1
    except (OSError, ValueError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("BLOCKED: interrupted; no final verification claim", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
