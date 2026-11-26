# Safe Refactoring Protocol

Refactoring improves internal structure without changing observable behavior. A requested bug fix or feature is a behavioral change and must have its own acceptance criteria. Do not silently combine it with cleanup.

## Contract checklist

Identify applicable public signatures, CLI/API/UI workflows, outputs and errors, domain invariants, serialization and configuration, persistence/schema, event ordering and delivery, state transitions, concurrency guarantees, authentication/authorization, external consumers, compatibility, and performance requirements. Explicitly record intended changes and preserve everything else.

## Staged procedure

1. Inspect actual implementation, dependency graph, callers, tests, dynamic registration and externally consumed interfaces. Identify concrete deficiencies and candidate cohesive responsibility boundaries. Compare incremental alternatives to a rewrite.
2. Establish an accurate baseline; record pre-existing failures and unverified behavior. Add characterization tests where inadequate. Confirm the tests protect relevant behavior before restructuring. Do not encode known defects as new requirements; isolate intentional fixes.
3. Define scope, acceptance criteria, stages, risks, rollback and required verification. Obtain approval for breaking contracts, architectural redesign or other protected changes. Audit-driven roadmaps require implementation authorization.
4. Extract or reorganize one cohesive responsibility at a time. Preserve the public facade if necessary. Move dependency wiring to composition boundaries, not business rules. Avoid temporary duplication except under a documented migration with removal criteria.
5. Run targeted checks after each meaningful stage, including contract/integration checks for boundary changes. Stop or isolate newly introduced failures; never overwrite unrelated user changes while recovering.
6. Verify all consumers before deleting obsolete code. Compare final observable behavior and full task diff to the baseline. Run final applicable quality gates and required independent review; update authorized plan, debt and handoff records.

Do not force large cohesive or legacy files into a rewrite merely to reduce size. Apply METRICS_POLICY.md; compare cohesion, coupling, invariants and behavior before extraction. Baseline approved gate violations and confirmed debt, and remediate in reviewable stages. Every stage should be independently understandable, verifiable and reversible within authorized Git/file operations.
