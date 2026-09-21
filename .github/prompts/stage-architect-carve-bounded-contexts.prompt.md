---
name: "carve-bounded-contexts"
description: "Evaluates scoped Stage 1 boundary hypotheses using SDD, TDD testability planning, and Modular Monolith instructions for a human decision."
argument-hint: "report=01-archaeology/discovery-report.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /carve-bounded-contexts

## Objective

Evaluate boundary hypotheses for the selected feature and record proposals separately from human-approved decisions. Describe responsibilities, evidenced data ownership, and in-process communication without prescribing a number of contexts.

## When to Invoke

At the start of Stage 2, immediately after reviewing `01-archaeology/discovery-report.md`.

## Preconditions

- The report identifies the selected scope and evidenced boundary hypotheses; do not invent extra hypotheses to reach a quota
- The team has reviewed the report and is ready to decide

## Inputs the Team Must Provide

- The discovery report path
- Additional constraints or preferences

## What I Will Do

- Load SDD/TDD and scoped instructions before evaluating hypotheses; apply the relevant SDD procedure and `Validation` gates without generating a `Full SDD` package
- Read the hypotheses and assess each for cohesion, coupling, and change frequency
- Present the analysis to the team and record rejections with rationale
- Formalize accepted contexts with names, responsibilities, and data ownership

## What I Will NOT Do

- Decide automatically; the team makes the final decision
- Propose microservices; the target is a Modular Monolith
- Invent business context or omit evaluation criteria
- Write requirements, executable tests, product code, or commits, or treat testability planning as executed TDD

## Output Format

A file at `02-modern-spec/bounded-contexts.md`:

```markdown
# Bounded context map
## Evaluation criteria
## Hypothesis evaluation
### [Hypothesis name] - Proposed / Accepted / Rejected
## Final bounded contexts
### [Context name]
- Responsibility:
- Owned data (DDMs/tables):
- Public interface:
- Reason for a separate context:
## Communication between contexts
## Planned verification and traceability
## Open decisions and validation status
## Context diagram, when needed
```

## Rules for SDD and TDD

Apply the [shared SDD artifact contract](../agents/architect.agent.md#sdd-workflow) directly, without a tooling prerequisite: keep supporting boundary decisions here and canonical requirements in `specs/<NNN>-<feature>/spec.md`. Link existing REQ-ID and AC-ID where available; before requirements exist, retain primary evidence and mark downstream mapping `PENDING`, rather than inventing IDs. Use the SDD skill's output template for the final report, without turning a proposed map into an implementation handoff.

## Definition of Done

- [ ] Every hypothesis has been assessed against all three criteria
- [ ] Rejections have a rationale
- [ ] Contexts are proportional to the evidenced scope, with no minimum count
- [ ] Each context has responsibilities, evidenced data ownership or a justified stateless boundary, and any necessary interface
- [ ] Any diagram uses the SDD light theme; an omitted diagram has an applicability rationale
- [ ] SDD/TDD and applicable instructions were applied; proposals, human decisions, planned checks, and blockers remain distinct

## Prompt Body

You are `@architect`. The team is starting Stage 2 and needs to define bounded contexts for the Modular Monolith.

**Step 0 - Load SDD, TDD, and instructions.**
Explicitly read [SDD artifact instructions](../instructions/sdd-artifacts.instructions.md) and load [sdd-requirements-engineer](../skills/sdd-requirements-engineer/SKILL.md) and [tdd-workflow](../skills/tdd-workflow/SKILL.md) before analysis. If skill loading is unavailable, read each `SKILL.md` directly. Read [Modular Monolith instructions](../instructions/modular-monolith.instructions.md), [test instructions](../instructions/tests.instructions.md) for planned checks, and [Natural/Adabas instructions](../instructions/natural-adabas.instructions.md) before legacy sources. Their `applyTo` patterns do not automatically cover this artifact. Read the [SDD quality gates](../skills/sdd-requirements-engineer/references/quality-gates.md) for scoped `Validation`; do not invoke `Full SDD` merely to evaluate boundaries.

**Step 1 - Read the report.**
Extract the selected scope and each relevant hypothesis with its programs, data ownership, and primary evidence. Inspect existing scope and boundary decisions before proposing changes; preserve deferred work and legacy question status.

**Step 2 - Assess three criteria.**

- **Cohesion**: do the rules represent the same business capability? Consult confirmed rules in `01-archaeology/business-rules-catalog.md`.
- **Coupling**: how many dependencies cross the boundary? Count the edges in `01-archaeology/dependency-map.md`. Low coupling strengthens the hypothesis.
- **Change frequency**: use dated change history or explicit team evidence. Names and call structure do not prove change frequency; record `PENDING` with an owner and impact when evidence is unavailable.

Use High/Medium/Low only when supported by cited evidence. Keep unknown assessments explicit; a proposed boundary is not an accepted decision.

**Step 3 - Request the decision.**
Present the assessment, recommendation, and rationale. Ask: "Does the team accept this recommendation? If not, what would you change?" Record the rationale for any different decision.

**Step 4 - Formalize accepted contexts.**
For each approved context, record its confirmed name, responsibility, owned DDMs or tables when applicable, necessary public operations, and rationale. A stateless capability does not need an invented repository or data store. Keep unapproved alternatives as `Proposed` with an accountable decision owner.

**Step 5 - Define communication.**
Record direction, mechanism (an in-process interface call, domain event, or shared kernel type), and exchanged data. Communication is in-process, never HTTP between services.

Assess testability using TDD and the test instructions: link each material boundary to existing acceptance criteria and a planned observable check or sourced architecture constraint. If the decision has no executable behavior, record TDD as `NOT APPLICABLE` with a reason. Do not write tests or claim a red-green-refactor cycle occurred.

**Step 6 - Draw the map.**
Add a diagram only when it clarifies the selected boundary or communication decision. First read and apply the [SDD document and Mermaid standard](../skills/sdd-requirements-engineer/references/sdd-document-and-mermaid-standard.md), including its universal light theme and applicable graph classes. Do not define a competing palette in this prompt.

**Step 7 - Write the output.**
Apply the scoped `Validation` gates and record `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE` with evidence or reasons. Check whether each cited validator exists and applies; with read/search/edit only, report commands as not executed and provide the checks to the team. Write `02-modern-spec/bounded-contexts.md` as `Draft` or `Ready for review` until explicit approval, retaining evidence, owners, and unresolved blockers.

## Example Invocation

```text
/carve-bounded-contexts report=01-archaeology/discovery-report.md
```
