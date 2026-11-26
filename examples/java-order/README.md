# Java order aggregate — cohesion over arbitrary size

This dependency-free Java 17+ example groups line-item operations, monetary invariants, lifecycle transitions and immutable snapshots in a single aggregate. The class exceeds the former 150-line cap, without padding or unrelated infrastructure. Most methods are small. Splitting solely to satisfy a length rule could expose mutable state, distribute invariants or create forwarding layers. A real project might still extract a value object or pricing policy if independent requirements justify it.

The example uses integer minor units for one caller-defined currency and detects overflow before mutation. It is single-owner, not thread-safe, and has no database, framework, network or UI dependencies. It is educational, not a production ordering system. No claim of measured cohesion, universal optimality or performance is made.

From the kit root, run `python tools/release/check_java_example.py` (requires a JDK, no dependencies). The checker compiles for Java 17 into a temporary directory with warnings treated as errors and executes the four behavioral scenarios. It does not assert a minimum class size: keeping code artificially long would be metric gaming too.

An adaptive review would examine invariants, API surface, dependencies and actual test evidence; a project with an approved blocking size rule would still need authorized disposition. See `../../docs/engineering/METRICS_POLICY.md`.
