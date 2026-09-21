---
name: "java-junit"
description: "Best practices for JUnit 5 unit tests: Arrange-Act-Assert structure, lifecycle, parameterized and data-driven tests, assertions, Mockito isolation, and organization. Use when writing or reviewing plain JUnit 5 unit tests for Java business logic. For Spring Boot slice or integration tests (@WebMvcTest, @DataJpaTest, Testcontainers), use spring-boot-testing."
---
# JUnit 5 best practices

Write focused JUnit 5 unit tests for SIFAP 2.0 backend business logic (Java 21 + Spring Boot 3.3). Cover standard and data-driven approaches with Mockito isolation and AssertJ assertions. For Spring Boot slice or integration tests (`@WebMvcTest`, `@DataJpaTest`, Testcontainers), use the [`spring-boot-testing`](../spring-boot-testing/SKILL.md) skill. For the red-green-refactor cycle, see [`tdd-workflow`](../tdd-workflow/SKILL.md).

## When to Invoke

- "Write JUnit 5 tests for this service."
- "Add a parameterized test covering these boundary values."
- "Review these unit tests' isolation and names."
- "Cover this business method's error paths."

## Project setup

- Use the standard Maven or Gradle layout and place tests in `src/test/java`.
- `spring-boot-starter-test` already includes JUnit 5 (including `junit-jupiter-params`), Mockito, and AssertJ in the kit's stack. No additional test dependency is required.
- Run tests with `./mvnw test` (or `./gradlew test`).

## Test structure

- Test classes must have the `Test` suffix, for example, `CalculatorTest` for a `Calculator` class.
- Use `@Test` on test methods.
- Follow the Arrange-Act-Assert pattern.
- Name tests using a descriptive convention, such as `methodName_should_expectedBehavior_when_scenario`.
- Use `@BeforeEach` and `@AfterEach` for per-test setup and cleanup.
- Use `@BeforeAll` and `@AfterAll` for per-class setup and cleanup. These methods must be static.
- Use `@DisplayName` to provide human-readable names for test classes and methods.
- Reference the tested requirement with a `// REQ-NNN` comment. The kit traces tests to REQ-IDs.

## Standard tests

- Keep each test focused on a single behavior.
- Avoid testing multiple conditions in the same test method.
- Create independent, idempotent tests that can run in any order.
- Avoid interdependencies between tests.

## Data-driven (parameterized) tests

Mark the method with `@ParameterizedTest` instead of `@Test` and supply arguments with a source annotation:

| Source | Usage |
|---|---|
| `@ValueSource` | One parameter of simple literals (strings and integers) |
| `@CsvSource` | Inline rows of comma-separated values (multiple parameters) |
| `@CsvFileSource` | Rows loaded from a CSV file on the classpath |
| `@MethodSource` | Arguments created by a factory method returning `Stream` or `Collection` |
| `@EnumSource` | All constants, or a named subset, of an enum |

## Assertions

- Prefer AssertJ's fluent `assertThat(...)` for readable failures. It is already on the kit's classpath.
- JUnit's `org.junit.jupiter.api.Assertions` methods (`assertEquals`, `assertTrue`, `assertNotNull`) remain available.
- Use `assertThrows` (or AssertJ's `assertThatThrownBy`) to verify exceptions.
- Group related assertions with `assertAll` to check all of them before the test fails.
- Use descriptive assertion messages to clarify the failure.

## Mocks and isolation

- Use a mocking framework such as Mockito to create mocks for dependencies.
- Use Mockito's `@Mock` and `@InjectMocks` annotations to simplify mock creation and injection.
- Use interfaces to make mocking easier.

## Test organization

- Group tests by feature or component using packages.
- Use `@Tag` to categorize tests, for example, `@Tag("fast")` and `@Tag("integration")`.
- Use `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` and `@Order` to control execution order only when strictly necessary.
- Use `@Disabled` to temporarily skip a test method or class and always state the reason.
- Use `@Nested` to group related tests in a nested inner class.

## Output Template

```java
// REQ-042: tax is zero for a tax-exempt customer
@ExtendWith(MockitoExtension.class)
class TaxCalculatorTest {

    @Mock TaxRateProvider rateProvider;
    @InjectMocks TaxCalculator calculator;

    @Test
    @DisplayName("returns zero tax for a tax-exempt customer")
    void returnsZeroForTaxExemptCustomer() {
        // Arrange
        var customer = new Customer(Status.TAX_EXEMPT);
        // Act
        var tax = calculator.taxFor(customer);
        // Assert
        assertThat(tax).isEqualTo(Money.ZERO);
    }

    @ParameterizedTest(name = "income {0} -> tax {1}")
    @CsvSource({ "1000, 100", "2000, 200" })
    void appliesFlatRate(BigDecimal income, BigDecimal expected) {
        when(rateProvider.ratePercent()).thenReturn(new BigDecimal("10"));
        assertThat(calculator.taxFor(income)).isEqualByComparingTo(expected);
    }
}
```

## Quality Gate

- [ ] Each test checks one behavior and runs independently of the others, in any order.
- [ ] Test names describe behavior, and the class contains a `// REQ-NNN` traceability comment.
- [ ] Boundary cases and error paths are covered, not just the happy path.
- [ ] Collaborators are isolated with Mockito; no unit test uses a real database, clock, or network.
- [ ] Assertions are meaningful (AssertJ's `assertThat`), not just "does not throw".
- [ ] `./mvnw test` passes locally before opening the PR.
