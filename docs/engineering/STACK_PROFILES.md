# Stack Profiles and Automated Enforcement

This is a menu of candidate tools, not a list of commands to run blindly. Inspect installed versions, manifests, existing CI and repository conventions first. Select actual commands in `../state/QUALITY_GATES.md` and optionally the runner configuration. Do not install, upgrade or enable new blocking policies without authorization; baseline legacy violations first. Commands below are examples, not verified project commands.

| Stack | Build/type/lint/test candidates | Architecture and metrics | Security/performance |
|---|---|---|---|
| TypeScript/JavaScript, Node, React, Next.js | Existing npm/pnpm/yarn scripts; `tsc --noEmit`; ESLint/Biome; Vitest/Jest; Playwright | dependency-cruiser, Madge, Knip; ESLint complexity, max-lines-per-function, max-depth, max-params, max-lines | package-manager audit, Semgrep, Gitleaks, Stryker, application profiling |
| Go | `go build ./...`, `go vet ./...`, `go test ./...`; golangci-lint | depguard, package architecture tests; gocyclo, gocognit, funlen, errcheck | `go test -race ./...` for concurrent code on supported platforms; govulncheck, gosec; `go test -bench=. -benchmem ./...` for relevant workloads |
| Python | pytest; Ruff check and format --check; mypy or Pyright | Import Linter (`lint-imports` after configuration), Radon, Vulture; Ruff C901 and relevant PLR rules | Bandit, pip-audit, mutmut, profiling |
| C#/.NET | `dotnet build`, `dotnet test`, `dotnet format --verify-no-changes`; Roslyn analyzers | ArchUnitNET/NetArchTest, configured analyzers and .editorconfig | package vulnerability listing (syntax depends on SDK), benchmarking, security scanners |
| C++ | Configured CMake/Ninja/MSVC; CTest, GoogleTest/Catch2; clang-tidy, clang-format, cppcheck | CMake target dependency rules, include dependency analysis, compiler/static analyzer metrics | ASan, UBSan, TSan in compatible separate configurations; profiling and benchmarks |
| Java/Kotlin | Existing Maven/Gradle wrappers, JUnit, static analysis | ArchUnit, Checkstyle, PMD, Detekt, Sonar | dependency scanning, PIT, JMH |
| Rust | Existing Cargo profiles; cargo check/test/clippy/fmt --check | crate/module boundaries, visibility, dependency graph checks | cargo audit/deny, Miri where appropriate, Criterion |

Cross-stack options: CodeQL/Semgrep for supported security analysis, OSV-Scanner/Trivy for supported dependency scanning, Gitleaks for secrets, jscpd for duplication, Sonar for cognitive complexity where supported. Dead-code and duplication findings are leads, not automatic deletion instructions. Verify dynamic usage and cross-domain semantics.

## Language-aware metric selection

Use METRICS_POLICY.md to calibrate metrics; this table suggests diagnostic dimensions, not mandatory thresholds. Java and C# classes often contain constructors, properties, overloads and cohesive lifecycle operations. Kotlin and Rust may use extensions or impl blocks. Go packages and functional modules require different boundaries. Prefer analyzer-specific rule semantics over cross-language LOC comparisons.

| Language | Useful structural signals (when supported) |
|---|---|
| Java | PMD GodClass (WMC, ATFD, TCC), cognitive/cyclomatic complexity, NCSS; Checkstyle method length, coupling and parameters; ArchUnit boundaries |
| Kotlin | Detekt complexity, nesting and long methods; package/feature cohesion |
| C# | Roslyn analyzers, coupling, complexity, public surface and namespace/assembly boundaries |
| Python | Radon complexity, Ruff rules, module cohesion, imports and effects |
| JS/TS | ESLint complexity and nesting, module dependency fan-out, exported API and rendering/state boundaries |
| Go | Package coupling, exported surface, complexity, error and concurrency handling |
| Rust | Clippy complexity-related lints, crate/module visibility, ownership and public API |
| C/C++ | clang-tidy complexity-related rules, include/target dependencies, ownership and resource lifecycle |
| Other languages | Use established native tools, actual idioms and project requirements; do not fabricate metrics |

For example, Checkstyle MethodLength has a configurable default maximum of 150 lines (including empty/comment lines by default), while PMD uses non-commenting source statements for NCSS and combines weighted method count, foreign data access and cohesion for GodClass. These are tool behaviors, not endorsed limits. Verify the installed version; choose a project rule only after calibration. Do not equate physical LOC and NCSS or treat an analyzer default as a new mandatory gate.

## Architecture enforcement recipe

1. Map actual source roots, bounded contexts, public entry points, composition root and approved domain-safe libraries in `../state/ARCHITECTURE.md`.
2. Configure language-native import/package/target checks. In a typical layered context, forbid domain -> application/presentation/infrastructure and application -> concrete infrastructure/presentation; forbid presentation -> concrete infrastructure; allow the composition root to wire outer implementations. Restrict direct cross-context internal imports and cycles. Adapt to real project structure; directory names alone do not establish responsibility.
3. Add positive and negative architecture fixtures or tests (known permitted and forbidden edges) to verify the rules actually work. Record any unavoidable legacy edges as scoped exceptions with owner, baseline and review date.
4. Add exact commands to project gates and existing CI. Configure approved metric rules with explicit counting semantics, calibrated thresholds, and a debt ratchet for confirmed defects or approved violations. Do not assume generic tools measure every policy metric; document unmeasured rules and manual review.
5. Protect quality-gate and architecture rule changes in code review/branch protection. Treat passing tools as evidence for their limited checks, not proof of SRP, correctness or security.

No universal tool automatically enforces all engineering principles. The included runner executes approved commands and records outcomes; it does not itself analyze application architecture.
