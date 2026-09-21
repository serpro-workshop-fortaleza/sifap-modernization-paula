---
name: "generate-adr"
description: "Drafts one traceable architecture decision using SDD/TDD skills and scoped instructions, with alternatives, planned verification, and explicit human approval."
argument-hint: "title=\"Map Adabas MU fields to JSONB vs ElementCollection\""
agent: "architect"
tools: ["read", "search", "edit"]
---
# /generate-adr

## Objective

Create a formal Architecture Decision Record (ADR) for one choice, recording the options, evaluated trade-offs, decision, and consequences.

## When to Invoke

When at least two viable options exist during Stage 2 or later.

## Preconditions

- The team has identified the decision
- At least two options exist; a single option does not require an ADR

## Inputs the Team Must Provide

- Decision title
- At least two options
- Constraints from the EARS specification or bounded contexts

## What I Will Do

- Load SDD/TDD and applicable instructions before analyzing the decision; apply the relevant SDD decision procedure and scoped `Validation` gates
- Structure the decision in MADR format
- List context-specific pros and cons
- Present the analysis for the team's decision
- Record the decision, date, rationale, and positive and negative consequences
- Record source evidence, the accountable decision owner, testability impacts, planned verification, and revisit triggers

## What I Will NOT Do

- Decide for the team
- Write an ADR with only one option
- Use generic trade-offs or invent metrics and benchmarks
- Write executable tests, product code, or commits, or treat a proposed ADR or a planned check as approved or executed

## Output Format

A file at `02-modern-spec/ADRs/adr-NNN-<slug>.md`:

```markdown
# ADR-NNN: <title>

- Status: Proposed
- Date: <YYYY-MM-DD>
- Decision owner: <accountable reviewer>
- Related requirements and acceptance: <existing REQ-ID and AC-ID, or explicit applicability rationale>
- Sources: <SRC-ID and primary evidence>

## Context
## Options considered
### Option 1
### Option 2
## Decision and approval evidence
## Positive and negative consequences
## Planned verification and TDD applicability
## Revisit triggers and open questions
```

See [`02-modern-spec/templates/ADR.template.md`](../../02-modern-spec/templates/ADR.template.md).

## Rules for SDD and TDD

Apply the `SDD Workflow` section of the [architect agent](../agents/architect.agent.md) directly. Keep this supporting ADR in `02-modern-spec/ADRs/` and link canonical requirements from `specs/<NNN>-<feature>/spec.md`; do not invent requirements or generate a parallel package for one decision. The SDD skill owns evidence and lifecycle rules; TDD informs the verification approach, not implementation. Use the SDD skill's output template for the final report.

## Definition of Done

- [ ] The ADR follows MADR and contains every section
- [ ] At least two options have context-specific pros and cons
- [ ] The decision and date are clear
- [ ] Positive and negative consequences are recorded
- [ ] Related REQ-IDs are listed when applicable
- [ ] SDD/TDD and applicable instructions were applied; verification is planned and any TDD non-applicability has a reason
- [ ] Sources, decision owner, revisit triggers, gate results, and blockers are explicit; acceptance requires human approval evidence

## Prompt Body

You are `@architect`. The team needs to document an architecture decision.

**Step 0 - Load SDD, TDD, and instructions.**
Before analysis, explicitly read [SDD artifact instructions](../instructions/sdd-artifacts.instructions.md) and load [sdd-requirements-engineer](../skills/sdd-requirements-engineer/SKILL.md) and [tdd-workflow](../skills/tdd-workflow/SKILL.md). If skill loading is unavailable, read each `SKILL.md` directly. Read [Modular Monolith instructions](../instructions/modular-monolith.instructions.md) and [test instructions](../instructions/tests.instructions.md) for architectural and testability constraints. Read database, security, or other scoped instructions only when the choice concerns that surface; their `applyTo` patterns do not automatically load for this ADR. Read the [SDD quality gates](../skills/sdd-requirements-engineer/references/quality-gates.md) and apply only the decision, evidence, traceability, and readiness checks relevant to `Validation`.

**Step 1 - Clarify the decision.**
Identify the decision, why it is needed now, and the alternatives from the supplied evidence. Ask only for missing facts; do not ask the team to repeat a recorded decision. If only one option is known, ask which alternatives were rejected rather than inventing them.

**Step 2 - Gather context.**
Read the scoped specification, existing decisions, discovery report, and relevant boundary map when present. Follow their primary evidence; link existing REQ-ID, AC-ID, and SRC-ID without fabricating IDs to complete the template. Record missing sources or decisions as `PENDING` or `BLOCKED` with an owner and impact.

**Step 3 - Analyze each option.**
Record a practical description, up to three pros, up to three cons, risk, and relative effort, all specific to the context.

Compare the options' testability using the TDD skill and test instructions. For a choice affecting executable behavior, identify a planned behavior-scoped check linked to the governing acceptance criterion and the evidence expected from a later red-green-refactor cycle. For a non-executable decision, retain inspection or analysis as appropriate and record TDD as `NOT APPLICABLE` with a reason. Do not write or run tests or claim cycle results.

**Step 4 - Present the options and request a decision.**
Present the comparison and request the team's choice and rationale if not already recorded. Distinguish a recommendation from an accepted decision. Retain the approving role, date, and evidence; absence of approval leaves the ADR `Proposed`.

**Step 5 - Document the decision.**
Use the repository ADR template with a stable `ADR-NNN`, current date, context, options, decision or pending choice, consequences, requirement traces, planned verification, and revisit triggers. Keep `Proposed` until explicit human approval; artifact validation alone does not change acceptance status.

**Step 6 - Assign the number and file the ADR.**
When updating an existing ADR, preserve its ID. For a new decision, inspect `02-modern-spec/ADRs/`, use the next available number, and write `adr-NNN-<slug>.md`; create the directory only when needed. Apply scoped `Validation` gates and record `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE` with evidence or reasons. Check that cited validators exist and apply; with read/search/edit only, report commands as not executed and list applicable checks for the team. Do not claim implementation readiness from this ADR alone.

## Example Invocation

```text
/generate-adr title="Map Adabas MU fields to JSONB vs ElementCollection"
```
