# Independent Engineering Review Protocol

Remain read-only unless remediation or report-file writes are explicitly authorized. Review the actual task baseline and full diff, including relevant additions and affected consumers; do not merely accept the implementing agent's report. Identify exact reviewed base and target revision or dirty snapshot, and verification environment. Approval is valid only for the reviewed scope/snapshot.

## Review dimensions

Check requirements and acceptance criteria, business correctness/invariants, SOLID and responsibility cohesion, bounded contexts/dependency direction, file/function ordering, complexity, error handling, state integrity, authorization/input safety, concurrency, resource lifecycle, performance and scalability, compatibility, failure paths, regression and test quality. Review changed gates and tests for weakening or concealed behavior changes. Trace relevant callers and indirect consumers. Evaluate changes first; separate unrelated pre-existing debt. Do not manufacture stylistic findings or assert untested hypotheses as confirmed defects. Apply METRICS_POLICY.md: an advisory size or complexity trigger alone is not a blocking defect. Document justified dispositions, and separately report actual approved gate failures.

## Finding format

Use stable IDs (ARCH-001, SEC-001, LOGIC-001, PERF-001, CONC-001, TEST-001, etc.), severity (CRITICAL/HIGH/MEDIUM/LOW/INFO), independent confidence (HIGH/MEDIUM/LOW), confirmation status, path/line range/fully qualified symbol, evidence, credible failure scenario and impact, affected consumers, recommended remediation and verification. Separate severity (impact) from confidence (evidence quality).

CRITICAL: severe safety/security/data integrity or operational impact; HIGH: significant correctness/security/reliability/contract defect; MEDIUM: material quality or localized reliability/performance deficiency; LOW: limited impact; INFO: observation. Adjust to context; explain severity.

## Outcome

- APPROVED — no blocking findings; required evidence adequate.
- APPROVED_WITH_NON_BLOCKING_FINDINGS — explicitly describe remaining non-blocking findings.
- CHANGES_REQUIRED — confirmed blocking issues (including introduced/exposed critical/high defects) or other acceptance-criteria violations.
- BLOCKED_PENDING_VERIFICATION — insufficient evidence, inaccessible scope or required checks not verified.

Prioritize actionable findings. Report inspected/uninspected scope, tests independently run, existing failures, assumptions, and exact approval snapshot. Do not independently approve your own implementation. If code materially changes after review, re-review the affected scope and rerun applicable gates. Use `../state/reviews/REVIEW_TEMPLATE.md` if authorized to persist a report.
