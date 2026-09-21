---
name: "tdd"
description: "Guide one behavior through a strict red-green-refactor cycle, producing separate commits for the red, green, and refactor phases."
argument-hint: "behavior=<behavior> req=REQ-NNN target=<file-or-class>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /tdd

## Objective

Produce a complete test-driven cycle for a single behavior, delivered in three separate commits: `red`, `green`, and `refactor`. No production code is written without a failing test, and no first test is written to pass immediately. The behavior must correspond to exactly one acceptance criterion of a `REQ-ID`.

> [!NOTE]
> One failing test at a time. Never maintain two `red` states. If the first test is hard to write, the design is revealing a problem.

## When to Invoke

Use during Stage 3 to discover or strengthen a small behavior, such as new logic, a boundary, or an edge case, when the design is not yet obvious and a test-first safety net adds the most value.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` contains the `REQ-ID` and acceptance criterion that the behavior corresponds to
- The current branch is `impl/<NNN>-<feature>`
- The testing framework is available: JUnit 5 + AssertJ (Java) or Vitest + Testing Library (TypeScript)
- The target module is already scaffolded, or this cycle creates its first class

## Inputs the Team Must Provide

- The behavior to discover, in plain language
- The linked `REQ-ID` in `specs/<NNN>-<feature>/spec.md`
- The target file or class (if it does not exist, say so. TDD also guides design, so creating it is acceptable)
- Ask the user for any missing item.

## What I Will Do

- Choose the simplest nontrivial case and write a failing test that names the behavior
- Confirm that the test fails for the right reason and commit the `red` state
- Write the smallest production code that makes the test pass, confirm that the full suite is green, and commit
- Refactor in the `green` state with a Fowler transformation, keep all tests passing, and commit
- Report the discovered behavior, the three commits, and the next test to write

## What I Will NOT Do

- Write the test and code together. That is verification, not TDD
- Keep two tests failing at the same time or skip the `refactor` phase
- Change behavior under the guise of refactoring. If an assertion changes, the cycle is invalid
- Test private methods or mock every dependency
- Invent an acceptance criterion absent from the specification. If the behavior has no `REQ-ID`, I will stop and route it to `/update-spec` instead of guessing
- Implement the suggested next test in this cycle

## Output Format

```markdown
### Discovered behavior
A tax-exempt payer receives a zero fee. (REQ-031, criterion 2)

### Commits
| Phase | Message | Files | Result |
|---|---|---|---|
| red | `test(fees): red - zero fee for an exempt payer` | `FeeServiceTest.java` | 1 failing |
| green | `feat(fees): green - implement REQ-031 (minimal)` | `FeeService.java` | 12 passing |
| refactor | `refactor(fees): extract the exemption check` | `FeeService.java` | 12 passing |

### Test file
<complete test source, with an inline `// REQ-031` comment>

### Production code
<complete source after the refactor phase>

### Suggestion for the next cycle
Add a boundary test: fee at the exemption threshold. (Not implemented here.)
```

## Definition of Done

- [ ] Three separate commits exist: `test:` (`red`), `feat:` (`green`), and `refactor:`
- [ ] The `red` commit is reproducibly red: checking it out makes the build fail
- [ ] The `green` commit contains the minimum needed to pass
- [ ] The `refactor` commit changes structure only. Test names and assertions remain unchanged
- [ ] The full suite finishes green
- [ ] The behavior corresponds to exactly one acceptance criterion of a `REQ-ID`, cited by an inline `// REQ-NNN` comment

## Prompt Body

You are `@implementer`. The team wants to discover a behavior starting with the test. Read the [`tdd-workflow`](../skills/tdd-workflow/SKILL.md) skill before starting. It defines the cycle, rules, and anti-patterns. Execute exactly three phases and do not combine them.

**Step 1: RED, write the failing test.**
Choose the simplest nontrivial case, not the empty case or the catastrophic case. Name the test `should_<expected>_when_<condition>` and add an inline `// REQ-NNN` comment. Use Arrange-Act-Assert, with blank lines between sections.

**Step 2: RED, confirm and commit.**
Run the test. Confirm that it fails and read the message to verify that the cause is expected (assertion or compilation, not a setup error). Commit with the message `test(<scope>): red - <behavior>`.

**Step 3: GREEN, write the smallest passing code.**
Write the minimum production code that makes the test pass. In the first cycle, faking it with a fixed value is allowed. Run the isolated test and then the full suite. Both must pass.

**Step 4: GREEN, commit.**
Commit with the message `feat(<scope>): green - implement REQ-NNN (minimal)`.

**Step 5: REFACTOR, improve while green.**
Look for duplication, misleading names, and primitive obsession. Apply a Fowler transformation: `Extract Method`, `Rename`, or `Inline Variable`. Run all tests after each micro-step. They must stay green.

**Step 6: REFACTOR, commit and stop.**
Commit with the message `refactor(<scope>): <description>`. Stop when the design is suitable for the next cycle, without seeking perfection.

**Step 7: report and hand off.**
State the discovered behavior in one sentence, list the three commits, and identify the next test (boundary, error, or second variation) without implementing it.

Never return `null`, never use `any`, and mask CPF or benefit amounts in any log line. If the behavior does not correspond to a `REQ-ID`, stop and route it to `/update-spec`. Do not invent the requirement.

## Example Invocation

```text
/tdd behavior="zero fee for a tax-exempt payer" req=REQ-031 target=FeeService
```
