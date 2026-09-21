# @MockitoBean

Mocking dependencies in Spring Boot tests (replaces deprecated @MockBean in Spring Boot 4+).

## Overview

`@MockitoBean` replaces the deprecated `@MockBean` annotation in Spring Boot 4.0+. It creates a Mockito mock and registers it in the Spring context, replacing any existing bean of the same type.

## Basic usage

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @MockitoBean
  private OrderService orderService;

  @MockitoBean
  private UserService userService;
}
```

## Supported test slices

- `@WebMvcTest`: mocks service or repository dependencies
- `@WebFluxTest`: mocks reactive service dependencies
- `@SpringBootTest`: replaces real beans with mocks

## Method stubbing

### Basic stub

```java
@Test
void shouldReturnOrder() {
  Order order = new Order(1L, "PENDING");
  given(orderService.findById(1L)).willReturn(order);

  // Test code
}
```

### Multiple returns

```java
given(orderService.findById(anyLong()))
  .willReturn(new Order(1L, "PENDING"))
  .willReturn(new Order(2L, "COMPLETED"));
```

### Throwing exceptions

```java
given(orderService.findById(999L))
  .willThrow(new OrderNotFoundException(999L));
```

### Argument matching

```java
given(orderService.create(argThat(req -> req.getQuantity() > 0)))
  .willReturn(1L);

given(orderService.findByStatus(eq("PENDING")))
  .willReturn(List.of(new Order()));
```

## Verifying interactions

### Verify the method was called

```java
verify(orderService).findById(1L);
```

### Verify it was never called

```java
verify(orderService, never()).delete(any());
```

### Verify the count

```java
verify(orderService, times(2)).findById(anyLong());
verify(orderService, atLeastOnce()).findByStatus(anyString());
```

### Verify the order

```java
InOrder inOrder = inOrder(orderService, userService);
inOrder.verify(orderService).findById(1L);
inOrder.verify(userService).getUser(any());
```

## Resetting mocks

Mocks are automatically reset between tests. To reset during a test:

```java
Mockito.reset(orderService);
```

## @MockitoSpyBean for partial mocking

Use `@MockitoSpyBean` to wrap a real bean with Mockito.

```java
@SpringBootTest
class OrderServiceIntegrationTest {

  @MockitoSpyBean
  private PaymentGatewayClient paymentClient;

  @Test
  void shouldProcessOrder() {
    doReturn(true).when(paymentClient).processPayment(any());

    // Tests with the real service but a mocked payment client
  }
}
```

## @TestBean for custom test beans

Register a custom bean instance in the test context:

```java
@SpringBootTest
class OrderServiceTest {

  @TestBean
  private PaymentGatewayClient paymentClient() {
    return new FakePaymentClient();
  }
}
```

## Scope: singleton versus prototype

Spring Framework 7+ (Spring Boot 4+) allows mocking non-singleton beans:

```java
@Component
@Scope("prototype")
public class OrderProcessor {
  public String process() { return "real"; }
}

@SpringBootTest
class OrderServiceTest {
  @MockitoBean
  private OrderProcessor orderProcessor;

  @Test
  void shouldWorkWithPrototype() {
    given(orderProcessor.process()).willReturn("mocked");
    // Test code
  }
}
```

## Common patterns

### Mocking a repository in a service test

```java
@SpringBootTest
class OrderServiceTest {
  @MockitoBean
  private OrderRepository orderRepository;

  @Autowired
  private OrderService orderService;

  @Test
  void shouldCreateOrder() {
    given(orderRepository.save(any())).willReturn(new Order(1L));

    Long id = orderService.createOrder(new OrderRequest());

    assertThat(id).isEqualTo(1L);
    verify(orderRepository).save(any(Order.class));
  }
}
```

### Multiple mocks of the same type

Use bean names:

```java
@MockitoBean(name = "primaryDataSource")
private DataSource primaryDataSource;

@MockitoBean(name = "secondaryDataSource")
private DataSource secondaryDataSource;
```

## Migrating from @MockBean

### Before (deprecated)

```java
@MockBean
private OrderService orderService;
```

### After (Spring Boot 4+)

```java
@MockitoBean
private OrderService orderService;
```

## Key differences from Mockito's @Mock

| Feature | @MockitoBean | @Mock |
| ------- | ------------ | ----- |
| Context integration | Yes | No |
| Spring lifecycle | Participates | None |
| Works with @Autowired | Yes | No |
| Test slice support | Yes | Limited |

## Best practices

1. Use `@MockitoBean` only when there is a Spring context
2. In pure unit tests, use Mockito's `@Mock` or `Mockito.mock()`
3. Always verify interactions with side effects
4. Do not verify simple queries (stubbing is sufficient)
5. Reset mocks if the test changes shared state
