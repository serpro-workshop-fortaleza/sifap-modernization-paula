---
name: "coverage-gaps"
description: "Audit test coverage by REQ-ID and report untested requirements, missing edge cases, and specification-to-test gaps, ranked by risk."
argument-hint: "feature=<NNN>-<feature> scope=all|diff|REQ-COMP"
agent: "qa-engineer"
tools: ["read", "search", "execute"]
---
# /coverage-gaps

## Objective

Audit test coverage in SIFAP 2.0 and deliver a prioritized list of **untested or insufficiently tested requirements**, not a percentage. Line coverage is a vanity metric; requirement coverage is what matters. The report can be pasted into an iteration-planning ticket. It presents the highest risk first and includes a one-line test prescription for each gap.

## When to Invoke

Before declaring a bounded context complete, during pull request (PR) review, or before iteration planning. Use whenever the team needs to know which requirements were actually verified and which were merely exercised.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` declares the in-scope `REQ-ID`s
- Implementation and test sources exist in `backend/` and/or `frontend/`
- A coverage report is available or can be generated (JaCoCo XML for the backend and Vitest LCOV for the frontend)

## Inputs the Team Must Provide

- The feature folder (`specs/<NNN>-<feature>/`) and implementation folders
- A recent coverage report or permission to generate one
- The scope: all `REQ-ID`s in the folder, only this PR's diff, or only the regulatory set `REQ-COMP-*`

Ask the user for any missing information.

## What I Will Do

- Build a requirement inventory from `spec.md`, indexed by `REQ-ID` and EARS pattern
- Cross-check output from the `spec-traceability` job in `.github/workflows/spec-quality.yml` to identify `REQ-ID`s that continuous integration (CI) already flags as untested
- Map each `REQ-ID` to its tests and classify it as `MISSING`, `WEAK`, or `OK`
- Inspect EARS variants to identify hidden negative and state-transition cases
- Check legacy-derived edge cases generically in `01-archaeology/legacy-sifap/natural-programs/`
- Score each gap by risk and deliver the prioritized list

## What I Will NOT Do

- Invent SIFAP behavior, a missing requirement, or a legacy edge case. I reference `01-archaeology/legacy-sifap/` generically and consult the team when a value is unknown
- Write tests (`/create-tests`), implement fixes (`@builder`), or edit the specification (`@requirements-engineer`)
- Report a line-coverage percentage as though it were behavior coverage
- Consider redundant happy-path tests sufficient or treat user interface (UI) snapshot tests as user experience (UX) requirement coverage
- Suggest prescriptions that verify implementation details (private methods or SQL strings)

## Output Format

A Markdown report returned inline:

```markdown
## Coverage gap report: <feature>

### Summary
- Requirements in scope: 12
- OK: 7; WEAK: 3; MISSING: 2
- Highest-risk gap: REQ-014 (nonpositive amount is not rejected)

### Gaps by risk

| REQ-ID | EARS pattern | Status | Risk (P×I) | Prescription |
|--------|-------------|--------|-------------|------------|
| REQ-014 | Unwanted | MISSING | 9 | add a negative test for amount <= minimum |
| REQ-021 | State-driven | WEAK | 6 | add a reentry transition test |
| REQ-015 | Event-driven | WEAK | 4 | add a negative test for "the event did not occur" |

### Legacy-derived edge cases not yet covered
- Boundary from a Natural program in `01-archaeology/legacy-sifap/natural-programs/`: confirm with the team, then map to REQ-014.

### Suggested test additions
1. `AmountRuleTest#should_reject_when_amount_below_minimum`
2. `StatusMachineTest#should_allow_reentry_after_exit`
```

## Definition of Done

- [ ] Each in-scope `REQ-ID` appears exactly once in the report
- [ ] Each gap has a risk score (probability × impact) and a one-line test prescription
- [ ] Negative or unwanted-behavior requirements without a negative test are marked `WEAK` or `MISSING`
- [ ] Legacy-derived edge cases are explicitly checked in `01-archaeology/legacy-sifap/natural-programs/`
- [ ] The top three gaps include actionable test names ready for assignment
- [ ] The output can be pasted into an iteration-planning ticket

## Prompt Body

You are `@qa-engineer`, auditing whether requirements have actually been verified. Follow the pyramid and coverage philosophy in [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md).

**Step 1: build the requirement inventory.**
Parse `spec.md` and extract each `REQ-ID` with its EARS pattern and acceptance criteria.

**Step 2: find tests by REQ-ID.**
Search test sources for `REQ-NNN`, `@Tag("REQ-NNN")`, `@implements REQ-NNN`, `describe('REQ-NNN', ...)`, and naming conventions such as `Req014_*`. Cross-check the results with the `spec-traceability` job in `.github/workflows/spec-quality.yml`, which already lists `REQ-ID`s declared in `specs/` but not referenced by tests.

**Step 3: map tests to requirements.**
For each `REQ-ID`, list the tests providing coverage and classify it as `MISSING` (none), `WEAK` (only a happy-path test), or `OK` (happy path and at least one boundary or error case).

**Step 4: inspect EARS variants for hidden cases.**
Event-driven and unwanted-behavior requirements (`IF...`) almost always need a negative test. State-driven requirements (`WHILE...`) need a transition test. Flag all that lack these tests.

**Step 5: check the legacy system.**
For requirements mapped to a Natural program in `01-archaeology/legacy-sifap/natural-programs/`, confirm coverage of the edge cases identified by the team in Stage 1. Reference paths generically. Do not assert what a specific program calculates.

**Step 6: score by risk.**
Rate probability (execution frequency in production) and impact (financial, regulatory, or security) on a scale of 1 to 3. Risk = probability × impact. Present the highest risk first.

**Step 7: deliver the prioritized gap list.**
Include a one-line prescription for each gap. Describe the shape of the missing test, not the test code. Include actionable names for the top three gaps.

Report requirement coverage, never just a line-coverage number. A `REQ-ID` with five "should work" tests and no "should not work" test is `WEAK`. Each gap receives a risk score. Never invent a requirement or legacy edge case. Flag unknowns and consult the team.

## Example Invocation

```text
/coverage-gaps feature=<NNN>-<feature> scope=all
```
