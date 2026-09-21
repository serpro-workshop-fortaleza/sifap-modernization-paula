---
name: "create-tests"
description: "Generate a complete JUnit 5 or Vitest test class for a REQ-ID, covering the expected path, boundaries, and negative cases."
argument-hint: "req=REQ-NNN class=<ClassUnderTest> framework=junit|vitest"
agent: "qa-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /create-tests

## Objective

Produce the test class for **one specific `REQ-ID`** in SIFAP 2.0. The output contains only ready-to-use JUnit 5 (Java) or Vitest (TypeScript) code and covers the happy path, boundaries, and negative cases. Tests are written *during* implementation, include the `REQ-ID` for continuous integration (CI) traceability, and fail with meaningful messages until production code exists. This prompt does not implement production code or edit the specification.

## When to Invoke

Immediately after `/test-strategy` assigns the `REQ-ID` to a layer, at the start of that requirement's red-green-refactor cycle. Use before writing production code so the test guides implementation.

## Preconditions

- The `REQ-ID` exists in `specs/<NNN>-<feature>/spec.md` with a complete EARS statement and acceptance criteria
- The target class or component has a name, even if it is still a skeleton
- The testing tool and existing reusable fixtures are known

## Inputs the Team Must Provide

- The `REQ-ID`, its complete EARS statement, and its acceptance criteria
- The class or component under test
- The tool: JUnit 5 + AssertJ + Mockito (backend) or Vitest + Testing Library (frontend)
- Existing fixtures or builders to reuse (`src/test/resources/fixtures/`, `__fixtures__/`)

Ask the user for any missing information.

## What I Will Do

- Read [`../skills/tdd-workflow/SKILL.md`](../skills/tdd-workflow/SKILL.md) and drive tests by behavior, not implementation
- Decompose the EARS statement into happy-path, boundary, and negative cases
- Reuse existing fixtures and never copy real PII
- Name each test by behavior and tag it with the `REQ-ID`
- Generate the complete, compilable test file, plus any new fixture builder
- Run the tests and report whether they fail for the right reason before implementation

## What I Will NOT Do

- Invent SIFAP behavior or expected values. Each assertion must derive from the EARS statement and acceptance criteria. Unknown legacy edge cases are flagged for the team, never assumed
- Write or modify production code (`@builder` / `@implementer`) or change the requirement (`@requirements-engineer`)
- Generate a test without a `REQ-ID` marker, because the `spec-traceability` job in `.github/workflows/spec-quality.yml` would not find it
- Put real PII or production credentials in fixtures
- Verify implementation details (private fields, exact SQL strings, or log message text) or use `Thread.sleep` / `setTimeout` for synchronization

## Output Format

Return inline for review, with no automatic commit:

1. A test plan mapping each acceptance criterion to a test method:

```markdown
| Acceptance criterion | Test method | Type |
|-----------------------|-----------------|------|
| A valid request is accepted | should_accept_when_input_is_valid | happy path |
| An amount below the minimum is rejected | should_reject_when_amount_below_minimum | boundary |
| A missing required field is rejected | should_reject_when_field_absent | negative |
```

2. The complete test file (illustrative format):

```java
@Tag("REQ-014") // spec-quality.yml looks for REQ-IDs in backend/src/test
class AmountRuleTest {

    @Test
    void should_reject_when_amount_below_minimum() {
        var rule = new AmountRule();

        var result = rule.evaluate(BigDecimal.ZERO);

        assertThat(result.rejected())
            .as("REQ-014: amounts at or below the minimum are rejected")
            .isTrue();
    }
}
```

3. Any new fixture builder, in a separate file.
4. The exact execution command, verified in the project, for example, `./mvnw test -Dtest=AmountRuleTest`.
5. The expected failure messages the team should see before implementation.

## Definition of Done

- [ ] Each acceptance criterion has at least one named test
- [ ] At least one boundary case and one negative case are included
- [ ] Each test includes the `REQ-ID` as a tag and in the assertion description
- [ ] Tests fail before implementation, for the right reason and with clear messages
- [ ] No production code is changed
- [ ] No real PII or production credentials appear in fixtures
- [ ] The test file compiles and runs in isolation

## Prompt Body

You are `@qa-engineer`. The team has a requirement and a skeleton. It needs failing tests that describe behavior before code is written.

**Step 1: load the test-driven development discipline.**
Read [`../skills/tdd-workflow/SKILL.md`](../skills/tdd-workflow/SKILL.md). Start with the simplest nontrivial case and add one variation at a time.

**Step 2: split the EARS statement into cases.**
Ubiquitous (`The system SHALL...`) → 1 happy path + 1 boundary. Event-driven (`WHEN...`) → 1 happy path + 1 negative ("the event did not occur, so nothing changes"). State-driven (`WHILE...`) → 1 case per transition (in the state, exiting the state, and reentry). Optional (`WHERE...`) → feature enabled and disabled. Unwanted (`IF..., THEN the system SHALL NOT...`) → at least 2 negative cases at different boundaries.

**Step 3: choose fixtures, not production data.**
Reuse existing builders and never copy real PII. Create fresh data for each test, with no shared mutable state between fixtures.

**Step 4: name tests by behavior.**
Use `should_<expected>_when_<condition>` (camelCase method names in JUnit and snake_case descriptions in Vitest). Structure the body as Arrange-Act-Assert or Given-When-Then so a reviewer can read it in ten seconds.

**Step 5: write complete assertions and tag the requirement.**
Use AssertJ chains (`assertThat(x).isEqualTo(y).as("REQ-XXX ...")`), never `assertTrue(x.equals(y))`. Tag with `@Tag("REQ-XXX")` in JUnit or `describe('REQ-XXX', ...)` in Vitest so `.github/workflows/spec-quality.yml` can trace the test.

**Step 6: mock only your own collaborators.**
Mock repositories, but not framework classes, value objects, or pure functions. Do not mock the class under test.

**Step 7: run the tests.**
Run the isolated command and confirm that each test fails with a meaningful message until `/speckit.implement` writes the production code. Report the exact command and expected failures.

Each test includes its `REQ-ID`, fails first for the right reason, and does not change production code. No real PII enters fixtures. If an expected value cannot be derived from the specification, mark it as a mystery with `@Disabled` and consult the team. Do not invent the value.

## Example Invocation

```text
/create-tests req=REQ-NNN class=<ClassUnderTest> framework=junit
```
