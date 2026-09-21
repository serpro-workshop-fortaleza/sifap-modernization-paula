---
name: "user-story-refine"
description: "Use when refining backlog items, splitting epics, or validating INVEST criteria. Triggers include \"refine story\", \"split epic\", \"acceptance criteria\", \"user story\", and \"INVEST\"."
---
# User story refinement

## When to Invoke

- "This story is too large. Help me split it."
- "Turn this feature description into user stories with acceptance criteria."
- "Check whether these stories meet INVEST."

## Required inputs

- Feature or epic description
- Persona or user type
- Business objective served by the feature
- Known constraints (regulatory, technical, or UX)

## Refinement steps

1. **Confirm the outcome**. Each story must answer: which persona, what outcome, and why it matters.
2. **Apply INVEST** (independent, negotiable, valuable, estimable, small, and testable) to each draft.
3. **Split vertically**, never horizontally. Prefer splitting by workflow step, data variation, CRUD operation, happy path versus edge case, business rule, or acceptance criterion.
4. **Write acceptance criteria in Given/When/Then format**. Include a happy path, an edge case, and an error path.
5. **Trace to a REQ-ID**. Every story must link to at least one requirement.

## Splitting patterns

Use these patterns when a story is too large to complete in one iteration:

| Pattern | Split a story by... | Example |
|---|---|---|
| Workflow steps | Each step of a multistep workflow | Submit versus review versus approve |
| Business rule | One rule per story | Standard rate versus exemption rate |
| Data variation | Each input type or format | Domestic versus international address |
| CRUD operation | Create, read, update, and delete separately | Add a record before editing a record |
| Happy path versus edge | Happy path first, then edge cases | Valid input before rejected input |
| Spike | Separate uncertainty into time-boxed research | Prototype the integration first |

## Anti-patterns

- Stories written as tasks ("Add a button").
- Acceptance criteria describing the interface instead of behavior.
- Horizontal splits ("backend story" + "UI story" for the same feature).
- Missing REQ-ID link.

## Output Template

```markdown
### US-NNN: <short title>
**As a** <persona>
**I want** <capability>
**So that** <business outcome>

**Acceptance criteria**
- Given <context>, When <action>, Then <outcome>
- Given <edge case>, When <action>, Then <outcome>

**Traces to**: REQ-001, REQ-042
**Effort**: S / M / L
**Dependencies**: US-NNN (if any)
```

## Quality Gate

- [ ] The story meets all INVEST criteria.
- [ ] Acceptance criteria use Given/When/Then and cover the happy path, an edge case, and the error path.
- [ ] The story is split vertically, not by architecture layer.
- [ ] The story traces to at least one REQ-ID, and each linked REQ-ID contains a `source_legacy:` line (enforced by the `legacy-traceability` CI job).
