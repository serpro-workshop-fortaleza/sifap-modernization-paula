---
name: "create-constitution"
description: "Write .specify/memory/constitution.md with the feature's numbered, testable, nonnegotiable rules."
argument-hint: "feature=NNN-feature-name"
agent: "enterprise-architect"
tools: ["read", "search", "edit"]
---
# /create-constitution

## Objective

Produce `.specify/memory/constitution.md`: a short (≤ 80 lines), numbered set of testable, nonnegotiable rules grouped by category. Each rule includes the consequence of a violation and a mutable or immutable designation. ADRs record decisions. The constitution defines the boundaries those decisions cannot cross.

## When to Invoke

At the start of a feature (or project), before ADRs and specifications depend on shared constraints. Run this prompt again to amend the constitution through the documented process.

## Preconditions

- `specs/<NNN>-<feature>/` exists, or the project scope has been agreed
- Organizational constraints are known (security baseline, Azure-only, OWASP Top 10, and LGPD)
- Any parent constitution to inherit is identified

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>` (or `project`)
- The existing organizational constraints to codify
- Any parent constitution to inherit
- Named approvers (Enterprise Architect, Technical Lead, and the information security team, or InfoSec)
- Ask the user for any missing information.

## What I Will Do

- Inherit the parent constitution and tailor it with an explicit justification
- Group rules into Stack, Security, Data, Operations, Process, and Compliance
- Make each rule testable and assign an ID (`C1`, `C2`, …)
- State the consequence of violating each rule
- Mark each rule as mutable (can be relaxed by an ADR with InfoSec approval) or immutable
- Record the date, apply semantic versioning (semver), and identify approvers
- Keep the file to at most 80 lines

## What I Will NOT Do

- Write principles ("we value quality") instead of rules ("Java 21 only")
- Emit a rule without an ID or violation consequence
- Exceed 80 lines. A constitution nobody can remember does not work
- Invent an organizational constraint or an approver. I will ask the team
- Decide a specific design choice. That decision must be recorded in an ADR through `/create-adr`

## Output Format

The deliverable is `.specify/memory/constitution.md`:

```markdown
# CONSTITUTION: 001-pagamento-beneficio

- **Version**: 1.0.0
- **Date**: 2026-04-29
- **Approvers**: @paula (Enterprise Architect), @morgan (Technical Lead), @infosec-lead
- **Scope**: rules applicable to this feature

## 1. Stack
| ID | Rule | Consequence |
|---|---|---|
| C1 | The backend runs only on Java 21 (Temurin) and Spring Boot 3.3. | The build fails. |
| C2 | The frontend runs on Next.js 15 with TypeScript `strict: true`. `any` is prohibited. | Static analysis blocks merging. |
| C3 | PostgreSQL 16 is the only system of record for SIFAP data. | Requires an InfoSec exception. |

## 2. Security
| ID | Rule | Consequence |
|---|---|---|
| C4 | Service-to-service authentication uses Azure Managed Identity. Client secrets are prohibited in code and configuration. | The pull request (PR) is blocked. |
| C5 | Secrets are read from Azure Key Vault at runtime. Committing `.env` is prohibited. | Gitleaks blocks merging. |
| C6 | OWASP Top 10 baseline: input validation, parameterized SQL, and no queries built by string concatenation. | The pull request (PR) is rejected. |

## 3. Data
| ID | Rule | Consequence |
|---|---|---|
| C7 | Columns with personally identifiable information (PII) contain a `COMMENT` identifying them as PII. | The database administrator (DBA) review blocks progress. |
| C8 | Production PII is prohibited in `dev` or `stage`. Use synthetic data only. | InfoSec records a finding and requires immediate rollback. |

## 4. Operations
| ID | Rule | Consequence |
|---|---|---|
| C9 | Each public endpoint emits a structured log with `requestId`, `userId`, and `latencyMs`. | Code review blocks progress. |
| C10 | Each user-facing endpoint has a service-level objective (SLO) recorded in a `REQ-OPS-*`. | Specification review blocks progress. |

## 5. Process
| ID | Rule | Consequence |
|---|---|---|
| C11 | Use one branch per work item, created from `develop` with the role prefix defined in `00-GIT-WORKFLOW.md` (`spec/`, `impl/`, `infra/`, `docs/`, `agent/`). Direct commits to `develop` or `main` are prohibited. | The pull request (PR) is rejected. |
| C12 | Each requirement uses EARS notation and each test cites a `REQ-ID`. | Specification review blocks progress. |

## 6. Compliance
| ID | Rule | Consequence |
|---|---|---|
| C13 | LGPD data subject rights endpoints (read, delete, and export) are covered by `REQ-COMP-*`. | Compliance review blocks release. |

## 7. Mutable and immutable
- Mutable (can be relaxed by an ADR with InfoSec approval): C9–C12.
- Immutable (require a constitutional amendment): C1, C3, C4, C5, C6, C7, C8, C13.

## 8. Amendment process
Open a pull request (PR) for this file. The architecture board reviews it and increments the version (`1.0.0` -> `1.1.0` minor, `-> 2.0.0` major). The new approvers record their approval.
```

## Definition of Done

- [ ] The file has ≤ 80 lines, excluding signatures
- [ ] Each rule has an ID and a violation consequence
- [ ] There is at least one rule per category (Stack, Security, Data, Operations, Process, and Compliance)
- [ ] The distinction between mutable and immutable is stated
- [ ] The amendment process is documented
- [ ] The constitution inherits from a parent constitution when one exists
- [ ] Approvers, the date, and a semantic version are recorded

## Prompt Body

You are the Enterprise Architect (`@enterprise-architect`). The team needs to establish boundaries before decisions and code depend on them.

**Step 1: inherit and tailor.**
Start from the project-level constitution. Make it more or less restrictive only for this feature, with an explicit justification.

**Step 2: group rules by category.**
Use Stack, Security, Data, Operations, Process, and Compliance.

**Step 3: make each rule testable.**
"Use Java 21" is testable (`mvnw --version`); "use modern Java" is not.

**Step 4: number the rules.**
Use `C1`, `C2`, … so reviewers can cite them.

**Step 5: state the consequence.**
Use "The build fails", "The pull request is rejected", or "Requires an InfoSec exception". Never omit the consequence.

**Step 6: mark as mutable or immutable.**
Some rules can be relaxed through an ADR with InfoSec approval. Others require a new constitution.

**Step 7: record the date, version, and approvals.**
Record the board date, approvers, and version `1.0.0`. Increment the version only when the constitution itself changes.

Keep only rules, not principles, and limit the file to 80 lines. A specific design choice belongs in an ADR created through `/create-adr`, not a constitutional rule.

## Example Invocation

```text
/create-constitution feature=001-pagamento-beneficio
```
