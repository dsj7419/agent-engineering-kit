# System Architecture — Project Template

Status: UNKNOWN / not yet inspected. Replace placeholders using repository evidence; do not impose an unapproved redesign.

## System overview
- Purpose, stack/version, deployment model, source roots, architecture diagram:
- Existing architecture and known constraints:
- Relevant ADRs and evidence (paths):
- Stakeholders, concerns, views/viewpoints and rationale as appropriate to project risk:

## Bounded contexts and ownership
| Context/module | Responsibility and reason to change | Owned rules/state | Public API | Internal paths | Consumers |
|---|---|---|---|---|---|
| TBD | | | | | |

## Dependency contracts
Map actual paths to layers; document approved shared/domain-safe libraries and exceptions. Typical source dependency model (adapt to actual design):
- Domain: domain-safe code only; no application, presentation, persistence, network or framework dependencies.
- Application: domain and owned ports; no concrete adapters or presentation.
- Infrastructure: implements inward ports; owns DB/HTTP/filesystem/external SDKs.
- Presentation: invokes application contracts; no direct persistence or adapter access.
- Composition root: explicitly wires concrete adapters to ports and creates use cases; no business decisions.
- Cross-context access: public contracts only; state belongs to its owning context. No package/module cycles.

| From actual path | Allowed targets | Forbidden targets | Enforcement command/rule | Exceptions |
|---|---|---|---|---|
| TBD | | | | |

## Critical execution paths
Describe entry -> application -> domain; where I/O is needed, application/domain-safe port -> adapter at runtime. Record source vs runtime dependency direction, transaction and concurrency boundaries, failure/retry behavior, authorization and public contracts.

## State, integration and nonfunctional constraints
- Sources of truth, invariants, state lifecycle, synchronization:
- External contracts, data schemas, event semantics, compatibility:
- Quality attributes, measurable acceptance criteria, performance budgets, reliability objectives, security/safety, interoperability, accessibility and operational constraints where applicable:
- Known dependency violations and debt IDs:
