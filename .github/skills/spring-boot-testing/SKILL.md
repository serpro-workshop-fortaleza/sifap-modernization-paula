---
name: "spring-boot-testing"
description: "Select the right Spring Boot testing technique for a scenario: slices (@WebMvcTest, @DataJpaTest, @RestClientTest, @JsonTest, @SpringBootTest), Testcontainers, Mockito, and AssertJ. Use when writing or reviewing Spring Boot integration or slice tests. Targets the kit's Spring Boot 3.3 + JUnit 5; newer 3.4+/4.0 APIs (MockMvcTester, @MockitoBean, RestTestClient) are out of scope."
---
# Spring Boot testing

This skill helps choose the right Spring Boot testing technique for a scenario. It targets the kit's **Spring Boot 3.3 + JUnit 5 + Testcontainers** stack. Some newer Spring Boot 3.4+/4.0 APIs appear only as references and are clearly marked **out of scope for the kit**. For plain business-logic unit tests without a Spring context, use [`java-junit`](../java-junit/SKILL.md).

## When to Invoke

- "Which test slice should I use for this controller?"
- "Write a `@DataJpaTest` against real PostgreSQL with Testcontainers."
- "Review the layer and scope of these Spring Boot tests."
- "Set up Testcontainers for our integration tests."

## Core principles

1. **Test pyramid**: unit (fast) > slice (focused) > integration (full)
2. **Right tool**: use the narrowest slice that provides confidence
3. **AssertJ style**: prefer fluent, readable assertions to verbose matchers
4. **Kit stack**: on Spring Boot 3.3, use classic MockMvc and `@MockBean`; newer MockMvcTester / `@MockitoBean` / RestTestClient APIs (3.4+/4.0) are out of scope

## Which test slice should you use?

| Scenario | Annotation | Reference |
|----------|------------|-----------|
| Controller + HTTP semantics | `@WebMvcTest` | [references/webmvctest.md](references/webmvctest.md) |
| Repository + JPA queries | `@DataJpaTest` | [references/datajpatest.md](references/datajpatest.md) |
| REST client + external APIs | `@RestClientTest` | [references/restclienttest.md](references/restclienttest.md) |
| JSON (de)serialization | `@JsonTest` | [references/test-slices-overview.md](references/test-slices-overview.md) |
| Full application | `@SpringBootTest` | [references/test-slices-overview.md](references/test-slices-overview.md) |

## Test slice reference

- [references/test-slices-overview.md](references/test-slices-overview.md): decision and comparison matrix
- [references/webmvctest.md](references/webmvctest.md): web layer with MockMvc
- [references/datajpatest.md](references/datajpatest.md): data layer with Testcontainers
- [references/restclienttest.md](references/restclienttest.md): REST client tests

## Testing tool reference

- [references/mockmvc-classic.md](references/mockmvc-classic.md): classic MockMvc, the kit's default on Spring Boot 3.3
- [references/mockmvc-tester.md](references/mockmvc-tester.md): AssertJ-style MockMvc (Spring Boot 3.4+, out of scope)
- [references/mockitobean.md](references/mockitobean.md): mocks with `@MockitoBean` (Spring Boot 3.4+, out of scope)
- [references/resttestclient.md](references/resttestclient.md): RestTestClient (Spring Boot 4.0, out of scope)

## Assertion libraries

- [references/assertj-basics.md](references/assertj-basics.md): scalars, strings, booleans, and dates
- [references/assertj-collections.md](references/assertj-collections.md): lists, sets, maps, and arrays

## Testcontainers

- [references/testcontainers-jdbc.md](references/testcontainers-jdbc.md): PostgreSQL 16 and other JDBC databases

## Test data generation

- [references/instancio.md](references/instancio.md): generating complex test objects (3 or more properties)

## Performance and migration

- [references/context-caching.md](references/context-caching.md): speeding up test suites
- [references/sb4-migration.md](references/sb4-migration.md): Spring Boot 4.0 changes

## Quick decision tree

```text
Testing a controller endpoint?
  Yes → @WebMvcTest with classic MockMvc (MockMvcTester requires Spring Boot 3.4+)

Testing repository queries?
  Yes → @DataJpaTest with Testcontainers (real database)

Testing business logic in the service?
  Yes → Plain JUnit + Mockito (no Spring context)

Testing an external API client?
  Yes → @RestClientTest with MockRestServiceServer

Testing JSON mapping?
  Yes → @JsonTest

Need a full integration test?
  Yes → @SpringBootTest with minimal context configuration
```

## Newer APIs outside the kit's scope (Spring Boot 3.4+/4.0)

The kit is pinned to **Spring Boot 3.3 + JUnit 5**. The following newer APIs are listed
for awareness only. Do not adopt them in the kit's code:

- **MockMvcTester**: AssertJ-style MockMvc assertions (Spring Boot 3.4+). On 3.3, use classic MockMvc.
- **@MockitoBean**: replaces `@MockBean` (Spring Boot 3.4+). On 3.3, use `@MockBean`.
- **RestTestClient**: alternative to `TestRestTemplate` (Spring Boot 4.0). On 3.3, use `TestRestTemplate` or `RestClient`.
- **Modular test starters** and **context pausing** (Spring Boot 4.0 / Spring Framework 7).

Consult [references/sb4-migration.md](references/sb4-migration.md) only if the project is actually upgraded beyond 3.3.

## Testing best practices

### Assessing code complexity

When a method or class is too complex to test effectively:

1. **Analyze complexity**: if more than five to seven test cases are needed to cover a single method, it is probably too complex
2. **Recommend refactoring**: suggest splitting the code into smaller, focused functions
3. **Respect the user's decision**: if they agree to refactor, help identify extraction points
4. **Proceed if necessary**: if they choose to keep the complex code, implement tests despite the difficulty

**Example refactoring recommendation:**

```java
// Before: complex method that is hard to test
public Order processOrder(OrderRequest request) {
  // Validation, discount calculation, payment, inventory, notification...
  // More than 50 lines with mixed responsibilities
}

// After: refactored into testable units
public Order processOrder(OrderRequest request) {
  validateOrder(request);
  var order = createOrder(request);
  applyDiscount(order);
  processPayment(order);
  updateInventory(order);
  sendNotification(order);
  return order;
}
```

### Avoid code repetition

Create helper methods for frequently used objects and mock setup, improving readability and maintainability.

### Test organization with @DisplayName

Use descriptive display names to clarify test intent:

```java
@Test
@DisplayName("Should calculate the discount for a VIP customer")
void shouldCalculateDiscountForVip() { }

@Test
@DisplayName("Should reject the order when the customer has insufficient credit")
void shouldRejectOrderForInsufficientCredit() { }
```

### Test coverage order

Always structure tests in this order:

1. **Main scenario**: happy path, most common use case
2. **Other paths**: alternative valid scenarios and boundary cases
3. **Exceptions/errors**: invalid inputs, error conditions, and failure modes

### Test production scenarios

Write tests with real production scenarios in mind. This makes tests easier to understand and helps explain code behavior in real cases.

### Test coverage targets

Aim for 80% code coverage as a practical balance between quality and effort. Higher coverage is beneficial but is not the only goal.

Use the JaCoCo Maven plugin to generate reports and track coverage.

**Coverage rules:**

- Minimum coverage of 80%
- Focus on meaningful assertions, not just execution

**What to prioritize:**

1. Critical business flows (payment processing, order validation)
2. Complex algorithms (pricing, discount calculation)
3. Error handling (exceptions, boundary cases)
4. Integration points (external APIs, databases)

## Dependencies (Spring Boot 3.3)

`spring-boot-starter-test` already includes JUnit 5, Mockito, AssertJ, and MockMvc. Add the
Testcontainers support module to run `@DataJpaTest` / `@SpringBootTest` against real PostgreSQL 16.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>

<!-- Testcontainers support (real PostgreSQL for @DataJpaTest / @SpringBootTest) -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <scope>test</scope>
</dependency>
```

## Output Template

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class PaymentRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    PaymentRepository repository;

    @Test
    void findsByStatus() {
        repository.save(new Payment("PENDING"));
        assertThat(repository.findByStatus("PENDING")).hasSize(1);
    }
}
```

## Quality Gate

- [ ] The narrowest slice that provides confidence is used (unit -> slice -> `@SpringBootTest`).
- [ ] Data-layer and full integration tests run against real PostgreSQL 16 through Testcontainers, not H2.
- [ ] On Spring Boot 3.3, classic `MockMvc` and `@MockBean` are used; no 3.4+/4.0 API (MockMvcTester, `@MockitoBean`, RestTestClient) is adopted.
- [ ] Assertions use AssertJ's `assertThat`; each test focuses on one behavior.
- [ ] The suite reuses the Spring context where possible (see context-caching) to stay fast.
- [ ] `./mvnw test` passes locally before opening the PR.
