# @WebMvcTest

Testing Spring MVC controllers with focused slice tests.

> [!IMPORTANT]
> The examples below use `MockMvcTester` and `@MockitoBean`, which belong to **Spring Boot 3.4+** and are **outside the kit's scope**. In the kit's Spring Boot 3.3, use classic `MockMvc` with `mockMvc.perform(...).andExpect(...)` and `@MockBean`. See [mockmvc-classic.md](mockmvc-classic.md).

## Basic structure

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @Autowired
  private MockMvcTester mvc;

  @MockitoBean
  private OrderService orderService;

  @MockitoBean
  private UserService userService;
}
```

## What is loaded

- The specified controllers
- Spring MVC infrastructure (HandlerMapping, HandlerAdapter)
- Jackson's ObjectMapper (for JSON)
- Exception handlers (@ControllerAdvice)
- Spring Security filters (if on the classpath)
- Validation (if on the classpath)

## Testing GET endpoints

```java
@Test
void shouldReturnOrder() {
  var order = new Order(1L, "PENDING", BigDecimal.valueOf(99.99));
  given(orderService.findById(1L)).willReturn(order);

  assertThat(mvc.get().uri("/orders/1"))
    .hasStatusOk()
    .hasContentType(MediaType.APPLICATION_JSON)
    .bodyJson()
    .extractingPath("$.status")
    .isEqualTo("PENDING");
}
```

## Testing POST with a request body

### Using text blocks (Java 21)

```java
@Test
void shouldCreateOrder() {
  given(orderService.create(any(OrderRequest.class))).willReturn(1L);

  var json = """
    {
      "product": "Product A",
      "quantity": 2
    }
    """;

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json))
    .hasStatus(HttpStatus.CREATED)
    .hasHeader("Location", "/orders/1");
}
```

### Using records

```java
record OrderRequest(String product, int quantity) {}

@Test
void shouldCreateOrderWithRecord() {
  var request = new OrderRequest("Product A", 2);
  given(orderService.create(any())).willReturn(1L);

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json.write(request).getJson()))
    .hasStatus(HttpStatus.CREATED);
}
```

## Testing validation errors

```java
@Test
void shouldRejectInvalidOrder() {
  var invalidJson = """
    {
      "product": "",
      "quantity": -1
    }
    """;

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(invalidJson))
    .hasStatus(HttpStatus.BAD_REQUEST)
    .bodyJson()
    .hasPath("$.errors");
}
```

## Testing query parameters

```java
@Test
void shouldFilterOrdersByStatus() {
  assertThat(mvc.get().uri("/orders?status=PENDING"))
    .hasStatusOk();

  verify(orderService).findByStatus(OrderStatus.PENDING);
}
```

## Testing path variables

```java
@Test
void shouldCancelOrder() {
  assertThat(mvc.put().uri("/orders/123/cancel"))
    .hasStatusOk();

  verify(orderService).cancel(123L);
}
```

## Testing with security

```java
@Test
@WithMockUser(roles = "ADMIN")
void adminShouldDeleteOrder() {
  assertThat(mvc.delete().uri("/orders/1"))
    .hasStatus(HttpStatus.NO_CONTENT);
}

@Test
void anonymousUserShouldBeForbidden() {
  assertThat(mvc.delete().uri("/orders/1"))
    .hasStatus(HttpStatus.UNAUTHORIZED);
}
```

## Multiple controllers

```java
@WebMvcTest({OrderController.class, ProductController.class})
class WebLayerTest {
  // Tests multiple controllers in one slice
}
```

## Excluding auto-configuration

```java
@WebMvcTest(OrderController.class)
@AutoConfigureMockMvc(addFilters = false) // Skips security filters
class OrderControllerWithoutSecurityTest {
  // Tests without security filters
}
```

## Key points

1. In Spring Boot 3.3, mock collaborators with `@MockBean` (`@MockitoBean` is the replacement in version 3.4+)
2. In Spring Boot 3.3, use classic `MockMvc` (`perform(...).andExpect(...)`); `MockMvcTester` requires 3.4+
3. Test HTTP semantics (status, headers, and content type)
4. Verify service method calls when side effects matter
5. Do not test business logic here; that belongs in unit tests
6. Leverage Java 21 text blocks for JSON payloads
