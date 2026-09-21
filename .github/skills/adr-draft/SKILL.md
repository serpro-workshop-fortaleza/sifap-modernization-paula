---
name: "adr-draft"
description: "Use when drafting Architecture Decision Records, evaluating alternatives, or documenting technical trade-offs. Triggers include \"ADR\", \"architecture decision\", \"trade-off\", \"choose between\", and \"why we chose\"."
---
# ADR draft

## When to Invoke

- "Draft an ADR for choosing PostgreSQL over MongoDB."
- "Document our decision to adopt an event-driven architecture."
- "Review ADR-007 because we need to supersede it."

## When to write an ADR

Write an ADR when a decision:

- Is difficult or expensive to reverse.
- Affects more than one team.
- Constrains future choices (technology lock-in).
- Is likely to be questioned in six months.

Do not write an ADR for a local refactoring or a reversible configuration change.

## Writing tips

- Write in the present tense ("We use X").
- Include at least two rejected alternatives.
- Name consequences you know will be difficult. This will be useful later.
- Supersede, never delete. History adds value.

## Anti-patterns

- ADRs written afterward to justify a decision already made.
- An ADR that bundles five unrelated decisions.
- A missing alternatives section, indicating that trade-offs were not analyzed.
- Status left as "proposed" for months.

## Output Template

Save the ADR in `docs/adr/NNNN-<slug>.md`. The repository's canonical template is [`docs/adr/0000-template.md`](../../../docs/adr/0000-template.md); the abbreviated structure is:

```markdown
# ADR-NNN: <Decision title in the imperative>

**Status**: proposed | accepted | superseded by ADR-NNN | deprecated
**Date**: YYYY-MM-DD
**Decision makers**: <names>
**Context tags**: security, performance, cost

## Context
Two to four paragraphs. What is the driving factor? What constraints apply?

## Decision
One paragraph. "We will <decision>."

## Alternatives considered
- **Option A**: <summary>. Pros: ... Cons: ...
- **Option B**: <summary>. Pros: ... Cons: ...
- **Option C (chosen)**: <summary>. Pros: ... Cons: ...

## Consequences
### Positive
- ...
### Negative
- ...
### Neutral
- ...

## Follow-ups
- [ ] Update REQ-NNN
- [ ] Migrate <system>
- [ ] Review in Q<N>

## References
- Source 1
- Source 2
```

## Quality Gate

- [ ] The ADR has Context, Decision, Alternatives considered, and Consequences sections.
- [ ] At least two rejected alternatives are documented with their trade-offs.
- [ ] The status is set (proposed, accepted, superseded, or deprecated), not blank.
- [ ] The file is saved as `docs/adr/NNNN-<slug>.md` and linked to the affected REQ-IDs.
