---
name: "java-junit"
description: "Write effective JUnit 5 unit and parameterized tests, delegating the best-practices checklist to the java-junit skill."
argument-hint: "class=<ClassUnderTest>"
agent: "qa-engineer"
tools: ["read", "search", "edit"]
---
# /java-junit

## Objective

Produce focused plain and parameterized JUnit 5 tests for a class or behavior. Follow Arrange-Act-Assert, descriptive naming, proper isolation, and REQ-ID traceability. The best-practices checklist is in the [`java-junit`](../skills/java-junit/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 backend without repeating it.

> [!IMPORTANT]
> Write tests alongside the code, never afterward. The kit prohibits retrofitted tests.

## When to Invoke

During Stages 3 or 4, when implementing backend business logic, after the behavior under test is defined by a REQ-ID and its acceptance criteria.

## Preconditions

- The class or behavior under test exists or is being written in the same change
- The backend module has `junit-jupiter` and `testcontainers` on the test classpath
- The REQ-IDs that the tests must cover are known

## Inputs the Team Must Provide

- `class`: the class or behavior under test, for example, `PaymentService`
- The REQ-IDs and acceptance criteria that the tests must satisfy
- Ask the user for any missing information.

## What I Will Do

- Follow the JUnit 5 practices in the [`java-junit`](../skills/java-junit/SKILL.md) skill and apply them to the class under test
- Write one test per acceptance criterion, named `should_<expected>_when_<condition>`, each with a `// REQ-NNN` comment in the code
- Use `@ParameterizedTest` with `@MethodSource` or `@CsvSource` for data-driven cases and Mockito for collaborators
- Use Testcontainers with real PostgreSQL 16 for anything that accesses the database

## What I Will NOT Do

- Write tests after production code or omit a case for any acceptance criterion
- Replace Testcontainers PostgreSQL with an in-memory database in the integration path
- Test multiple behaviors in one method or depend on execution order
- Leave a test without a REQ-ID comment, as this breaks `spec-traceability`

## Output Format

A JUnit 5 test class with each case traceable to a REQ-ID:

```java
// REQ-042: reject inactive beneficiary
@Test
@DisplayName("rejects a payment line for an inactive beneficiary")
void should_reject_when_beneficiary_is_inactive() {
    // Arrange - Act - Assert
}
```

## Definition of Done

- [ ] There is a test for each acceptance criterion of all related REQ-IDs
- [ ] Each test contains a `// REQ-NNN` comment
- [ ] Data-driven cases use `@ParameterizedTest`; collaborators are mocked
- [ ] Database tests use Testcontainers and `./mvnw test` passes

## Prompt Body

The [`java-junit`](../skills/java-junit/SKILL.md) skill defines conventions for plain and parameterized tests. Read it and apply them to the class under test.

**Step 1 — Map the behavior.**
List each acceptance criterion of the related REQ-IDs. Each criterion becomes a test.

**Step 2 — Apply the skill.**
Write tests according to the skill: AAA, `@DisplayName`, `assertAll`, `assertThrows`, and `@ParameterizedTest`. Mock collaborators with Mockito.

**Step 3 — Follow the kit's rules.**
Use Testcontainers with PostgreSQL 16 for database paths, add a `// REQ-NNN` comment to each test, and run `./mvnw test`.

**Step 4 — Verify.**
Run the suite and confirm that each case passes for the right reason.

## Example Invocation

```text
/java-junit class=PaymentService
```
