# Public launch checklist — v2.2.1

This package is prepared for publication, not yet published. The owner must authorize publication and confirm rights to all included material, the MIT license and copyright notice. No repository URL, author identity or results are fabricated.

## Before opening the repository
- Inspect the entire package and review any original source rights. Confirm the public project name, license, copyright holder and citation metadata.
- Create a new GitHub repository (prefer initially private for final verification); do not upload your actual application or private project state. Copy the contents of this archive into the repository root, including `.github`, `.gitignore`, and `.gitattributes`.
- Commit on a new branch after reviewing staged files, secret exposure and attribution. Set `main` as default. Enable GitHub Actions and review permissions. Run CI across the entire matrix; do not claim a pass until it runs.
- Review and configure branch rules, required checks, independent review, secret scanning and dependency alerts as available. Mark as a template repository if desired.
- **Before public launch, enable and verify GitHub Private Vulnerability Reporting** under the repository security settings when available. Confirm the private reporting entry point and maintainer notification access. If unavailable, establish a verified private reporting channel, update SECURITY.md, and explicitly record the exception before release; do not solicit vulnerability details in public issues.
- Have an independent reviewer inspect the exact commit, especially installer behavior, executable manifests, policy clarity, security and tests. Resolve blockers.
- Add the actual repository URL to citation and documentation if desired. Verify the README and links on GitHub. After successful review, authorize visibility change and create release tag `v2.2.1` and release notes. Never tag a different revision from the reviewed one.

## Evidence
Local checks are not hosted CI or independent review. Windows/macOS, real agent instruction loading and comparative benchmarks must be verified separately. Record results and any release exceptions explicitly.
