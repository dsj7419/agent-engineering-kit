# Agent Engineering Kit — benchmark protocol

Status: **experimental; no agent comparison results yet**. One reproducible starter task is provided in `tasks/order-discount.md`. Expand the suite to include legacy refactoring, defect detection, security, concurrency and handoffs before drawing broad conclusions.

## Experimental design

1. Freeze the kit version, baseline source digest/commit, task specification, evaluator version and test commands. Copy `examples/python-order/` to a fresh isolated working directory for each run. Do not expose unrelated code or credentials. For a kit-enabled run, install the kit into that copy and bootstrap project state from evidence. For control runs, use only ordinary task instructions and repository documentation. Keep both groups' task requirements identical.
2. Pre-register agent/model version, CLI version, tool permissions, context and token/time budget, baseline, repeat count, evaluator and stopping rule. Use randomized run order and independent sessions. Repeat each arm at least five times for exploratory results; more runs may be needed for useful uncertainty estimates. Record actual costs, retries, failures and aborted runs rather than excluding them post hoc.
3. Give both arms the exact task text and equal access to baseline tests. Do not give agents evaluator internals if measuring generalization; the included evaluator is public, so results using it are open-test results. For stronger studies, freeze independently developed held-out cases before running agents.
4. Run baseline tests and the acceptance evaluator on each final candidate using a disposable environment without credentials. Candidate code is untrusted executable code; isolate it externally, with resource/network restrictions. Do not let agents change the external evaluator. Record test exit status, architecture compliance, behavior, scope, regressions, runtime and token/cost data. Independent reviewers should be blinded to arm where feasible; resolve disagreements using documented rubrics.
5. Report per-task pass rates, failure counts, effect sizes and uncertainty, including cost/time trade-offs and all limitations. Do not equate test success with proof of correctness or infer causality from uncontrolled comparisons. Preserve sanitized diffs and raw measurements where rights permit.

## Starter task

See `tasks/order-discount.md`. Copy the example to a separate folder, then run from the kit root:

```sh
python benchmarks/evaluate_order_discount.py /path/to/candidate
```

The evaluator runs the candidate suite, the original behavior and import-boundary tests against the candidate, and an external acceptance script. Baseline tests alone are insufficient because a candidate may change them; retain and compare the original tests, and use independent review. The starter evaluator is expected to fail acceptance on the unmodified example; this is not an agent benchmark result.

Record each run in a copy of `run-record.csv` or an equivalent structured record. Do not commit raw logs containing secrets, private prompts or personal data. Keep results separate from the framework's release CI.
