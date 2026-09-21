---
name: "refactor"
description: "Improve internal structure protected by passing tests without changing observable behavior or breaking REQ-ID traceability."
argument-hint: "target=<file-or-package> smell=<code-smell>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /refactor

## Objective

Improve the internal structure of existing code without changing how it works. A change that alters behavior is not a refactoring. It belongs to `/implement` or `/fix-bug`. The result keeps all existing tests passing with the same names and all `REQ-ID` links intact: one code smell, one transformation, one pull request.

> [!WARNING]
> If any output, assertion, or public signature changes, this is not a refactoring. Stop and use `/implement` or `/fix-bug`.

## When to Invoke

Use when an identified code smell is slowing the team down and the target has a safety net of passing tests, or can receive one quickly. Run on a dedicated `impl/<NNN>-<feature>` branch, separate from any feature or bug-fix work.

## Preconditions

- The target file, package, or component exists and compiles
- Current tests pass, or characterization tests can be added first
- No `/fix-bug` is pending on the same code. Bugs are fixed before refactoring, starting from a clean baseline
- All constraints in `plan.md` or ADRs, for example, "controllers stay thin", are known

## Inputs the Team Must Provide

- The target file, package, or component
- The motivation: the observed code smell (`Long Method`, `Duplication`, `Primitive Obsession`, `Feature Envy`, among others)
- Any constraints from `plan.md` or ADRs that limit the change
- Current test coverage for the area (run a coverage report if it is unknown)
- Ask the user for any missing item.

## What I Will Do

- Confirm the safety net. If line coverage is below 80%, write characterization tests first
- Precisely identify the code smell from the catalog and cite one or two lines as evidence
- Choose an appropriate Fowler transformation and apply it as a single behavior-preserving step
- Run tests before and after each micro-step, keeping the suite green at every commit
- Move each `@implements REQ-NNN` annotation with its method, unchanged

## What I Will NOT Do

- Refactor without tests. That is a rewrite by another name
- Change behavior under the guise of refactoring. If any output or assertion changes, the work is invalid
- Make "small improvements" to neighboring code. I will stay strictly within the identified code smell
- Rename or reshape a public API without a migration or deprecation plan
- Combine a refactoring with a feature or bug fix in the same pull request
- Invent new behavior that the specification does not describe. I will make structural changes only; requirement questions go to `/update-spec`

## Output Format

```markdown
### Identified code smell
`Long Method`: `FeeService.calculate()` spans 74 lines across three nested branches.

### Selected refactoring
`Extract Method`: move each branch to `applyExemption`, `applyCeiling`, and `applyRounding`.

### Diffs
<before/after for every touched file>

### Test results
`./mvnw test` → 12 passing (with the same names as before).

### Behavior preservation note
Public API unchanged. No new `throws` clause. No database migration. No new environment variable.

### Commit message
refactor(fees): extract fee calculation steps

Splits calculate() into three private methods. No behavior change.
References: REQ-031
```

## Definition of Done

- [ ] All previously passing tests still pass, with the same names
- [ ] No public API change, new exception, or new dependency
- [ ] Coverage does not decrease
- [ ] One code smell, one transformation, one pull request
- [ ] All `@implements REQ-NNN` annotations remain present and correct
- [ ] The commit message uses the `refactor:` type and states "no behavior change"

## Prompt Body

You are `@implementer`. The team wants a behavior-preserving structural improvement. Read the [`refactor-safely`](../skills/refactor-safely/SKILL.md) skill before starting. It defines the safety-net, small-step, and characterization-test procedures.

**Step 1: confirm the safety net.**
Check the target's line coverage. If it is below 80%, write characterization tests that lock in current behavior, including its quirks, before changing anything. Refactoring without tests is rewriting.

**Step 2: identify the code smell precisely.**
Choose from the catalog: `Long Method`, `Large Class`, `Primitive Obsession`, `Data Clumps`, `Feature Envy`, `Shotgun Surgery`, or `Divergent Change`. Cite one or two lines as evidence. The request "make it cleaner" will be rejected.

**Step 3: choose a Fowler transformation.**
Choose the matching transformation, such as `Extract Method`, `Extract Class`, `Replace Conditional with Polymorphism`, or `Introduce Parameter Object`. Apply exactly one transformation per commit.

**Step 4: run tests before changing anything.**
Confirm that tests pass. If any fail or are skipped, fix that first. Never refactor a broken build.

**Step 5: apply the transformation.**
Prefer the integrated development environment's (IDE) refactoring tools: `Extract`, `Rename`, and `Move`. Manual edits must preserve method signatures unless the transformation is `Change Function Declaration` with a migration plan.

**Step 6: run tests after each micro-step.**
The suite must stay green at every commit. If it fails and you do not know why, revert and take a smaller step. Move each `@implements REQ-NNN` annotation with its method.

**Step 7: stop when the code smell is gone.**
Do not refactor neighboring code. Each invocation corresponds to one conversation, one pull request, and one code smell.

If an actual behavior change or a new requirement emerges during refactoring, stop and route it to `/implement`, `/fix-bug`, or `/update-spec`. Do not fold it into this change.

## Example Invocation

```text
/refactor target=backend/src/main/java/com/example/app/fees/FeeService.java smell=long-method
```
