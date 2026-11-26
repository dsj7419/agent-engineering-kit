# Local release verification — 2.2.1

## Windows remediation verification — 2026-11-26

Environment: Windows, CPython 3.14.4, Temurin JDK 25.0.5 (compiled for Java 17), Windows PowerShell 5.1.26100.9711, PowerShell 7.6.9, actionlint 1.7.12. Commands ran from the kit root. Temporary files were isolated outside the source tree; `PYTHONDONTWRITEBYTECODE=1` prevented source-tree caches. The sandbox's default temporary directory denied writes, so `TEMP` and `TMP` were redirected to a writable disposable directory.

| Exact command | Exit | Observed result |
|---|---|---|
| `python tools/release/check_release.py` | 0 | 34 tests discovered: 33 passed, 1 skipped because this host could not create symbolic links. Includes 10 runner, 8 installer, 6 policy/packaging, 3 PowerShell-wrapper and 7 Python-example tests; syntax and portable-payload checks passed. |
| `python tools/release/check_java_example.py` | 0 | Four scenarios passed; `javac --release 17 -Xlint:all -Werror`, executed with JDK 25. This is not evidence of execution on a Java 17 runtime. |
| `actionlint .github/workflows/ci.yml` | 0 | Workflow lint passed. |
| `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\INSTALL.ps1 -Target $target -WithTools` | 0 | Windows PowerShell 5.1 preview on the normal PATH; target remained empty. |
| `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\INSTALL.ps1 -Target $target -WithTools -Apply` | 0 | All 29 expected files matched source bytes and paths. |
| `pwsh.exe -NoProfile -ExecutionPolicy Bypass -File .\INSTALL.ps1 -Target $target -WithTools` | 0 | PowerShell 7 preview on the normal PATH; target remained empty. |
| `pwsh.exe -NoProfile -ExecutionPolicy Bypass -File .\INSTALL.ps1 -Target $target -WithTools -Apply` | 0 | All 29 expected files matched source bytes and paths. |

Each `$target` was a newly created disposable directory with spaces in its path, removed after verification. Execution-policy bypass applied only to the test process; no persistent PowerShell policy or PATH was changed. Without that process option, this host's Restricted policy blocks scripts; README documents the direct Python alternative.

The three new wrapper regressions were first run against the original installer: exit 1 with failures in both shells. After remediation, they passed in both shells. They exercise multiple PATH applications with an unusable first candidate, no usable Python, preview/apply content, and preservation of installer conflict exit code 2 and existing files.

Verified source snapshot: SHA-256 `4caf5077c719fcd834bf038f1c97f32aa96ed951fe664d1125674acff9d9e49c`, calculated from case-sensitive lexicographically sorted repository-relative POSIX paths and SHA-256 file hashes (`path<TAB>hash<LF>`), excluding this report and Git metadata. The source had no Git history at local verification time. This report was updated afterward; hosted run evidence must identify the committed SHA separately.

At this local checkpoint, hosted CI and independent commit review remain pending. The configured hosted checks cover Linux, Windows and macOS with Python 3.11/3.13, both Windows shells, and a separate explicit Temurin Java 17 job. Owner approval covers local remediation and private repository setup only; public visibility and tag/release publication require a separate final approval. The owner confirmed MIT distribution rights and retained the contributor attribution. Portable `docs/state/` files remain uninitialized templates, not records of this kit's release process.

## Historical Linux verification supplied with the package

The following is the previous package's recorded evidence, not a rerun of the remediated snapshot. Environment: Linux, CPython 3.13.5, JDK 21.0.12.1 (compiled for Java 17). No hosted workflow or release publication was claimed by that record.

| Check | Outcome |
|---|---|
| `python tools/release/check_release.py` | PASS: 10 runner, 8 installer, 6 policy packaging/metadata and 7 Python example tests (31 total); Python syntax and portable payload checks |
| `python tools/release/check_java_example.py` | PASS: Java 17 target compilation with `-Xlint:all -Werror`; 4 behavioral scenarios |
| Bash installer syntax, preview and application in temporary target | PASS: preview wrote nothing, quality-gate template and kit license installed |
| Missing required source / unexpected source files | PASS: missing source blocks installation before writes; unlisted files excluded |
| Bootstrap document references and guardrail markers | PASS: textual regression checks, not evidence of model instruction following |
| Benchmark evaluator against unchanged starter | Expected rejection: candidate suite=0, original checks=0, acceptance=1 |
| Benchmark evaluator against temporary reference discount implementation | PASS: all three exit codes=0; evaluator validation, not an agent experiment |
| Workflow/dependabot/citation YAML parsing | PASS: syntax only, not full schema validation or hosted execution |
| Windows PowerShell, macOS, other Python versions | NOT_RUN: environments unavailable locally; hosted matrix still pending |
| Independent review of v2.2.1, real agent instruction loading, fast-path token savings | NOT_RUN: require independent execution and measurement |
| Comparative agent benchmarks | NOT_RUN: protocol and starter task only |
| Formal ISO/IEEE conformity assessment | NOT_RUN: public catalogue scope descriptions used; no normative clause audit, certification or claim of conformity |

Installer conflict preflight is not an atomic transaction: I/O errors may leave partial new files, and concurrent filesystem mutation is not supported. The installer and gate runner are not security sandboxes. The release owner must confirm licensing/distribution rights, hosted CI, repository settings and independent review before publication. No target-project thresholds or gates are preapproved. See RELEASE_CHECKLIST.md and docs/engineering/STANDARDS_ALIGNMENT.md.
