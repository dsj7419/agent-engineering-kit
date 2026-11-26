# Optional quality-gate runner

Requires Python 3.9+; no third-party packages. This is an optional command runner, not an architecture analyzer or security sandbox. Only run trusted, reviewed commands. It inherits the calling environment and permissions; commands can perform arbitrary actions. Configure safe test environments, avoid production, and do not pass secrets on command lines. Timeouts terminate the direct process; descendant process cleanup is not guaranteed. No automatic retries, installation, shell expansion or parallel execution. Console output is streamed; JSON records command metadata and outcomes, not captured stdout/stderr. Retain sanitized CI logs as needed. Record the exact source snapshot and environment separately; the runner does not attest to Git state or protect against concurrent edits.

## Configure

Copy `docs/state/quality-gates.example.json` to `docs/state/quality-gates.json` in your project. The example is intentionally unconfigured. After confirming the approved commands and prerequisites, set `configured` to true and fill gates. Example only (use only if your actual project has these scripts):

```json
{
  "schema_version": 1,
  "configured": true,
  "gates": [
    {"id": "unit", "level": 1, "argv": ["python", "-m", "pytest", "tests/unit"], "cwd": ".", "timeout_seconds": 120, "required": true},
    {"id": "architecture", "level": 2, "argv": ["lint-imports"], "cwd": ".", "timeout_seconds": 60, "required": true}
  ]
}
```

Each gate has a unique ID, minimum level (1–3), argv array, existing repository-relative cwd, positive timeout (1–86400 seconds), and required boolean. Level 2 runs levels 1 and 2; level 3 runs all. Include at least one required selected gate. Optional failed/blocked checks remain visible but do not determine the required-gate exit status; do not mark policy-required checks optional. Do not assume Windows batch wrappers behave like native executables; use a trusted explicit interpreter or native command appropriate to your environment. Commands and paths are not sanitized for arbitrary untrusted inputs.

```text
python tools/engineering/run_gates.py --config docs/state/quality-gates.json --level 2
python tools/engineering/run_gates.py --config docs/state/quality-gates.json --level 3 --report gate-report.json
python -m unittest discover -s tools/engineering -p "test_*.py" -v
```

Exit 0: required selected commands passed; 1: one or more required selected commands failed or blocked; 2: configuration/report error or no required selection; 130: interrupted. Above-level checks are NOT_RUN. Existing reports are not overwritten. A zero exit code is not evidence of unconfigured gates, independent review, or semantic correctness. An interrupted run does not produce a final report. Keep the manifest and project QUALITY_GATES.md aligned.
