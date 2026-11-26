# Adaptive size, complexity and cohesion policy

## Policy hierarchy

- **Invariant:** correctness, security, domain integrity, authorized contracts, declared architecture and truthful verification. Apply DDD and inward dependencies within the architecture actually adopted, not as a mandate to redesign every small application.
- **Blocking project requirement:** an existing or explicitly approved measurable gate. It remains binding until authorized change or scoped exception. A metric is never blocking merely because this kit, a tool's default, or an AI suggests it.
- **Review heuristic:** evidence to investigate; not a defect verdict. A review may conclude that a larger component is preferable. Document the rationale when a project review-required rule applies.

## Select a profile

| Profile | Default behavior | Appropriate use |
|---|---|---|
| Adaptive (default) | No new numeric blockers; use language-native diagnostics and qualitative review | Most projects |
| Strict | Explicitly approve calibrated blocking checks where they predict actual risk; preserve meaningful exceptions | Teams with established governance and representative baseline data |
| Legacy Modernization | Baseline confirmed issues and approved gate violations; improve selected areas in stages | Existing systems with debt or incomplete tests |

All profiles retain the same architectural, security, behavior-preservation and verification requirements. Profile selection does not override existing gates. Strict is not inherently better; do not switch profiles to bypass a failure.

## Calibrate before enforcing

1. Identify the language, idioms, architecture, runtime, component types, risk and existing tools. Inspect representative healthy and problematic components, including larger cohesive types. Record baseline revision and versions.
2. Prefer meaningful native measures: cognitive/cyclomatic complexity, cohesion (e.g. TCC or LCOM with a specified variant), dependency coupling/fan-out, WMC, API surface, nesting, parameter count, executable statements or source lines. Do not assume metrics from different analyzers are comparable; NCSS and physical LOC are different. A metric may be unavailable or inappropriate for a language. Never fabricate one.
3. Choose project thresholds only where useful. Define analyzer/rule/version, measurement and comparator (`>=` versus `>`), unit, scope, exclusions, severity, mode, baseline and rationale. Separate methods, types, modules and files; do not cap a class by summing a preferred method length. Set thresholds from observed code and maintenance risks, not generic cross-language tables. See STACK_PROFILES.md for tool candidates.
4. Evaluate false positives and false negatives with healthy and problematic examples; verify known allowed/forbidden cases. If a rule is too noisy, propose a scoped adjustment with evidence. Do not silently disable a rule. Record approval before enforcing a new blocker.
5. Integrate approved commands into existing CI and document the gate IDs in QUALITY_GATES.md. Advisory diagnostics can be reported without failing completion. Mandatory assessments may require a documented disposition, not a forced split. Recalibrate after meaningful architecture or tool changes; never rebaseline to conceal a regression.

Modes: **TARGET** (aspirational), **ADVISORY** (inspection signal), **REVIEW_REQUIRED** (record assessment), **BLOCKING** (approved enforceable requirement). Review completion and metric compliance are different. Existing project-specific blockers remain binding even under Adaptive.

## Structural assessment

For a flagged component, inspect responsibility and reasons to change; semantic cohesion of methods/state; ownership of invariants and transaction boundaries; coupling and dependency direction; public interface and consumers; readability and cognitive load; failure paths and testability; frequency and locality of changes if reliable history exists. Check whether an extraction reduces actual complexity or merely moves it into another file. Consider alternatives (retain, simplify, extract a cohesive responsibility, introduce a boundary, improve tests). Compare resulting coupling, behavior, and evidence. Record concrete defects separately from advisory observations. No single numeric score proves quality.

A Java aggregate with many small operations protecting the same state can be healthy even if its physical line count exceeds a small class heuristic. A short service mixing authorization, persistence, billing and UI formatting can be defective despite meeting all length targets. For Go and Rust, assess packages/modules, types/impls and public contracts rather than inventing a class metric. For functional styles, assess functions, effects, modules and composition rather than imposing OO patterns.

Parsers, state machines, numerical algorithms, engines, protocol handlers, generated code, schemas, migrations and framework adapters may require distinct review treatment. Do not automatically exempt authored logic or safety-critical paths. Separate generated/vendor code from authored code; inspect generation inputs and integration risks. Keep related behavior and invariants together.

## Anti-gaming and technical debt

Do not extract arbitrary helpers, forwarding methods or interfaces solely to satisfy metrics; split state ownership, widen visibility or duplicate business rules to reduce local counts; compress formatting or delete documentation; hide authored logic under exclusions; move complexity into tests/configuration; or replace an approved analyzer or baseline to obtain a pass. A raw increase in length or complexity is not automatically a defect. Conversely, justified growth does not override an existing blocking requirement. Seek authorized disposition when necessary. Ratchet confirmed debt and approved gate violations in the relevant scope; do not require global legacy rewrites. Record scoped exceptions with owner, approver, justification, risk, mitigation and review/retirement criteria.

## Evidence and limitations

Record the tool's actual result and separate reviewer interpretation. An advisory threshold crossing alone is not a confirmed architecture defect or a blocking review finding. A failure of an approved gate must be reported even if the reviewer considers the code cohesive. Report unmeasured requirements and uncertainty. The kit's profiles are engineering governance choices, not ISO/IEEE mandated numeric thresholds, certification or compliance guarantees. See STANDARDS_ALIGNMENT.md.
