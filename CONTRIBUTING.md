# Contributing

Use a focused issue or pull request. Explain the problem, affected users, acceptance criteria and any policy trade-offs. For policy changes, provide a concrete example of failure or ambiguity and why the change improves engineering outcomes. Do not turn style preferences into mandatory architecture rules without justification.

Follow [AGENTS.md](AGENTS.md). Preserve unrelated work, use small diffs, add regression tests for tooling defects and update relevant documentation. Run `python tools/release/check_release.py` from the repository root. Report the actual environment and results, including skipped checks. Do not claim benchmark improvements without reproducible evidence.

AI-assisted contributions are welcome; contributors remain responsible for reviewing code, licensing, attribution, secrets and correctness. Disclose material AI assistance and verification limitations in the PR. Do not submit third-party proprietary source or private project data. Contributions are submitted under the repository license; confirm you have the rights to submit them.

Maintainers should independently review security-sensitive changes, installer behavior, command execution and policy changes. Passing CI is necessary but not proof of correctness. Do not merge unresolved critical/high findings. See [SECURITY.md](SECURITY.md) for private vulnerability reporting.
