# Project Quality Gates — Authoritative Project Template

**Status: UNCONFIGURED.** The kit has no knowledge of the target repository's stack, scripts or CI. An agent must inspect existing tooling and propose exact project commands for approval before treating this template as configured. Continue to honor existing repo gates in the meantime; do not claim verified completion based on this empty template.

## Environment and verification levels
- Stack/tool versions, dependency installation prerequisites, working directories, safe test environment, CI equivalent: UNKNOWN.
- Level 1: applicable focused tests, lint, format verification and static analysis.
- Level 2: Level 1 plus relevant integration/contract tests, build, typecheck, architecture/complexity checks.
- Level 3: all applicable gates, full relevant suite, security/dependency checks, performance/concurrency checks and independent review where required.

Risk levels select the minimum checks; actual applicability and protected criteria override a generic list. Record reasons for missing or inapplicable checks. Level 3 must not be marked complete without required review. For projects without a particular check category, explicitly document why it is not applicable or is a tooling gap. Do not silently omit required checks.

## Approved command registry
| Gate ID | Level (minimum) | Exact command/argv | CWD | Prerequisites / side effects | Expected result | Required? / applicability |
|---|---|---|---|---|---|---|
| TBD | | | | | | |

Resolve build, typecheck, lint, format, unit/integration/contract/E2E tests, dependency/architecture rules, size/complexity, secret/security/dependency scanning, performance and concurrency as relevant. For metrics use METRICS_PROFILE.md: record tool version, counting semantics, comparator, mode, source roots, exclusions, approvals, exception IDs and debt baseline. Only approved blockers are required metric gates; keep advisory diagnostics and review dispositions distinct from gate failures. For test commands, ensure no production systems or secrets are used. Identify any network access or filesystem writes before execution.

## Optional executable runner

`../../tools/engineering/run_gates.py` is a standard-library Python 3.9+ utility; the application itself need not use Python. Copy `quality-gates.example.json` to `quality-gates.json` in this directory and populate approved commands as argv arrays (not shell strings), repository-relative working directories, minimum levels, timeouts and required flags. Keep this registry and the manifest aligned. The manifest is executable configuration: review its contents and authorize commands before running. Never execute untrusted commands or paths; it is not a sandbox. The runner intentionally does not install dependencies or select tools. On Windows, use native executables or explicitly invoke approved interpreters for scripts; do not rely on shell expansion.

From repository root, after configuring:

```text
python tools/engineering/run_gates.py --config docs/state/quality-gates.json --level 2
```

Optionally specify `--report PATH` for JSON evidence (existing reports are not overwritten). Console logs and JSON may contain sensitive output from project commands; sanitize before sharing. Add the approved invocation to existing CI if useful. Do not use the runner in a read-only task if its commands or report would modify files without permission.

The runner treats zero exit status as a process pass only; configure commands so nonzero denotes a failed requirement. Validate output/coverage thresholds separately when needed. A successful runner cannot prove unconfigured requirements were met. It reports above-level gates as NOT_RUN, optional failures explicitly, and returns nonzero for missing configuration or required selected checks that fail/block. An empty or optional-only selection cannot produce a successful verification.

## Verification evidence and protection
Record exact command, CWD, revision/snapshot, timestamp, environment, exit status and meaningful output. PASSED / FAILED / NOT_RUN / NOT_APPLICABLE / BLOCKED are distinct. Use NOT_APPLICABLE only with explicit rationale; no passing claim from prior results or skipped tests. Record baseline failures separately. Required unresolved gates block verified completion; any policy exception needs authorized disposition. Never weaken tests, suppress analyzers, change policy or adjust CI to force success. Review gate configuration changes independently.
