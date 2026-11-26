# Principal Engineer Deep Audit Protocol

Start read-only. No source modification until a remediation roadmap is authorized. Persist artifacts only with permission; otherwise return findings and inventory in the report. Follow the constitution and review protocol for severity and evidence.

## Phase 1 — Discovery and scope

Record root, revision/dirty snapshot, source roots, languages, exclusions with reasons, tool availability, and intended coverage. Map bounded contexts, module responsibilities, public surfaces, dependency graph, entry points, critical paths, state ownership, architecture violations and duplicate sources of truth. Inventory authored production files and all relevant functions, methods, classes, modules, including nested/anonymous symbols when identifiable. Use language-aware AST/symbol tooling where possible; document unsupported syntax, generated code and dynamic behavior. Include file-level coverage for code without functions. Tests/config/migrations may need separate risk-based scope; do not hide relevant paths behind exclusions.

## Phase 2 — Structural and symbol coverage

Use `../state/audits/SYMBOL_INVENTORY.csv` as a header template; copy to a task-specific artifact if authorized. Each record includes stable symbol key, path, qualified name, type, responsibility, line range, size, complexity metrics, incoming/outgoing dependencies, ordering assessment, review status, tests/evidence, findings and exclusion/block reason. Use path + fully qualified symbol + signature/disambiguator for overloaded or anonymous functions; line ranges are revision-specific. Inventory file/module records independently from symbol records. Mark unavailable metrics UNKNOWN rather than guessing.

Statuses: NOT_REVIEWED, IN_PROGRESS, REVIEWED_NO_FINDINGS, REVIEWED_WITH_FINDINGS, BLOCKED, EXCLUDED_WITH_JUSTIFICATION. Review each in-scope symbol for correctness, SOLID/SRP, cohesion, coupling, boundaries, ordering, complexity, security, concurrency, reliability, resource lifecycle, performance and test adequacy. Mark non-applicable dimensions with rationale where significant. Apply METRICS_POLICY.md and the approved project profile. Record analyzer/version, units and applicable rule IDs; distinguish raw observations, review-required dispositions, confirmed defects and approved gate failures. Inspect cohesion/coupling and identify genuine extraction boundaries; no fragmentation solely for metrics.

Track separately: files/symbols identified, reviewed, pending, blocked, excluded, findings, and inventory completeness. Report review coverage as reviewed / (identified minus justified exclusions), separately for files and symbols; if the denominator is zero, report N/A. Do not claim comprehensive review if inventory is incomplete, any in-scope item remains pending/blocked, or required areas were inaccessible. Reviewed does not mean executed/tested. Reconcile inventory to the current revision before resuming.

## Phase 3 — Functional, security and concurrency analysis

Trace critical execution paths and cross-module interactions, including failures, domain invariants, state transitions, authorization, OWASP risks, races, deadlocks, resource leaks, N+1 queries and scalability. Use concrete code evidence and plausible failure scenarios; identify downstream consumers, external inputs and assumptions. Distinguish confirmed defects from hypotheses needing verification.

## Phase 4 — Testing analysis

Identify untested business rules, fragile/over-mocked tests, missing boundary/integration tests, uncovered edges, and misleading coverage. Evaluate observable behavior and test effectiveness, not just coverage percentage. Execute authorized applicable checks; record actual status and baseline failures.

## Phase 5 — Findings register

Use stable IDs and the finding format in `REVIEW_PROTOCOL.md`, adding root cause, remediation complexity, regression risk and dependencies. Keep severity and confidence separate. Group related symbols under a single root-cause finding when warranted. Preserve exact revision and evidence. Report inspected, tested, unverified and excluded scope distinctly.

## Phase 6 — Prioritized roadmap

Group findings into small independently verifiable stages, ordered by risk, dependencies, correctness, architecture and maintainability. For each stage identify affected symbols, acceptance criteria, tests, rollback, complexity and prerequisites. Separate mandatory fixes from optional improvements. Prefer incremental refactoring to unnecessary rewrites.

## Phase 7 — Controlled implementation (approval required)

Use `REFACTORING_PROTOCOL.md` and `AGENT_WORKFLOW.md`. Establish behavioral baseline and characterization tests, implement one approved stage at a time, run relevant gates after stages and all applicable final gates, then independently review as required. Update authorized audit, debt, plan and state records. Use `../state/audits/AUDIT_TEMPLATE.md` for the report.
