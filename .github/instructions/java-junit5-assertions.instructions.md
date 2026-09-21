---
description: "Use when writing or reviewing JUnit 5 (Jupiter) assertions in backend Java tests: expected-value ordering, lazy Supplier messages, assertAll grouping, assertThrows and assertThrowsExactly, timeouts, and assertInstanceOf."
applyTo: "**/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java"
---

# JUnit 5 assertions - Jupiter assertion conventions

This file activates for backend Java tests (`*Test.java`, `*IT.java`, `*Steps.java`, `*StepDefs.java`). It teaches correct use of JUnit Jupiter's built-in `org.junit.jupiter.api.Assertions` in Java 21: expected-value ordering, lazy failure messages, grouped assertions, exception and type checks, and timeouts. It teaches how to assert, but does not decide test strategy, slice selection, mocking policy, or coverage targets. Structure and the pyramid live in the [`java-junit`](../skills/java-junit/SKILL.md) skill, Spring slice and integration tests in the [`spring-boot-testing`](../skills/spring-boot-testing/SKILL.md) skill, and traceability and coverage in [`tests.instructions.md`](tests.instructions.md).

> [!NOTE]
> These are Jupiter's built-in `Assertions`. For fluent chains and advanced object or collection checks, the kit prefers AssertJ (`assertThat(...)`), as in [`tests.instructions.md`](tests.instructions.md) and the [`spring-boot-testing`](../skills/spring-boot-testing/SKILL.md) skill. Use the Jupiter assertions below for grouped, exception, timeout, exact-type, and simple equality checks.

## Static imports

Import each assertion statically so test methods express intent, not boilerplate. Prefer explicit imports over wildcards unless the module already standardizes on them.

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertAll;

assertEquals(expected, actual);
```

Always import from `org.junit.jupiter.api.Assertions`. Never mix in `org.junit.Assert` (JUnit 4): argument ordering differs, and the APIs are not interchangeable.

## Expected value first

`expected` is always the **first** argument, and `actual` the **second**, so the failure log correctly reports "expected X but got Y".

```java
// Avoid - reversed order; the failure message is misleading
assertEquals(resourceService.count(), 2);

// Prefer
assertEquals(2, resourceService.count());

// Unavoidable floating point (never money, which uses BigDecimal): provide a delta
assertEquals(0.3, 0.1 + 0.2, 1e-9);
```

> [!WARNING]
> `assertEquals` on `BigDecimal` uses `equals`, which is scale-sensitive: `new BigDecimal("10.0")` does **not** equal `new BigDecimal("10.00")`. For monetary amounts, compare the value with `assertEquals(0, expected.compareTo(actual))` or use AssertJ's `isEqualByComparingTo`.

## Failure messages: Supplier and String

Pass the message as `Supplier<String>` when construction is expensive, so the string is created only on failure. A constant literal can remain a `String`.

```java
// Avoid - the formatted message is created even when the assertion passes
assertEquals(expected, actual, "expected %s but got %s".formatted(expected, actual));

// Prefer - lazy evaluation, only on failure
assertEquals(expected, actual,
    () -> "expected %s but got %s".formatted(expected, actual));

// Appropriate - a constant literal incurs no additional cost
assertTrue(account.isActive(), "account must be active");
```

## Grouping with assertAll

Use `assertAll` to check multiple properties of a result; all assertions run even when an earlier one fails, showing every mismatch.

```java
record PaymentView(String beneficiary, BigDecimal amount, PaymentStatus status) {}

@Test
void should_map_all_fields_when_building_view() { // REQ-042
    PaymentView view = mapper.toView(payment);
    assertAll("payment view",
        () -> assertEquals("ACME LTDA", view.beneficiary()),
        () -> assertEquals(0, new BigDecimal("1500.00").compareTo(view.amount())),
        () -> assertEquals(PaymentStatus.APPROVED, view.status())
    );
}
```

Do not manually build a sequence of isolated assertions to check an object; the first failure hides the others.

## Exceptions: assertThrows and assertThrowsExactly

`assertThrows` returns the thrown exception for further checks and accepts subtypes of the expected class. Use `assertThrowsExactly` (JUnit 5.8+) when the exact class is part of the contract.

```java
@Test
void should_reject_duplicate_label_when_it_exists() { // REQ-021
    var request = new CreateResourceRequest("alpha", new BigDecimal("5.00"));
    ResourceConflictException ex = assertThrows(
        ResourceConflictException.class,
        () -> resourceService.create(request));
    assertEquals("alpha", ex.conflictingLabel());
}

// Exact type required - a subclass must NOT satisfy this assertion
assertThrowsExactly(IllegalArgumentException.class, () -> ResourceLabel.of(""));
```

## assertDoesNotThrow

Use `assertDoesNotThrow` only when absence of an exception is the contract under test; it returns the value for further assertions.

```java
BigDecimal total = assertDoesNotThrow(() -> invoiceService.total(batch));
assertEquals(0, new BigDecimal("2500.00").compareTo(total));
```

## Timeouts

Use `assertTimeout` to check a duration without interrupting the work. Use `assertTimeoutPreemptively` only when a hard abort is necessary.

```java
assertTimeout(Duration.ofSeconds(1), () -> reportService.generate(batch));

assertTimeoutPreemptively(Duration.ofMillis(500), () -> validator.check(payload));
```

> [!WARNING]
> `assertTimeoutPreemptively` runs code in a **separate thread**, so `ThreadLocal` state is not propagated. The bound `EntityManager` of a `@Transactional` test and any security context are absent. Never wrap a transactional persistence call in it.

## Type checks: assertInstanceOf

Prefer `assertInstanceOf` (JUnit 5.8+) over `assertTrue(x instanceof T)`; it fails with a useful message and returns the cast value, suitable for the kit's sealed result types.

```java
sealed interface PaymentResult permits Approved, Rejected {}

Approved approved = assertInstanceOf(Approved.class, paymentService.process(request));
assertEquals(42L, approved.paymentId());
```

## Collections and arrays

Use dedicated assertions so failures show an element-by-element diff instead of an opaque `false`.

```java
assertIterableEquals(List.of("alpha", "beta"), resourceService.labels()); // ordered deep diff
assertArrayEquals(expectedBytes, actualBytes);
```

## Conventions

| Rule | Rationale |
|---|---|
| `expected` first and `actual` second in `assertEquals` | The failure log correctly shows expected and actual values |
| Compare `BigDecimal` by value, not with `equals` | `equals` is scale-sensitive and silently fails for money |
| Wrap expensive messages in `Supplier<String>` | The message is created only when the assertion fails |
| Group related checks with `assertAll` | All properties are reported |
| `assertThrows` for hierarchy, `assertThrowsExactly` for exact class | Matches the contract's type strictness |
| `assertInstanceOf` instead of `assertTrue(... instanceof ...)` | Returns the cast value and fails with a useful message |
| Import only from `org.junit.jupiter.api.Assertions` | JUnit 4's `org.junit.Assert` uses different argument ordering |

## Do / Don't

| Do | Don't |
|---|---|
| Put `expected` before `actual` | Reverse them and produce misleading logs |
| Compare money with `compareTo` or `isEqualByComparingTo` | Compare `BigDecimal` with scale-sensitive `equals` |
| Use `assertEquals(2, result)` for values | Use `assertTrue(result == 2)` and lose the values in the log |
| Check the value when possible | Settle for `assertNotNull` when a real check is available |
| Use `Supplier` for expensive messages | Build a formatted message on every run |
| Avoid `assertTimeoutPreemptively` in transactional code | Wrap `@Transactional` persistence and lose the `EntityManager` |
| Let assertions fail clearly | Catch `AssertionError` to hide a failure |

## PR Checklist

- [ ] Every `assertEquals` lists `expected` first and `actual` second
- [ ] `BigDecimal` and other monetary amounts are compared by value, not with scale-sensitive `equals`
- [ ] Multiple-property checks use `assertAll`; expensive messages use `Supplier<String>`
- [ ] Exception tests deliberately choose `assertThrows` or `assertThrowsExactly` and check the returned exception
- [ ] `assertTimeoutPreemptively` wraps neither transactional nor `ThreadLocal`-bound code
- [ ] Imports are Jupiter-only; no mixing with `org.junit.Assert` (JUnit 4)
- [ ] Requirement-driven tests retain the inline `// REQ-NNN` comment (see [`tests.instructions.md`](tests.instructions.md))
