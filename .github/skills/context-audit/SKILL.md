---
name: "context-audit"
description: "Use when a new engineer joins the team, when onboarding to an unfamiliar codebase, or when auditing whether the team shares a common understanding. Triggers include \"onboarding\", \"context\", \"knowledge gap\", \"bus factor\", and \"team understanding\"."
---
# Context audit

## When to Invoke

- "A new developer starts on Monday. What do they need to know in their first week?"
- "Audit whether the team really understands why we chose X."
- "Our bus factor is 1 for the billing module. Fix that."

## Objective

Measure the team's shared understanding, expose knowledge concentrated in one person, and create a first-week onboarding roadmap for new members.

## Audit questions (ask each member privately)

1. Can you draw the system architecture on a whiteboard in 5 minutes?
2. What are the 3 most important invariants this system must preserve?
3. Where is the riskiest code? Who understands it best?
4. What would you never change without a senior review? Why?
5. Which parts do you avoid changing? Why?

If the answers differ significantly, the team has a context gap.

## Anti-patterns

- "Our onboarding consists only of READMEs." (Insufficient because READMEs omit tacit knowledge.)
- A first-week plan without coding or operating the system.
- No mention of invariants or failure modes.
- Knowledge held only by senior engineers, without a documentation record.

## Output Template

### 1. Shared architecture map (1 page)

- Mermaid diagram of services and data flow
- List of external integrations and their owners
- List of invariants (business rules that must remain intact)

### 2. Risk heatmap

```markdown
| Module | Criticality | Bus factor | Last refactoring | Owner |
|----------|-------------|------------|----------------|-------|
| billing | high | 1 (Alex) | 2 years ago | Alex |
| authentication | high | 3 | 6 months ago | team |
```

Any row with a bus factor of 1 for a high-criticality module requires a P0 action.

### 3. First-week runbook for new members

- Day 1: read these 5 ADRs and run the services locally.
- Day 2: pair with Alex on billing and submit a documentation improvement.
- Day 3: shadow the on-call rotation.
- Day 4: take on a starter task with paired review.
- Day 5: hold a retrospective with the Technical Lead. What is still unclear?

## Quality Gate

- [ ] The shared architecture map, risk heatmap, and first-week runbook exist.
- [ ] Every high-criticality module with a bus factor of 1 has a P0 remediation action.
- [ ] The runbook includes coding and system operation tasks, not just reading.
- [ ] A new engineer can deliver a low-risk change by the end of the first week, with paired review.
