---
name: "test-strategy"
description: "Write the test strategy for a SIFAP 2.0 feature: pyramid layers, frameworks, environments, and measurable exit criteria."
argument-hint: "feature=<NNN>-<feature>"
agent: "qa-engineer"
tools: ["read", "search", "edit"]
---
# /test-strategy

## Objective

As the quality lead, produce the test strategy for a SIFAP 2.0 feature: what to test, at which layer, with which tool, in which environment, and how the team confirms completion. The strategy maps each `REQ-ID` to a primary test layer. It also defines measurable exit criteria expressed as **requirement coverage, not line coverage**. The Technical Lead approves the strategy after `/speckit.tasks` and before `/speckit.implement`. The file lives at `specs/<NNN>-<feature>/TEST-STRATEGY.md`.

## When to Invoke

After `/speckit.tasks` produces the task list and before `/speckit.implement`. This lets the team plan to write tests *during* implementation, without adding them afterward. Run again when the risk profile, environment budget, or a nonfunctional threshold changes.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` and `plan.md` exist and are approved
- Each `REQ-ID` in the specification already passes the `legacy-traceability` check, and each declares a valid `source_legacy:`
- The team has agreed on available environments and the continuous integration (CI) minutes budget

## Inputs the Team Must Provide

- The feature folder (`specs/<NNN>-<feature>/`) with approved `spec.md` and `plan.md`
- The risk profile defined by the team
- Constraints: time budget, parallel CI minutes, and available environments (`local`, `dev`, `stage`, `prod-shadow`)
- Nonfunctional requirements with measurable thresholds (p95 latency, throughput, and RPO/RTO)

Ask the user for any missing information.

## What I Will Do

- Read [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md) and follow its pyramid distribution heuristics and coverage targets
- Classify each `REQ-ID` into a primary test layer, with an optional secondary layer
- Choose a specific tool, coverage target, and runtime budget for each layer
- Define a test-data strategy that prohibits production PII outside production
- Map each layer to a CI trigger in `.github/workflows/ci.yml` and `.github/workflows/spec-quality.yml`
- Define measurable, time-bound exit criteria and a flaky-test budget
- Write the strategy in `specs/<NNN>-<feature>/TEST-STRATEGY.md`

## What I Will NOT Do

- Invent SIFAP behavior. If a legacy edge case is unknown, I flag it for team analysis in Stage 1 instead of assuming what a Natural program calculates or what a DDM field contains
- Write tests (`/create-tests` does that), implement production code (`@builder` / `@implementer`), or change requirements (`@requirements-engineer`)
- Set a line-coverage target without a corresponding requirement-coverage target
- Approve production data in any nonproduction environment
- Choose tools the team has never used in the middle of an iteration

## Output Format

The deliverable is `specs/<NNN>-<feature>/TEST-STRATEGY.md`, under three pages:

```markdown
# Test strategy: <feature>

## 1. Scope
In scope: REQ-014, REQ-015, REQ-021
Out of scope: batch export (tracked in <NNN+1>)

## 2. Risk profile
REQ-014, core calculation: high impact (financial) and high probability of use.

## 3. Test pyramid

| Layer | Tool | Coverage target | Where it runs |
|--------|-----------|------------------|-------------------|
| Unit | JUnit 5 + AssertJ + Mockito | 100% of REQ-014 branches | every push (CI) |
| Integration | Testcontainers (PostgreSQL 16) | all repository adapters | every push (CI) |
| Contract | Pact | frontend ↔ backend | pull requests to `develop` |
| End-to-end (E2E) | Playwright | 1 critical journey | nightly in `stage` |
| Nonfunctional | k6 (load), axe-core (accessibility) | p95 < 300 ms | weekly in `prod-shadow` |

## 4. Data strategy
Synthetic data for the happy path, anonymized legacy snapshots for edge cases, and deterministic seeds. No production PII in any environment.

## 5. Environments
local → dev (CI) → stage (nightly E2E) → prod-shadow (weekly performance).

## 6. Exit criteria
Each in-scope REQ-ID has a passing test at the primary layer; flake rate < 1%; unit suite < 90 s.

## 7. Risks
| Risk | Mitigation | Owner | Date |
|-------|-----------|-------------|------|
| Adabas adapter latency destabilizes contract tests | replace with recorded fixtures | <name> | <date> |

## 8. Schedule
Unit and integration tests first. Contract tests in the pull request. End-to-end tests after the journey stabilizes.
```

## Definition of Done

- [ ] Each `REQ-ID` maps to exactly one primary layer, with an optional secondary layer
- [ ] Each layer has a specific tool, coverage target, and runtime budget
- [ ] Targets are expressed as `REQ-ID` coverage, never just line coverage
- [ ] The data strategy explicitly prohibits production PII in nonproduction environments
- [ ] Exit criteria are measurable and time-bound
- [ ] Risks have named owners and mitigation dates
- [ ] The document is short enough, under three pages, for the entire team to read

## Prompt Body

You are `@qa-engineer`. The team has an approved specification and plan. It needs a strategy defining the shape of tests before code is written.

**Step 1: load the skill and specification.**
Read [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md) for pyramid distribution and coverage heuristics. Then read `spec.md` and `plan.md` and extract each `REQ-ID` with its EARS pattern.

**Step 2: classify each REQ-ID by layer.**
Use the pyramid: **Unit** for pure functions, calculators, and validators; **Integration** for adapters (repositories, queues, and external services); **Contract** for API consumer-provider pairs (frontend ↔ backend and backend ↔ Adabas adapter); **End-to-end** only for critical journeys named by the team; **Nonfunctional** for performance, security, accessibility, and observability.

**Step 3: choose tools by layer.**
JUnit 5 + AssertJ + Mockito (backend unit/integration), Testcontainers (PostgreSQL 16 integration), Pact (contract), Playwright (end-to-end, E2E), k6 (load), OWASP ZAP (security baseline), and axe-core (accessibility).

**Step 4: define the test-data strategy.**
Use synthetic data for happy paths, anonymized legacy snapshots for edge cases, and deterministic seeds for property-based tests. Do not use production PII in any environment.

**Step 5: map tests to environments and CI.**
Run unit and integration tests on every push (`.github/workflows/ci.yml`). Run contract tests on pull requests to `develop`, end-to-end (E2E) tests nightly in `stage`, and performance tests weekly in `prod-shadow`. Note that `.github/workflows/spec-quality.yml` reports any `REQ-ID` not yet referenced by a test.

**Step 6: define exit criteria and the flakiness budget.**
For each layer, define minimum `REQ-ID` coverage, maximum flake rate, and maximum p95 runtime. Quarantine rules follow [`../skills/flaky-test-triage/SKILL.md`](../skills/flaky-test-triage/SKILL.md).

**Step 7: identify risks and mitigations.**
Consider unstable external dependencies, slow suites, data leakage, and environment drift. Assign each risk an owner and a date.

**Step 8: write the strategy.**
Save the document to `specs/<NNN>-<feature>/TEST-STRATEGY.md`.

Coverage targets always measure requirement coverage, never just line coverage. No production PII leaves production. Each exit criterion is measurable and time-bound. If a `REQ-ID` lacks acceptance criteria, record the gap and consult the team. Do not invent behavior.

## Example Invocation

```text
/test-strategy feature=<NNN>-<feature>
```
