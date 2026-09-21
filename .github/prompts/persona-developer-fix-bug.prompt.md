---
name: "fix-bug"
description: "Reproduce, isolate, and fix a bug with a regression test, keeping spec.md as the source of truth."
argument-hint: "bug=<observed-vs-expected> req=REQ-NNN area=<service-or-page>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /fix-bug

## Objective

Fix a bug so that the fix is (a) reproducible with a new failing test, (b) the smallest change that makes that test pass, and (c) traceable to a real `REQ-ID`, either an existing one or a new one proposed through `/update-spec` when the bug reveals a missing requirement. The root cause is identified, not hidden by a superficial patch.

> [!WARNING]
> SIFAP must fail explicitly. Never wrap a bug in a catch that logs the error and continues execution.

## When to Invoke

Use when a bug is reported in code already merged into `develop` and the team wants to fix the root cause with a regression test instead of treating the symptom. Run on an `impl/<NNN>-<bug-name>` branch created from `develop`.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists for the affected area and can confirm the intended behavior
- The current branch is `impl/<NNN>-<bug-name>`
- The failure scenario is described in enough detail to reproduce it, or the reporter is available
- The affected `backend/` or `frontend/` module is already scaffolded

## Inputs the Team Must Provide

- A bug description: observed and expected behavior, exact steps, and environment
- A stack trace, log line, or screenshot, if available
- The affected service or page
- The likely related `REQ-ID` (or "unknown, investigate")
- Ask the user for any missing item before starting.

## What I Will Do

- Reproduce the bug locally or write the smallest test that captures the report
- Write the regression test before changing production code and confirm that it fails for the right reason
- Diagnose the root cause by reading the code, tracing the call stack, and checking the specification
- Map the corrected behavior to an existing `REQ-ID` or propose a new EARS requirement
- Apply the smallest fix, add a boundary test, and run the full local suite

## What I Will NOT Do

- Fix only the symptom by catching the exception, ignoring `null`, or wrapping the bug in a try/catch that logs the error and continues
- Ship a fix without a regression test
- Refactor the surrounding class "while I am here". That belongs in a separate `/refactor`
- Silently change behavior when the specification is ambiguous. Instead, I will propose a specification update
- Change the schema. That belongs to `/migration` and must be routed to the database administrator
- Invent a root cause I cannot demonstrate. If I cannot reproduce the bug, I will stop and report what is missing

## Output Format

```markdown
### Root cause
Two `BigDecimal` values were compared with `equals`, so `10.00` and `10` were never considered equal and the
exemption branch was skipped for inputs with scale 0. Three to five sentences in plain language.

### Linked requirement
REQ-031 (existing) or "PROPOSED: new REQ-XXX; see /update-spec".

### Regression and boundary tests
<complete test source, each test with an inline `// REQ-031` comment>

### Fix
<minimal production diff>

### Risk assessment
Affects the shared fee calculator used by intake and reconciliation. Both paths were retested.

### Commit message
fix(fees): compare BigDecimal by value, not scale (REQ-031)

Root cause: equals() considers scale in BigDecimal. Adds a regression test.
References: BUG-42, REQ-031
```

## Definition of Done

- [ ] A new test fails before the fix and passes afterward, with an inline `// REQ-NNN` comment
- [ ] The root cause is identified in the commit message and pull request description
- [ ] The fix is the smallest change that makes the test pass
- [ ] At least one boundary test is added beyond the reproduction case
- [ ] An existing `REQ-ID` is cited or a new one is formally proposed through `/update-spec`
- [ ] No unrelated files are modified
- [ ] The full suite passes: `./mvnw -B verify` (backend) or `pnpm lint && pnpm typecheck && pnpm build && pnpm test --run --coverage` (frontend)

## Prompt Body

You are `@implementer`. A bug has been reported and the team wants to fix the root cause with a regression test. Read the [`tdd-workflow`](../skills/tdd-workflow/SKILL.md) skill. The same red-green discipline applies to bug fixes.

**Step 1: reproduce locally first.**
Run the failure scenario or write the smallest test that captures the report. If you cannot reproduce it, stop and tell the user exactly what is missing.

**Step 2: write the regression test.**
Before changing any code, add a test named `should_<expected>_when_<condition>` in the same package as the code under test, with an inline `// REQ-NNN` comment. Confirm that it fails and read the assertion to verify that the reason is correct. Otherwise, fix the setup first.

**Step 3: diagnose the root cause.**
Read the related code, trace the call stack, and compare the behavior with `spec.md`. Write three to five plain-language sentences explaining the cause before showing any fix. Do not fix without a diagnosis.

**Step 4: map the fix to a requirement.**
If an existing `REQ-ID` covers the correct behavior, cite it. Otherwise, draft a new EARS requirement and propose it through `/update-spec`. Never change behavior silently.

**Step 5: apply the smallest fix.**
Change only what the failing test requires. Record any unrelated cleanup as `// TODO(REQ-XXX)` or in a follow-up item.

**Step 6: add a boundary test.**
A happy-path test is not enough. Add an edge case: `null`, empty, maximum value, or off-by-one.

**Step 7: run the full suite.**
Run `./mvnw -B verify` or `pnpm lint && pnpm typecheck && pnpm build && pnpm test --run --coverage`. Do not finish until everything passes.

Mask CPF and benefit amounts in any log line. If the bug reveals an ambiguous or missing requirement, route it back to the specification. Do not decide the business rule yourself.

## Example Invocation

```text
/fix-bug bug="an exempt payer is still charged a fee" req=REQ-031 area=fee-service
```
