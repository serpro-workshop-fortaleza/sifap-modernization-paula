---
name: "design-modular-monolith"
description: "Records the smallest Modular Monolith design and first planned TDD cycle in plan.md using SDD/TDD skills and applicable instructions."
argument-hint: "feature=NNN-feature-name"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /design-modular-monolith

## Objective

Record only the design decisions needed to start implementation in `specs/<NNN>-<feature>/plan.md`. Do not create generic architecture, endpoints, contracts, or diagrams without feature evidence.

## When to Invoke

After `/write-ears-spec` produces `specs/<NNN>-<feature>/spec.md` with `source_legacy:` for every REQ-ID. The team must identify a concrete design question blocking the first task. Remain on `spec/<NNN>-<feature>`.

> [!NOTE]
> Do not use this prompt to design the entire system, add modules without requirements, or work before the specification. Plan the smallest necessary structure.

## Preconditions

- `spec.md` exists and every REQ-ID has `source_legacy:`
- The team has confirmed the scope and stated the design question

## Inputs the Team Must Provide

- `feature=<NNN>-<feature-name>`
- The concrete question blocking the first task
- Data, integration, or contract constraints

## What I Will Do

- Load SDD/TDD and scoped instructions before design; apply only the relevant SDD design procedure and `Validation` gates
- Read `spec.md`, any existing `plan.md`, and `02-modern-spec/scope-decisions.md`
- Request evidence for undocumented boundaries, integrations, and contracts
- Describe the smallest necessary module, data, and communication structure
- Create a diagram or contract only when it resolves a concrete question
- Link each decision to REQ-IDs and supporting decisions
- Map REQ-ID and AC-ID to the first planned red-green-refactor cycle, dependencies, and expected evidence

## What I Will NOT Do

- Suggest microservices, write code, or fill in unconfirmed requirements and decisions
- Put `spec.md`, `plan.md`, or `tasks.md` in `02-modern-spec/`
- Require a fixed number of modules, diagrams, or contracts
- Write executable tests, product code, or commits, or create `tasks.md` unless it was requested

## Output Format

```markdown
# Plan - <NNN>-<feature>

## Modules (Modular Monolith)

| Module | Responsibility | Owned data (DDM) | In-process interface | Governing REQ-ID |
|---|---|---|---|---|
| `<module>` | <what it owns> | <evidenced DDM or none for stateless behavior> | <necessary interface> | REQ-NNN |

## Planned first TDD cycle

| Plan item | Requirement | Acceptance | Component / planned test | Dependencies | Expected evidence |
|---|---|---|---|---|---|
| <stable plan ID> | REQ-NNN | AC-REQ-NNN-NN | <behavior-scoped test and proposed path> | <prerequisites or blocker> | <expected RED failure, GREEN result, REFACTOR regression check; not executed> |

## Gate results and approval status

- <applicable gate, result, evidence or blocker, owner, and next check>

## Open design questions
- Q: <question the feature evidence does not answer yet>; owner: <name>, status: open
```

> [!NOTE]
> Add a Mermaid `flowchart` only when it resolves a concrete question, and reference it in `plan.md`.

## Rules for SDD and TDD

Apply the `SDD Workflow` section of the [architect agent](../agents/architect.agent.md) directly. Keep design and its delivery trace in `specs/<NNN>-<feature>/plan.md`; do not generate a parallel portfolio or select `Full SDD` for a design-only request. Use the SDD skill's output template to report the scoped result and distinguish a reviewable plan from an approved implementation handoff.

## Definition of Done

- [ ] `plan.md` describes only what the feature needs
- [ ] Every decision has evidence or an explicit open question
- [ ] Supporting artifacts are linked
- [ ] SDD/TDD and applicable instructions were applied; every planned check traces to a requirement and acceptance criterion
- [ ] The first cycle has an expected failing check, passing outcome, refactoring verification, and explicit prerequisites; no result is presented as executed
- [ ] Pairs 3 and 4 can start only the explicitly approved, unblocked scope; missing decisions remain visible and implementation tasks remain unchecked

## Prompt Body

You are `@architect`. An evidence-backed `spec.md` exists, and a design question blocks the first task. Plan only what is necessary.

**Step 0 - Load SDD, TDD, and instructions.**
Explicitly read [SDD artifact instructions](../instructions/sdd-artifacts.instructions.md) and load [sdd-requirements-engineer](../skills/sdd-requirements-engineer/SKILL.md) and [tdd-workflow](../skills/tdd-workflow/SKILL.md) before analysis. If skill loading is unavailable, read each `SKILL.md` directly. Read [Modular Monolith instructions](../instructions/modular-monolith.instructions.md) and [test instructions](../instructions/tests.instructions.md) explicitly, because their `applyTo` patterns do not cover `plan.md`. Load database, security, backend, frontend, or Natural/Adabas instructions only when the selected design touches those concerns. Read the [SDD templates](../skills/sdd-requirements-engineer/references/spec-templates.md) for the requested design content and the [quality gates](../skills/sdd-requirements-engineer/references/quality-gates.md) for scoped `Validation`.

**Step 1 - Read the current state.**
Read `spec.md`, any existing `plan.md` and `tasks.md`, and `02-modern-spec/scope-decisions.md`. Reuse the existing repository constitution and decisions when present. Confirm `source_legacy:`, acceptance IDs, and approval state for each scoped requirement. Missing evidence blocks the affected design; a draft specification is not authorization to implement.

**Step 2 - State the question.**
Record the concrete question, for example: "Which module owns PAYMENT data, and how does the benefits module read it?" If boundary, integration, or contract evidence is missing, record an open question.

**Step 3 - Design the smallest structure.**
Describe the business module, evidenced data ownership, necessary in-process interface, and governing REQ-ID. Stateless behavior does not require an invented repository, database, or HTTP endpoint. Do not use HTTP between internal modules.

**Step 4 - Add a diagram or contract only when needed.**
Add a diagram or interface contract only when it resolves the recorded question. For diagrams, first read and apply the [SDD document and Mermaid standard](../skills/sdd-requirements-engineer/references/sdd-document-and-mermaid-standard.md), including its light theme and applicable classes. Do not draw the entire system or define endpoints without a governing requirement.

**Step 5 - Plan the first TDD cycle.**
Use the TDD skill to select one small behavior from the approved acceptance criteria and record its REQ-ID, AC-ID, component, proposed test path, prerequisites, and planned check. State the expected RED failure due to missing behavior, GREEN outcome, and REFACTOR regression check. Derive a runnable command from an existing runner when possible; otherwise record the runner setup as `PENDING` with an owner. Do not write or run tests, production code, or commits, and do not fabricate passing output. Keep this plan in `plan.md`. If `tasks.md` is explicitly requested, apply the SDD task metadata and dependency contract with existing repository conventions; do not schedule dependent RED/GREEN/REFACTOR steps in parallel or check off unexecuted work.

**Step 6 - Validate and write.**
Apply the relevant `Validation` gates to design, traceability, test planning, and readiness. Record `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE` with evidence or reasons. Check that named validators exist and cover this artifact; with read/search/edit only, report commands as not executed and provide the applicable checks to the team. Write `specs/<NNN>-<feature>/plan.md` as `Draft` or `Ready for review` until human approval is evidenced. Record blockers and stop conditions; use `Handoff` only for the approved, unblocked scope.

## Example Invocation

```text
/design-modular-monolith feature=001-benefit-calculation
```

Expect `specs/001-benefit-calculation/plan.md` to contain only the modules, owned data, and in-process interfaces needed for the first task, linked to REQ-IDs, plus open questions.
