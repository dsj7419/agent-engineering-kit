# Agent Workflow and Operating Modes

## Mode selection

| Mode | Objective | Default write authority |
|---|---|---|
| IMPLEMENT | Requested feature or behavior | Scoped implementation |
| REFACTOR | Improve structure without changing behavior | Scoped refactor if requested |
| HOTFIX | Smallest safe correction for confirmed defect | Scoped fix |
| AUDIT | Systematic inventory and findings | Read-only |
| REVIEW | Independent diff review | Read-only |
| ARCHITECT | Alternatives and design proposal | Read-only |
| HANDOFF | Reconstruct verified project context | Read-only until implementation or documentation writes authorized |

User authorization to implement a task covers ordinary scoped edits and relevant safe verification, not unrelated changes or protected operations. Request approval for material scope expansion. In read-only modes, commands can be run only if compatible with read-only scope; some builds/tests create files, modify caches or contact external services. Use safe isolation or request permission. Return reports in the conversation unless writing report files is authorized. Never transition from audit/review/proposal to implementation merely because findings exist.

## Risk and verification

Use the risk-based bootstrap in `../../AGENTS.md`. Fast path is an optimization for initialized, known-context Level 1 IMPLEMENT/HOTFIX tasks; it is not a waiver of the constitution, local policies, approved verification or reporting. Full bootstrap is mandatory for initial discovery, stale/unknown context, Levels 2–3 and the other modes specified in AGENTS.md. Reassess risk when scope or evidence changes. The operating mode controls authority independently of risk.

- **Level 1 / routine:** Small localized change, no material contract, persistence, security or concurrency impact. Focused discovery, tests and applicable routine gates.
- **Level 2 / significant:** Multi-component feature/refactor, public behavior change or broad dependency impact. Written staged plan, baseline, regression/integration tests, build/typecheck and architecture checks where applicable.
- **Level 3 / high risk:** Auth/security, money/data integrity, migrations, concurrent core engine, release or cross-context redesign. Explicit risks and rollback, full applicable gates, independent review, explicit approval for protected changes. Escalate risk whenever warranted.

Use the exact project gates and their applicability in `../state/QUALITY_GATES.md`. Run targeted checks after each meaningful stage; run all applicable final gates before claiming verified completion. Never downgrade risk to avoid verification. A one-line change can be high risk.

## Execution loop

1. Bootstrap per root instructions; inspect Git status, diff, scope and relevant contracts. Establish baseline and report uncertainty.
2. Define observable acceptance criteria, risk, dependencies and impact. For significant work use `../state/plans/PLAN_TEMPLATE.md` (copy only when authorized). Identify checkpoints and rollback.
3. Implement minimal cohesive changes; test each stage. Keep unrelated findings in a separate register.
4. Inspect full task diff including untracked additions; run relevant final gates; resolve introduced defects. If a check is unavailable, record exact blocker. Do not weaken checks.
5. Obtain independent review where required; remediate validated findings and reverify any materially changed revision. Report actual final status.
6. Record state after meaningful authorized write milestones and before planned handoff. If interrupted, report the last known safe point without claiming future completion.

## Multi-agent coordination

Assign one implementing writer per working tree. Independent reviewers may inspect a fixed revision/diff in read-only mode. For parallel writing, use explicitly authorized isolated worktrees/branches, non-overlapping scope and a designated integration owner; do not assume Git merge resolves semantic conflicts. No agent may approve its own change as independent review.

A practical assignment is Claude/Codex/Gemini as interchangeable implementer, independent reviewer, and architecture auditor; assign based on capability and available credits, not vendor identity. CI is the objective gate, not another agent's opinion. Do not imply this kit automatically invokes or connects agents.

## Handoff contract

Use `../state/CURRENT_STATE.md` for active tasks. Record branch, HEAD, worktree status, baseline, verification revision/snapshot, active plan, completed and partial changes, remaining risks and safe next action. A HEAD hash alone does not identify uncommitted changes; record a reproducible diff/snapshot identifier where available, otherwise mark dirty verification as non-reproducible and rerun. Never put secrets, sensitive diffs or production data in handoff files. Record verification time and commands; note that state-document updates can change the working tree afterward. A receiving agent independently checks current HEAD/status/diff, applicable ADRs, actual behavior and the relevant tests; stale reports are not current verification. Resolve conflicting ownership before editing.
