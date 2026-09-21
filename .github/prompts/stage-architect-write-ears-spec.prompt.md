---
name: "write-ears-spec"
description: "Writes confirmed EARS requirements in spec.md using SDD/TDD skills and scoped instructions, with source traceability and planned acceptance checks."
argument-hint: "feature=NNN-feature-name rules=01-archaeology/business-rules-catalog.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /write-ears-spec

## Objective

Turn only confirmed Stage 1 rules into formal EARS requirements in `specs/<NNN>-<feature>/spec.md`. Open questions remain questions; do not fill in requirements, criteria, or architecture through assumptions.

## When to Invoke

At the start of Stage 2, after Pair 2 selects the narrow feature and completes the H1 handoff. Work on `spec/<NNN>-<feature>`, branched from `develop`.

> [!NOTE]
> Do not use this prompt to explore legacy code, catalog questions (`/catalog-mysteries`), or design modules (`/design-modular-monolith`). Record only requirements backed by confirmed evidence.

## Preconditions

- `01-archaeology/business-rules-catalog.md` contains the evidence
- The team has identified `specs/<NNN>-<feature>/`
- The team has read each cited legacy source

## Inputs the Team Must Provide

- `feature=<NNN>-<feature-name>`
- `rules=01-archaeology/business-rules-catalog.md`
- The subset of **Confirmed** rules belonging to the feature
- A confirmed `[GREENFIELD]` justification for capabilities without a legacy equivalent

## What I Will Do

- Load SDD/TDD and the applicable instructions before authoring; use `Requirements` then `Validation`, applying TDD only to acceptance planning
- Confirm scope and record deferred work in `02-modern-spec/scope-decisions.md`
- Validate the `.NSP`, `.NSN`, `.NSC`, `.NSA`, `.NSL`, `.jcl`, or `.ddm` source
- Preserve existing REQ-IDs and assign unique IDs to new requirements, with `source_legacy:`, paths, and lines; use `[GREENFIELD]` only with a supplied justification
- Record the EARS pattern, `SRC-###` source, justified priority, behavior rationale, status, and planned verification method according to the skill's contract
- Record Given/When/Then only when supported by evidence or a scope decision
- Preserve unvalidated questions from `mysteries-found.md`, including every field
- Maintain a traceability matrix and apply `Validation` before delivery

## What I Will NOT Do

- Create a requirement without `source_legacy:` or a justified `[GREENFIELD]` designation
- Promote, answer, or change the status of hypotheses and questions
- Require a fixed number of requirements, C4 diagrams, ADRs, or endpoints
- Implicitly migrate `specs/` to `.specs/`, change the `REQ-NNN` scheme, or generate a `Full SDD` package for this requirements request
- Put canonical feature specifications, plans, or tasks in `02-modern-spec/`
- Invent SIFAP business facts
- Write executable tests, product code, or commits, or report a planned check as an observed TDD result

## Output Format

```markdown
### REQ-007 - Short imperative behavior title

IF <confirmed unwanted condition>, THEN the system SHALL <one observable response>.

- EARS pattern: Unwanted
- Priority: <P0 | P1 | P2 | P3, with rationale based on confirmed scope>
- Status: Proposed
- Source: SRC-001
- Rationale: <reason supported by the confirmed rule>
- source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN#L<start>-L<end>
- Planned verification: <test, inspection, analysis, demonstration, or measurement; expected evidence>
- AC-REQ-007-01 - Acceptance (Given/When/Then):
  - Given <evidenced precondition>
  - When <trigger>
  - Then <observable, testable outcome>
```

Keep the source register and traceability matrix in the same `spec.md`:

| SRC-ID | Source type | Primary evidence | Confirmed rule |
|---|---|---|---|
| SRC-001 | Legacy | `<full program path>#L<start>-L<end>` | Rule 4 |

| REQ-ID | EARS Pattern | source_legacy | Source Rule | Source File | SRC-ID | AC-ID |
|---|---|---|---|---|---|---|
| REQ-007 | Unwanted | `<PROGRAM>.NSN#L<start>-L<end>` | Rule 4 | `business-rules-catalog.md` | SRC-001 | AC-REQ-007-01 |

## Rules for SDD and Traceability

- SDD instructions apply to `specs/**`; read them explicitly before authoring so their evidence, EARS atomicity, traceability, and status rules govern the whole task.
- Preserve `specs/<NNN>-<feature>/spec.md` and the `REQ-NNN` scheme. Do not create a parallel artifact tree or impose files outside the requested scope.
- Use `SHALL` in normative clauses as defined by the skill. Preserve meaning and IDs when normalizing existing requirements. `SRC-###` supplements but never replaces `source_legacy:`.
- Do not invent priorities, metrics, approvals, or test results to complete the template. Unevidenced fields remain `PENDING` or `BLOCKED`, with an impact and owner; do not present blocked requirements as ready.
- Load only resources needed by the selected mode. Do not assume generators or validators named by the skill exist or cover this repository's artifacts; record unexecuted checks and the reason.
- Apply the `SDD Workflow` section of the [architect agent](../agents/architect.agent.md) directly. Keep test planning in the requirement's verification field; do not create `tasks.md` or a parallel FRD/NFRD unless requested. Use the SDD skill's output template for the final report.

## Definition of Done

- [ ] SDD/TDD and applicable instructions were loaded and applied in `Requirements` and `Validation`, with TDD limited to planned acceptance checks
- [ ] `spec.md` contains only requirements for the feature
- [ ] Each requirement has an observable EARS response using `SHALL`, the skill's metadata, a stable acceptance ID, and valid `source_legacy:` or a justified `[GREENFIELD]` designation
- [ ] Open questions remain outside requirements and retain their status
- [ ] The matrix links each REQ-ID to the reviewed evidence
- [ ] Test-verifiable acceptance criteria identify the planned behavior check and expected evidence; other verification methods have an explicit applicability rationale
- [ ] Applicable gates and blockers are recorded; the specification remains `Draft` or `Ready for review` until explicit human approval

## Prompt Body

You are `@architect`. Promote confirmed Stage 1 rules to formal EARS requirements without inventing evidence.

**Step 0 - Load SDD, TDD, and instructions.**
Before reading feature inputs or authoring, explicitly read [SDD artifact instructions](../instructions/sdd-artifacts.instructions.md) and load [sdd-requirements-engineer](../skills/sdd-requirements-engineer/SKILL.md) and [tdd-workflow](../skills/tdd-workflow/SKILL.md). If skill loading is unavailable, read each `SKILL.md` directly. Read [test instructions](../instructions/tests.instructions.md) for acceptance planning and [Natural/Adabas instructions](../instructions/natural-adabas.instructions.md) before legacy sources. Select `Requirements` and read the [EARS reference](../skills/sdd-requirements-engineer/references/ears-notation.md) and [quality gates](../skills/sdd-requirements-engineer/references/quality-gates.md); apply the repository contract above.

**Step 1 - Confirm scope.**
List only **Confirmed** entries that the team assigned to the feature. Record deferred work in `scope-decisions.md`. Do not include **Inferred** or **Mystery** entries.

**Step 2 - Validate each source.**
Open each cited member and confirm the lines. If the reference is invalid, return the rule as an open question. Never cite `.NSD`; no such file exists in the corpus.
Associate each primary source with a stable `SRC-###` and the confirmed rule, retaining the full path in `source_legacy:`.

**Step 3 - Write the EARS requirement.**
Preserve existing IDs and assign a unique `REQ-NNN` to each new requirement. Apply the SDD skill's requirement contract and EARS reference: exactly one classification and one observable response using `SHALL`. Do not maintain a competing set of EARS templates in this prompt.

Attach `source_legacy:`. For new capabilities, use `[GREENFIELD]` followed only by the justification supplied by the team.
Populate the remaining template fields from evidence and keep gaps explicit. A non-functional target is normative only when its metric, workload, observation window, environment, and owner are defined.

**Step 4 - Record acceptance criteria.**
Add Given/When/Then only for evidenced behavior. Preserve existing acceptance IDs and use `AC-REQ-NNN-NN` for new criteria. For each test-verifiable criterion, apply TDD to identify the smallest behavior-scoped check, its input or precondition, why it should fail before implementation, and its expected passing outcome. Keep all of this as planned verification in `spec.md`, not executable test code or execution evidence. For inspection, analysis, demonstration, or measurement, retain the appropriate method and mark the TDD cycle `NOT APPLICABLE` with a reason where needed.

**Step 5 - Preserve open questions.**
Copy unvalidated items to "Open questions", preserving `path:line` evidence, impact, unconfirmed hypothesis, owner, and status. Do not answer or change them.

**Step 6 - Build the matrix.**
Maintain the `REQ-ID | EARS Pattern | source_legacy | Source Rule | Source File | SRC-ID | AC-ID` table and the source register. Check bidirectional links between rules, sources, requirements, and acceptance.

**Step 7 - Validate and write.**
Apply `Validation` to the relevant requirement and traceability gates. Record each result as `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE`, with evidence or a reason. Verify that any named validator exists and covers this artifact. With read/search/edit only, report commands as not executed and list the applicable checks for the team. Save `specs/<NNN>-<feature>/spec.md` as `Draft` or `Ready for review`; approval and implementation readiness are separate, evidenced decisions. Do not expand scope to complete the report.

## Example Invocation

```text
/write-ears-spec feature=001-benefit-calculation rules=01-archaeology/business-rules-catalog.md
```

Expect a `spec.md` with evidence-backed EARS requirements, `source_legacy:`, a traceability matrix, and preserved open questions.
