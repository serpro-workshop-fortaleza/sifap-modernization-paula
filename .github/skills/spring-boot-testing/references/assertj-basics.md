# AssertJ basics

Fluent assertions for readable, maintainable tests.

## Basic assertions

### Object equality

```java
assertThat(order.getStatus()).isEqualTo("PENDING");
assertThat(order.getId()).isNotEqualTo(0);
assertThat(order).isEqualTo(expectedOrder);
assertThat(order).isNotNull();
assertThat(nullOrder).isNull();
```

### String assertions

```java
assertThat(order.getDescription())
  .isEqualTo("Test Order")
  .startsWith("Test")
  .endsWith("Order")
  .contains("Test")
  .hasSize(10)
  .matches("[A-Za-z ]+");
```

### Number assertions

```java
assertThat(order.getAmount())
  .isEqualTo(99.99)
  .isGreaterThan(50)
  .isLessThan(100)
  .isBetween(50, 100)
  .isPositive()
  .isNotZero();
```

### Boolean assertions

```java
assertThat(order.isActive()).isTrue();
assertThat(order.isDeleted()).isFalse();
```

## Date and time assertions

```java
assertThat(order.getCreatedAt())
  .isEqualTo(LocalDateTime.of(2024, 1, 15, 10, 30))
  .isBefore(LocalDateTime.now())
  .isAfter(LocalDateTime.of(2024, 1, 1))
  .isCloseTo(LocalDateTime.now(), within(5, ChronoUnit.SECONDS));
```

## Optional assertions

```java
Optional<Order> maybeOrder = orderService.findById(1L);

assertThat(maybeOrder)
  .isPresent()
  .hasValueSatisfying(order -> {
    assertThat(order.getId()).isEqualTo(1L);
  });

assertThat(orderService.findById(999L)).isEmpty();
```

## Exception assertions

### JUnit 5 exception handling

```java
@Test
void shouldThrowException() {
  OrderService service = new OrderService();

  assertThatThrownBy(() -> service.findById(999L))
    .isInstanceOf(OrderNotFoundException.class)
    .hasMessage("Order 999 not found")
    .hasMessageContaining("999");
}
```

### AssertJ exception handling

```java
@Test
void shouldThrowExceptionWithCause() {
  assertThatExceptionOfType(OrderProcessingException.class)
    .isThrownBy(() -> service.processOrder(invalidOrder))
    .withCauseInstanceOf(ValidationException.class);
}
```

## Custom assertions

Create domain-specific assertions to reuse test code:

```java
public class OrderAssert extends AbstractAssert<OrderAssert, Order> {

  public static OrderAssert assertThat(Order actual) {
    return new OrderAssert(actual);
  }

  private OrderAssert(Order actual) {
    super(actual, OrderAssert.class);
  }

  public OrderAssert isPending() {
    isNotNull();
    if (!"PENDING".equals(actual.getStatus())) {
      failWithMessage("Expected order status PENDING but was %s", actual.getStatus());
    }
    return this;
  }

  public OrderAssert hasTotal(BigDecimal expected) {
    isNotNull();
    if (!expected.equals(actual.getTotal())) {
      failWithMessage("Expected total %s but was %s", expected, actual.getTotal());
    }
    return this;
  }
}
```

Usage:

```java
OrderAssert.assertThat(order)
  .isPending()
  .hasTotal(new BigDecimal("99.99"));
```

## Soft assertions

Collect multiple failures before stopping the test:

```java
@Test
void shouldValidateOrder() {
  Order order = orderService.findById(1L);

  SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(order.getId()).isEqualTo(1L);
    softly.assertThat(order.getStatus()).isEqualTo("PENDING");
    softly.assertThat(order.getItems()).isNotEmpty();
  });
}
```

## The `satisfies` pattern

```java
assertThat(order)
  .satisfies(o -> {
    assertThat(o.getId()).isPositive();
    assertThat(o.getStatus()).isNotBlank();
    assertThat(o.getCreatedAt()).isNotNull();
  });
```

## Usage with Spring

```java
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class OrderServiceTest {

  @Autowired
  private OrderService orderService;

  @Test
  void shouldCreateOrder() {
    Order order = orderService.create(new OrderRequest("Product", 2));

    assertThat(order)
      .isNotNull()
      .extracting(Order::getId, Order::getStatus)
      .containsExactly(1L, "PENDING");
  }
}
```

## Static import

Always use static imports to keep assertions clean:

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.catchThrowable;
```

## Key benefits

1. **Readable**: sentence-like structure
2. **Type-safe**: IDE autocomplete works
3. **Comprehensive API**: many built-in assertions
4. **Extensible**: custom assertions for your domain
5. **Better errors**: clear failure messages
