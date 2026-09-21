---
name: "tdd-workflow"
description: "Use when practicing test-driven development, writing a failing test first, or guiding the red-green-refactor cycle. Triggers include \"TDD\", \"red-green-refactor cycle\", \"test first\", \"failing test\", and \"write a test\"."
---
# TDD workflow

## When to Invoke

- When starting a new behavior or bug fix.
- When pair or mob programming on unfamiliar code and needing a safety net.
- When changes keep causing unexpected failures.

## The cycle

```text
RED -> write the smallest failing test that expresses the next behavior
GREEN -> write the least code that makes the test pass
REFACTOR -> improve the design while tests stay green
```

Commit at each green step. Cover one behavior per cycle.

## Rules

1. **Do not write production code without a failing test.** No test, no change.
2. **Keep only one failing test at a time.** Never have two red tests.
3. **Take the smallest step that fails.** If the first test is hard to write, the design is signaling a problem.
4. **Test names describe behavior**, not implementation: `calculates_tax_for_tax_exempt_customer`, not `test_method1`.
5. Use the **Given-When-Then / Arrange-Act-Assert** structure in the test body.
6. **The refactoring phase is not optional**. It holds most of the value.

## How to choose the next test

Order tests to guide the design:

- Start with the simplest nontrivial case (the "0->1" case or the happy path with one input).
- Then add a single variation (a boundary, a branch, or an error).
- Avoid writing a huge test that covers everything.

## Fakes and stubs

- Use a test double only when the real collaborator is slow, nondeterministic, or does not exist yet.
- Do not mock types you do not own. Wrap them in a thin abstraction first.
- A test that mocks everything tests nothing.

## When TDD is difficult, the problem is often in the design

- Difficulty constructing the object under test: too many collaborators, violation of the single-responsibility principle (SRP).
- Inability to make an assertion without reading three other objects: Law of Demeter or encapsulation issue.
- Needing to mock the whole world: hidden coupling; introduce an abstraction.

## Anti-patterns

- Writing code and then the test (that is verification, not TDD).
- Skipping the refactoring phase.
- Tests that duplicate the implementation (change detectors).
- Huge test fixtures shared across files, because they are brittle.
- Checking implementation details (private methods or exact SQL strings).

## Output Template

```java
// REQ-NNN: <behavior under test>
@Test
void calculatesTaxForTaxExemptCustomer() {
    // Arrange
    var customer = new Customer(TAX_EXEMPT);
    // Act
    var tax = calculator.taxFor(customer);
    // Assert
    assertThat(tax).isEqualTo(Money.ZERO);
}
```

Commit sequence per behavior: `red: add failing test` -> `green: make it pass` -> `refactor: <improvement>`.

## Quality Gate

- [ ] No production code was written without a failing test first.
- [ ] Only one test is red at a time, and each cycle covers one behavior.
- [ ] The refactoring step was performed while tests were green.
- [ ] Test names describe behavior and reference the REQ-ID in a comment.

## References

- [Kent Beck - Test Driven Development: By Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [GOOS - Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [Martin Fowler - Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
