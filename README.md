# Agent Engineering Kit — v2.2.1

A portable, language-agnostic engineering governance kit for Claude Code, Codex, Gemini CLI and other repository-aware agents. Includes SOLID/SRP, DDD, modular engineering, safe refactoring, audit coverage, independent review, revision-aware handoff and optional executable quality-gate orchestration.

## Quick start

**Architecture governance for autonomous coding agents.** Use the same standards across Claude Code, Codex and Gemini CLI. This is a policy and verification kit, not an agent orchestrator. No API credentials or paid service are required by the kit itself.

The installer and optional tools require Python 3.9+ (use a supported Python release for new installations); the documentation does not. No package installation is required.

**1. Preview. 2. Apply only after reviewing the preview. 3. Open your agent in the target project and use the initial setup prompt.**

Clone the kit into a directory separate from your target project (or download and extract its ZIP):

```sh
git clone https://github.com/dsj7419/agent-engineering-kit.git
cd agent-engineering-kit
```

The repository must be accessible to your GitHub account while it is private. Template mode is off for v2.2.1; use the installer to import the portable files without copying the kit's release infrastructure or examples.

For a new project, first create an empty directory outside the kit:

```powershell
# Windows; choose your own project location.
New-Item -ItemType Directory -Path 'C:\path\to\my-project'
```

```sh
# Linux/macOS; choose your own project location.
mkdir -p /path/to/my-project
```

From the cloned or extracted kit directory, substitute your new or existing project path:

Windows PowerShell:

```powershell
.\INSTALL.ps1 -Target 'C:\path\to\project' -WithTools
.\INSTALL.ps1 -Target 'C:\path\to\project' -WithTools -Apply
```

If your PowerShell execution policy blocks scripts, use the Python alternative below. The wrapper supports Windows PowerShell 5.1 and PowerShell 7, skips Windows Store execution aliases, and selects the first working Python 3.9+ application on PATH.

Linux/macOS:

```sh
bash install.sh --target /path/to/project --with-tools
bash install.sh --target /path/to/project --with-tools --apply
```

Portable alternative: `python tools/release/install_kit.py --target /path/to/project --with-tools` (add `--apply` after reviewing). Preview is the default. Identical files are skipped; conflicting files cause an abort before writes. The installer never overwrites a project's existing files. Merge conflicts manually, especially when upgrading from earlier versions. Back up or commit your work first, use a stable local directory with no concurrent writers, and review the diff afterward. An I/O error during application may leave partial new files; no automatic rollback is attempted. The installer is not a filesystem sandbox. It does not install dependencies, configure target CI, or copy public-repository metadata. A copy of the kit license is installed as `docs/engineering/KIT-LICENSE.txt`.

For first use, tell your agent: **“Read AGENTS.md, use the full HANDOFF bootstrap, and inspect the project read-only. Propose project setup and exact verification commands.”** Once initialized, routine low-risk tasks can use the shorter fast path. Unknown context, significant changes and specialized reviews still require the full path.

## Installation (manual / existing projects)

Upgrading an existing kit installation? See [upgrade and migration guidance](docs/engineering/UPGRADING.md).

1. Extract the ZIP into a temporary folder. Copy `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `docs/` and optionally `tools/engineering/` into your project root; retain the kit license as `docs/engineering/KIT-LICENSE.txt` without replacing your project license. **Merge, do not blindly overwrite** existing agent instructions, project state, ADRs, or tools. Keep your project's README; this README is the kit's setup guide. Review the resulting diff before use.
2. Open your coding agent from the project root. Use the bootstrap prompt below. It should inspect the repository and existing changes before proposing updates. Existing architecture and requirements remain authoritative; no migration or redesign is implied.
3. Authorize only the appropriate project-document updates. Fill `docs/state/ARCHITECTURE.md`, `CURRENT_STATE.md`, and `QUALITY_GATES.md` from verified repository evidence; calibrate `METRICS_PROFILE.md` if project metrics are needed. Complete domain/security/debt templates as applicable. Do not leave unknowns disguised as successful verification.
4. Configure actual gates using existing project tooling. Optionally copy `docs/state/quality-gates.example.json` to `quality-gates.json`, set `configured` to true only after review, and enter approved gates. See `tools/engineering/README.md` for format and examples. Integrate the verified commands into existing CI and protected review when appropriate.
5. Confirm agent instruction loading. Codex uses AGENTS.md; Claude Code and Gemini CLI use their respective Markdown wrappers with `@AGENTS.md`. Trust/configuration and local instructions can affect discovery. If needed, explicitly request the agent read AGENTS.md. Instructions are not guaranteed compliance or a security sandbox.

## Bootstrap: less context, same engineering rules

| Task | Documents to load |
|---|---|
| Localized low-risk implementation or hotfix in an initialized repository | AGENTS.md, current state, quality gates, applicable local policies and relevant code/tests |
| First use, takeover, uncertain context, Levels 2–3, structural refactoring, audit, independent review, architecture proposal or handoff | Full six-document bootstrap in AGENTS.md plus applicable protocols and project records |

Fast path never bypasses required checks or permissions. Escalate if scope or risk changes. The initial setup and state configuration take longer than the install commands.

## Copy/paste prompts

**Initial setup / takeover (read-only):**
> Read AGENTS.md and all required bootstrap documents. Enter HANDOFF mode. Inspect this repository and its actual Git state, architecture, active work, tests and quality gates. Do not modify files yet. Report verified facts, unknowns, existing violations, proposed project-specific documentation and exact verification commands, risks and safe continuation point. Ask for authorization before protected changes.

**Populate project state (after reviewing proposal):**
> Implement the approved documentation and quality-gate configuration only. Preserve existing project records, code and user changes. Do not install new tooling or change CI without approval. Record actual verification evidence and remaining gaps.

**Everyday coding:**
> Follow AGENTS.md in IMPLEMENT mode. Implement [task] with acceptance criteria [criteria]. Preserve unrelated behavior and changes, use the appropriate risk level and report actual verification results.

**Deep audit:**
> Follow AGENTS.md and AUDIT_PROTOCOL.md in AUDIT mode for [scope]. Stay read-only. Enumerate in-scope files and symbols, assess architecture, correctness, security, concurrency, performance and tests, and report actual coverage, prioritized findings and a staged roadmap. Do not refactor until authorized. Report in chat unless artifact writes are approved.

**Refactor:**
> Follow REFACTORING_PROTOCOL.md for [approved scope]. Preserve observable behavior, establish baseline and characterization tests, stage cohesive changes, run required checks and record remaining risks. Do not expand scope.

**Independent review:**
> In REVIEW mode, independently inspect [base -> target snapshot] against [requirements]. Follow REVIEW_PROTOCOL.md. Do not edit files. Report evidence-based findings and approval outcome for this exact snapshot.

## Structure

- `AGENTS.md` — canonical shared entry point; `CLAUDE.md` and `GEMINI.md` are thin imports.
- `docs/engineering/` — constitution, agent workflow, audit, review, refactoring, adaptive metrics, standards alignment and stack profiles; version-control these standards and require approval for changes.
- `docs/state/` — project-specific architecture, domain model, security, quality gates, debt, current state, metrics profile, and ADR/plan/audit/review templates. Copy task templates to uniquely named files when authorized.
- `tools/engineering/` — optional Python standard-library runner and self-tests, no external dependencies. It does not install or configure application analyzers.
- `CHANGELOG.md`, `REFERENCES.md` — changes and supporting resources.

## Scope and limitations

The kit is complete as a reusable template, not configured or tested against your application. Adaptive is the default: no universal numeric size or complexity caps. Existing approved gates remain binding. Select and calibrate a project profile using `docs/state/METRICS_PROFILE.md` and `docs/engineering/METRICS_POLICY.md`. See `docs/engineering/STANDARDS_ALIGNMENT.md` for the standards crosswalk and its limitations. Actual tooling, architecture checks, CI, acceptance criteria and approval rules must be tailored to your project. The optional runner checks command outcomes; it is not a security sandbox, architecture analyzer, or multi-agent orchestrator. Keep one writer per worktree and require independent review for high-risk changes. Never assume a passing test suite proves correctness.

## Examples, verification and publication

- [Runnable Python order example](examples/python-order/README.md): domain invariants, a persistence port, composition root, behavior and architecture tests.
- [Runnable Java order aggregate](examples/java-order/README.md): cohesive state and invariants without arbitrary type-size caps. Run `python tools/release/check_java_example.py` with a Java 17+ JDK.
- [Benchmark protocol](benchmarks/README.md): one starter task, acceptance evaluator and recording template; no comparative agent results yet.
- Run `python tools/release/check_release.py` to verify the kit itself. GitHub Actions runs the same checks on Linux, Windows and macOS with Python 3.11 and 3.13, including Windows PowerShell 5.1 and PowerShell 7 installer smoke tests. A separate Linux job verifies the Java example with an explicitly selected Java 17 JDK. These workflows are not target-project CI.
- [Contribution guide](CONTRIBUTING.md), [security policy](SECURITY.md), [code of conduct](CODE_OF_CONDUCT.md), [roadmap](ROADMAP.md) and [public launch checklist](RELEASE_CHECKLIST.md).
- [MIT license](LICENSE) and citation metadata (`CITATION.cff`). The release owner must confirm distribution rights before public launch.

No claim of superiority, production validation or guaranteed agent compliance is made. Verify with your stack and agent versions before relying on the kit.
