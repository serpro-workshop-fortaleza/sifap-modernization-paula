---
name: "routing-table"
description: "Map a feature's tasks to the appropriate Copilot mode and model tier, with rationale and cost tier, following the kit's routing cards."
argument-hint: "tasks=specs/<NNN>-<feature>/tasks.md"
agent: "tech-lead"
tools: ["read", "search"]
---
# /routing-table

## Objective

Map tasks to a sufficient mode and model tier, with rationale and cost, following the kit's cards.

## When to Invoke

At the start of a feature, after `tasks.md`.

## Preconditions

- Tasks exist
- [`model-routing.md`](../../09-cheat-sheets/model-routing.md) and [`copilot-3-modes.md`](../../09-cheat-sheets/copilot-3-modes.md) are the sources

## Inputs the Team Must Provide

- Path to the tasks

## What I Will Do

- Classify tasks as Discovery, Design, Implementation, Refactor, Review, or Mechanical
- Recommend Ask, Plan, or Agent and Haiku 4.5, Sonnet 4.6, or Opus 4.6
- Provide a per-task rationale, Low/Medium/High cost, and cheaper options

## What I Will NOT Do

- Pin a model in frontmatter, invent a tier, use Opus by default, or redefine scope

## Output Format

Table `Task ID | Category | Copilot mode | Model tier | Rationale | Cost`.

## Definition of Done

- [ ] Every task has a mode, tier, and specific rationale
- [ ] There is a cheaper candidate or "none applicable"; recommendations follow the cards

## Prompt Body

You are `@tech-lead`. Read the tasks and assess ambiguity and risk. Classify them. Use Ask mode for exploration, Plan for changes across multiple files, and Agent for a well-defined issue through to a PR. Use Haiku 4.5 for mechanical work, Sonnet 4.6 by default, and Opus 4.6 only for architecture, technical trade-offs, or impact. Justify escalation. Assign cost and flag savings without loss of quality. Never pin the model.

## Example Invocation

```text
/routing-table tasks=specs/014-registration/tasks.md
```
