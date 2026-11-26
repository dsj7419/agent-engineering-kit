# Standards alignment and evidence

This kit is informed by recognized engineering guidance. It is not certified, endorsed, or a complete implementation of any ISO/IEC/IEEE standard, and does not claim conformity. Public catalogue descriptions were used for the formal standards, not a clause-by-clause audit of their full normative text. Projects with contractual, regulatory or safety requirements must identify applicable editions and controls, obtain the relevant standards, and establish separate traceability and assurance. No source listed below prescribes this kit's former universal source-size caps.

| Source / edition | Relevance | Kit mechanism / evidence |
|---|---|---|
| [IEEE Computer Society SWEBOK v4](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | Engineering knowledge across requirements, design, construction, testing, maintenance and quality | Constitution, scoped plans, reviews, verification and handoffs |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Product quality model | Project quality attributes, measurable acceptance criteria, risk-based assessment; no aggregate numeric quality score |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | Software life cycle processes | Authorized scope, staged work, evidence, configuration/change management and maintenance |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Architecture description | Stakeholders, concerns, viewpoints, decisions, boundary maps, architecture evidence |
| [NIST SP 800-218 SSDF v1.1 (final)](https://csrc.nist.gov/pubs/sp/800/218/final) | Secure development lifecycle | Threat modeling, protected development, dependency review, secure implementation, verification and vulnerability response |
| [OWASP ASVS 5.0.0](https://owasp.org/projects/asvs/) | Web application security verification | Select applicable versioned requirements and verification evidence in project security records; not a blanket checklist for all software |
| [Google code review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Design, functionality, complexity, testing, naming and documentation | Independent review and actual risk assessment; avoid overengineering |
| [Martin Fowler, Refactoring](https://martinfowler.com/books/refactoring.html) | Behavior-preserving structural changes | Characterization tests, incremental refactoring and contract preservation |
| [PMD Java design rules](https://pmd.github.io/pmd/pmd_rules_java_design.html), [Checkstyle MethodLength](https://checkstyle.org/checks/sizes/methodlength.html) | Configurable structural diagnostics | Tool-specific calibration; PMD combines measures for GodClass and uses NCSS for size; Checkstyle length is configurable and has different counting semantics |

## Apply to projects

Record stakeholder concerns and quality attributes with acceptance criteria, risk and verification evidence. Consider functional suitability, performance efficiency, compatibility, interaction/accessibility, reliability, security, maintainability, flexibility and safety where relevant. Tailor to system context and applicable obligations. Document non-applicability; do not imply all attributes have been tested because the kit was installed. For regulated/safety-critical systems obtain qualified domain review and independent assurance as required. Security response and operations remain ongoing responsibilities after delivery.

Sources checked 2026-11-25; verify editions and applicability before making contractual claims. The profile modes, audit formats and approval workflow are the kit's own recommendations.
