---
name: "impl-plan"
description: "Structure a feature's plan.md into dependency-ordered phases with parallelism markers, capability profiles, and measurable exit criteria."
argument-hint: "feature=NNN-feature-name"
agent: "software-architect"
tools: ["read", "search", "edit"]
---
# /impl-plan

## Objective

Organize tasks in `plan.md` by dependency, safe parallelism, capability profile, and measurable criteria, without inventing scope.

## When to Invoke

In Stage 2, after `spec.md`, the initial design, and `tasks.md`, before implementation.

## Preconditions

- Each REQ-ID has `source_legacy:`
- The Modular Monolith and tasks are defined

## Inputs the Team Must Provide

- Identifier and tasks

## What I Will Do

- Create foundation, features, and hardening phases
- Mark `[P]` only for distinct files with no execution dependency, verified by grep
- Use deep reasoning, implementation, or mechanical profiles according to [`model-routing.md`](../../09-cheat-sheets/model-routing.md)
- Define measurable exit criteria and risks

## What I Will NOT Do

- Pin a model, invent a task/REQ-ID, write code, or design architecture

## Output Format

Phases with `Task ID | Title | [P] | Capability profile | Effort | Traces to`, criteria, and a risk table.

## Definition of Done

- [ ] Every task traces to a REQ-ID, takes at most one day, and has a profile
- [ ] `[P]` has evidence; phases have criteria; risks have mitigations

## Prompt Body

You are `@software-architect`. Read `spec.md`, `plan.md`, and `tasks.md`. Order foundation, features, and hardening. Mark parallelism only after checking files and dependencies. Assign a profile, never a model. Define verifiable tests, documentation, and review for each phase. Record risks, especially unconfirmed legacy rules. Break down tasks longer than one day.

## Example Invocation

```text
/impl-plan feature=014-registration
```
