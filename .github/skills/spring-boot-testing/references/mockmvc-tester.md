# MockMvcTester

AssertJ-style Spring MVC controller tests (Spring Boot 3.4+).

## Overview

MockMvcTester provides fluent AssertJ-style assertions for web-layer tests. It is more readable and type-safe than traditional MockMvc.

**Recommended pattern**: convert JSON to real objects and assert them with AssertJ:

```java
assertThat(mvc.get().uri("/orders/1"))
  .hasStatus(HttpStatus.OK)
  .bodyJson()
  .convertTo(OrderResponse.class)
  .satisfies(response -> {
    assertThat(response.getTotalToPay()).isEqualTo(expectedAmount);
    assertThat(response.getItems()).isNotEmpty();
  });
```

## Basic usage

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @Autowired
  private MockMvcTester mvc;

  @MockitoBean
  private OrderService orderService;
}
```

## Recommended: object conversion pattern

### Single-object response

```java
@Test
void shouldGetOrder() {
  given(orderService.findById(1L)).willReturn(new Order(1L, "PENDING", 99.99));

  assertThat(mvc.get().uri("/orders/1"))
    .hasStatus(HttpStatus.OK)
    .bodyJson()
    .convertTo(OrderResponse.class)
    .satisfies(response -> {
      assertThat(response.getId()).isEqualTo(1L);
      assertThat(response.getStatus()).isEqualTo("PENDING");
      assertThat(response.getTotalToPay()).isEqualTo(new BigDecimal("99.99"));
    });
}
```

### List response

```java
@Test
void shouldGetAllOrders() {
  given(orderService.findAll()).willReturn(Arrays.asList(
    new Order(1L, "PENDING"),
    new Order(2L, "COMPLETED")
  ));

  assertThat(mvc.get().uri("/orders"))
    .hasStatus(HttpStatus.OK)
    .bodyJson()
    .convertTo(new TypeReference<List<OrderResponse>>() {})
    .satisfies(orders -> {
      assertThat(orders).hasSize(2);
      assertThat(orders.get(0).getStatus()).isEqualTo("PENDING");
      assertThat(orders.get(1).getStatus()).isEqualTo("COMPLETED");
    });
}
```

### Nested objects

```java
@Test
void shouldGetOrderWithCustomer() {
  assertThat(mvc.get().uri("/orders/1"))
    .hasStatus(HttpStatus.OK)
    .bodyJson()
    .convertTo(OrderResponse.class)
    .satisfies(response -> {
      assertThat(response.getCustomer()).isNotNull();
      assertThat(response.getCustomer().getName()).isEqualTo("John Doe");
      assertThat(response.getCustomer().getAddress().getCity()).isEqualTo("Berlin");
    });
}
```

### Complex assertions

```java
@Test
void shouldCalculateOrderTotal() {
  assertThat(mvc.get().uri("/orders/1/calculate"))
    .hasStatus(HttpStatus.OK)
    .bodyJson()
    .convertTo(CalculationResponse.class)
    .satisfies(calc -> {
      assertThat(calc.getSubtotal()).isEqualTo(new BigDecimal("100.00"));
      assertThat(calc.getTax()).isEqualTo(new BigDecimal("19.00"));
      assertThat(calc.getTotalToPay()).isEqualTo(new BigDecimal("119.00"));
      assertThat(calc.getItems()).allMatch(item -> item.getPrice().compareTo(BigDecimal.ZERO) > 0);
    });
}
```

## HTTP methods

### POST with a request body

```java
@Test
void shouldCreateOrder() {
  given(orderService.create(any())).willReturn(1L);

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content("{\"product\": \"Laptop\", \"quantity\": 2}"))
    .hasStatus(HttpStatus.CREATED)
    .hasHeader("Location", "/orders/1");
}
```

### PUT request

```java
@Test
void shouldUpdateOrder() {
  assertThat(mvc.put().uri("/orders/1")
    .contentType(MediaType.APPLICATION_JSON)
    .content("{\"status\": \"COMPLETED\"}"))
    .hasStatus(HttpStatus.OK);
}
```

### DELETE request

```java
@Test
void shouldDeleteOrder() {
  assertThat(mvc.delete().uri("/orders/1"))
    .hasStatus(HttpStatus.NO_CONTENT);
}
```

## Status assertions

```java
assertThat(mvc.get().uri("/orders/1"))
  .hasStatusOk()                    // 200
  .hasStatus(HttpStatus.OK)         // 200
  .hasStatus2xxSuccessful()         // 2xx
  .hasStatusBadRequest()            // 400
  .hasStatusNotFound()              // 404
  .hasStatusUnauthorized()          // 401
  .hasStatusForbidden()             // 403
  .hasStatus(HttpStatus.CREATED);   // 201
```

## Content type assertions

```java
assertThat(mvc.get().uri("/orders/1"))
  .hasContentType(MediaType.APPLICATION_JSON)
  .hasContentTypeCompatibleWith(MediaType.APPLICATION_JSON);
```

## Header assertions

```java
assertThat(mvc.post().uri("/orders"))
  .hasHeader("Location", "/orders/123")
  .hasHeader("X-Request-Id", matchesPattern("[a-z0-9-]+"));
```

## Alternative: JSON Path (use sparingly)

Use only when conversion to a typed object is not possible:

```java
assertThat(mvc.get().uri("/orders/1"))
  .hasStatusOk()
  .bodyJson()
  .extractingPath("$.customer.address.city")
  .asString()
  .isEqualTo("Berlin");
```

## Request parameters

```java
// Query parameters
assertThat(mvc.get().uri("/orders?status=PENDING&page=0"))
  .hasStatusOk();

// Path parameters
assertThat(mvc.get().uri("/orders/{id}", 1L))
  .hasStatusOk();

// Headers
assertThat(mvc.get().uri("/orders/1")
  .header("X-Api-Key", "secret"))
  .hasStatusOk();
```

## Request body with JacksonTester

```java
@Autowired
private JacksonTester<OrderRequest> json;

@Test
void shouldCreateOrder() {
  OrderRequest request = new OrderRequest("Laptop", 2);

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json.write(request).getJson()))
    .hasStatus(HttpStatus.CREATED);
}
```

## Error responses

```java
@Test
void shouldReturnValidationErrors() {
  given(orderService.findById(999L))
    .willThrow(new OrderNotFoundException(999L));

  assertThat(mvc.get().uri("/orders/999"))
    .hasStatus(HttpStatus.NOT_FOUND)
    .bodyJson()
    .convertTo(ErrorResponse.class)
    .satisfies(error -> {
      assertThat(error.getMessage()).isEqualTo("Order 999 not found");
      assertThat(error.getCode()).isEqualTo("ORDER_NOT_FOUND");
    });
}
```

## Testing validation errors

```java
@Test
void shouldRejectInvalidOrder() {
  OrderRequest invalidRequest = new OrderRequest("", -1);

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json.write(invalidRequest).getJson()))
    .hasStatus(HttpStatus.BAD_REQUEST)
    .bodyJson()
    .convertTo(ValidationErrorResponse.class)
    .satisfies(errors -> {
      assertThat(errors.getFieldErrors()).hasSize(2);
      assertThat(errors.getFieldErrors())
        .extracting("field")
        .contains("product", "quantity");
    });
}
```

## Comparison: MockMvcTester versus classic MockMvc

| Feature | MockMvcTester | Classic MockMvc |
| ------- | ------------- | --------------- |
| Style | Fluent AssertJ | MockMvc matchers |
| Readability | High | Medium |
| Type safety | Better | Lower |
| IDE support | Excellent | Good |
| Object conversion | Native | Manual |

## Migrating from classic MockMvc

### Before (classic)

```java
mvc.perform(get("/orders/1"))
  .andExpect(status().isOk())
  .andExpect(jsonPath("$.status").value("PENDING"))
  .andExpect(jsonPath("$.totalToPay").value(99.99));
```

### After (Tester with object conversion)

```java
assertThat(mvc.get().uri("/orders/1"))
  .hasStatus(HttpStatus.OK)
  .bodyJson()
  .convertTo(OrderResponse.class)
  .satisfies(response -> {
    assertThat(response.getStatus()).isEqualTo("PENDING");
    assertThat(response.getTotalToPay()).isEqualTo(new BigDecimal("99.99"));
  });
```

## Key points

1. **Prefer `convertTo()` to `extractingPath()`**: type-safe and refactorable
2. **Use `satisfies()` for multiple assertions**: keeps tests readable
3. **Statically import `org.assertj.core.api.Assertions.assertThat`**
4. **Works with generics through `TypeReference`**: for `List<T>` responses
5. **Supports IDE refactoring**: when fields are renamed, the IDE updates tests
