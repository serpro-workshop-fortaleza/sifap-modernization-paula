---
name: "create-adr"
description: "Write an ADR recording the context, options, decision, and consequences of a SIFAP 2.0 architectural choice."
argument-hint: "feature=NNN-feature-name topic=<decision>"
agent: "enterprise-architect"
tools: ["read", "search", "edit"]
---
# /create-adr

## Objective

Produce an Architecture Decision Record using the repository's ADR template. The record captures the context, at least three options, the decision, and the consequences of a cross-cutting or feature-specific SIFAP 2.0 choice. An ADR becomes immutable after acceptance. Corrections are made in a new ADR that supersedes it.

## When to Invoke

When a decision blocks `plan.md`, is costly to reverse, affects more than one team, or commits to a technology. Consult the "should this be an ADR?" test in the [`adr-draft`](../skills/adr-draft/SKILL.md) skill.

## Preconditions

- The decision topic is stated
- The target location is known: project-wide -> `docs/adr/` (template `docs/adr/0000-template.md`); feature-scoped -> `specs/<NNN>-<feature>/` (template `02-modern-spec/ADR-TEMPLATE.md`)
- The next ADR number has been checked to avoid collisions
- Linked REQ-IDs and `.specify/memory/constitution.md` are accessible

## Inputs the Team Must Provide

- `topic=<decision in plain language>`
- The location or scope (project or feature)
- The linked REQ-IDs affected by the decision
- The stakeholders and approvers to name
- A draft of the chosen direction, even if rough
- Ask the user for any missing information

## What I Will Do

- Choose the correct template: `docs/adr/0000-template.md` (project) or `02-modern-spec/ADR-TEMPLATE.md` (feature)
- Choose a verb-led decision title and the next collision-free number
- Set the status correctly: Proposed, Accepted, Superseded by NNNN, or Rejected
- Write an accurate context (forces, constraints, and previous ADRs)
- List at least three options, including the status quo, with pros, cons, and a cost/risk profile
- State the decision and rationale and record positive AND negative consequences
- Link REQ-IDs, previous ADRs, and the constitutional rules on which the decision depends
- Follow the [`adr-draft`](../skills/adr-draft/SKILL.md) skill for procedure and quality

## What I Will NOT Do

- Present only the chosen option. I always list rejected alternatives because they represent half the record's value
- Rewrite an accepted ADR. I create a new ADR that supersedes it
- Assert what a specific legacy program does. The context cites files the team has read, or I request information as protection against hallucinations
- Invent REQ-IDs, approvers, or a decision the team has not made
- Define nonnegotiable rules. They belong in the constitution, created by `/create-constitution`

## Output Format

A single file that follows the chosen template and aligns with `docs/adr/0000-template.md`:

```markdown
# ADR-0007: Adopt Flyway for database migrations

| Field | Value |
|---|---|
| **Status** | accepted |
| **Date** | 2026-05-12 |
| **Author** | Enterprise Architect: <name> |
| **Supersedes** | N/A |

## Context

The modernization replaces Adabas with PostgreSQL 16 and requires a versioned
schema evolution strategy enforced by continuous integration (CI). Cite the legacy programs
the team has read (`path#Lstart-Lend`) that inform the schema's shape. Do not
assume their contents.

## Decision

We will adopt Flyway. Each change is a versioned file
`V<N>__description.sql`, and CI runs `flyway:migrate` on each pull request (PR) to
`develop`.

## Alternatives considered

| Alternative | Reason for rejection |
|---|---|
| Liquibase | More verbose XML; steeper learning curve for the immersion |
| Manual SQL | No traceability, rollback, or CI integration |

## Consequences

- **Easier:** each schema change is traceable and checked by CI.
- **Harder:** applied migrations are immutable; fixes require a new file.
- **Risks:** editing an applied migration breaks Flyway.
- **Mitigations:** protection of the `develop` branch.

## Related

- REQ-IDs: REQ-DATA-003
- ADRs: ADR-0003
- Legacy source files: <programs the team cited>
```

## Definition of Done

- [ ] The file follows the chosen template and `NNNN-title-slug` naming, without number collisions
- [ ] The status is Proposed, Accepted, Superseded by NNNN, or Rejected
- [ ] The date and approvers are recorded
- [ ] At least three options are listed, each with pros, cons, and a cost/risk profile
- [ ] The decision names the chosen option; consequences include positive effects, negative effects, and risks
- [ ] Linked REQ-IDs, previous ADRs, and relevant constitutional rules are cited
- [ ] The ADR is treated as immutable after acceptance: superseded, never rewritten

## Prompt Body

You are `@enterprise-architect`, recording a lasting answer to "why did we do it this way?".

**Step 1: choose the template and location.**
Project-wide decision -> `docs/adr/` with `docs/adr/0000-template.md`; feature-scoped -> `specs/<NNN>-<feature>/` with `02-modern-spec/ADR-TEMPLATE.md`.

**Step 2: choose a precise title and number.**
Use a verb-led title phrased as a decision ("Integrate legacy Adabas data through a REST adapter"). Use the next number that does not collide with existing files.

**Step 3: set the status.**
Proposed (draft), Accepted (approved with a date), Superseded by NNNN, or Rejected (recorded to avoid reopening the discussion).

**Step 4: write the context accurately.**
Name the forces and constraints (Java 21, PostgreSQL 16, Azure-only, and regulatory) and previous ADRs. Cite the legacy files the team has actually read. Never reproduce their contents from memory.

**Step 5: list at least three options.**
Include the status quo or a "do nothing" option. Each option gets a one-line description, up to three pros, up to three cons, and a cost/risk note.

**Step 6: state the decision and rationale.**
Use one paragraph for each and name the chosen option.

**Step 7: record the consequences.**
Include positive effects, negative effects, new risks, and all decisions that are now forced or constrained.

**Step 8: link and sign.**
Cite REQ-IDs, previous ADRs, and the constitutional rules on which the decision depends. Record the date and approvers.

Always list rejected options, supersede rather than rewrite, and cite legacy files rather than reproducing them from memory. A nonnegotiable rule belongs in the constitution, not an ADR.

## Example Invocation

```text
/create-adr feature=001-pagamento-beneficio topic="Expose legacy Adabas data through a REST adapter"
```
