# Classic MockMvc

Classic `MockMvc` API for Spring MVC controller tests, the approach used by the kit on **Spring Boot 3.3**.

## When to use this reference

- The project uses Spring Boot 3.3 (the kit's stack) or a version before 3.4, where `MockMvcTester` is unavailable
- Existing tests use `mvc.perform(...)`, and you are maintaining or extending them
- You need to migrate classic MockMvc tests to `MockMvcTester` (see the migration section)
- The user explicitly asks about `ResultActions`, `andExpect()`, or Hamcrest-style web assertions

`MockMvcTester` (AssertJ style) requires **Spring Boot 3.4+** and is outside the kit's scope. Consult [mockmvc-tester.md](mockmvc-tester.md) only if the project is upgraded beyond 3.3.

## Setup

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @Autowired
  private MockMvc mvc;

  @MockBean
  private OrderService orderService;
}
```

## Basic GET request

```java
@Test
void shouldReturnOrder() throws Exception {
  given(orderService.findById(1L)).willReturn(new Order(1L, "PENDING", 99.99));

  mvc.perform(get("/orders/1"))
    .andExpect(status().isOk())
    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
    .andExpect(jsonPath("$.id").value(1))
    .andExpect(jsonPath("$.status").value("PENDING"))
    .andExpect(jsonPath("$.totalToPay").value(99.99));
}
```

## POST with a request body

```java
@Test
void shouldCreateOrder() throws Exception {
  given(orderService.create(any(OrderRequest.class))).willReturn(1L);

  mvc.perform(post("/orders")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"product\": \"Laptop\", \"quantity\": 2}"))
    .andExpect(status().isCreated())
    .andExpect(header().string("Location", "/orders/1"));
}
```

## PUT request

```java
@Test
void shouldUpdateOrder() throws Exception {
  mvc.perform(put("/orders/1")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"status\": \"COMPLETED\"}"))
    .andExpect(status().isOk());
}
```

## DELETE request

```java
@Test
void shouldDeleteOrder() throws Exception {
  mvc.perform(delete("/orders/1"))
    .andExpect(status().isNoContent());
}
```

## Status matchers

```java
.andExpect(status().isOk())           // 200
.andExpect(status().isCreated())      // 201
.andExpect(status().isNoContent())    // 204
.andExpect(status().isBadRequest())   // 400
.andExpect(status().isUnauthorized()) // 401
.andExpect(status().isForbidden())    // 403
.andExpect(status().isNotFound())     // 404
.andExpect(status().is(422))          // arbitrary code
```

## JSON Path assertions

```java
// Exact value
.andExpect(jsonPath("$.status").value("PENDING"))

// Existence
.andExpect(jsonPath("$.id").exists())
.andExpect(jsonPath("$.deletedAt").doesNotExist())

// Array size
.andExpect(jsonPath("$.items").isArray())
.andExpect(jsonPath("$.items", hasSize(3)))

// Nested field
.andExpect(jsonPath("$.customer.name").value("John Doe"))
.andExpect(jsonPath("$.customer.address.city").value("Berlin"))

// With Hamcrest matchers
.andExpect(jsonPath("$.total", greaterThan(0.0)))
.andExpect(jsonPath("$.description", containsString("order")))
```

## Content assertions

```java
.andExpect(content().contentType(MediaType.APPLICATION_JSON))
.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
.andExpect(content().string(containsString("PENDING")))
.andExpect(content().json("{\"status\":\"PENDING\"}"))
```

## Header assertions

```java
.andExpect(header().string("Location", "/orders/1"))
.andExpect(header().string("Content-Type", containsString("application/json")))
.andExpect(header().exists("X-Request-Id"))
.andExpect(header().doesNotExist("X-Deprecated"))
```

## Request parameters and headers

```java
// Query parameters
mvc.perform(get("/orders").param("status", "PENDING").param("page", "0"))
  .andExpect(status().isOk());

// Path variables
mvc.perform(get("/orders/{id}", 1L))
  .andExpect(status().isOk());

// Request headers
mvc.perform(get("/orders/1").header("X-Api-Key", "secret"))
  .andExpect(status().isOk());
```

## Capturing the response

```java
@Test
void shouldReturnCreatedId() throws Exception {
  given(orderService.create(any())).willReturn(42L);

  MvcResult result = mvc.perform(post("/orders")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"product\": \"Laptop\", \"quantity\": 1}"))
    .andExpect(status().isCreated())
    .andReturn();

  String location = result.getResponse().getHeader("Location");
  assertThat(location).isEqualTo("/orders/42");
}
```

## Chaining with andDo

```java
mvc.perform(get("/orders/1"))
  .andDo(print())              // prints request/response to the console (debugging)
  .andExpect(status().isOk());
```

## Static imports

```java
import org.springframework.boot.test.mock.mockito.MockBean;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.*;
import static org.hamcrest.Matchers.*;
```

## Migrating to MockMvcTester

| Classic MockMvc | MockMvcTester (recommended) |
| --- | --- |
| `@Autowired MockMvc mvc` | `@Autowired MockMvcTester mvc` |
| `mvc.perform(get("/orders/1"))` | `mvc.get().uri("/orders/1")` |
| `.andExpect(status().isOk())` | `.hasStatusOk()` |
| `.andExpect(jsonPath("$.status").value("X"))` | `.bodyJson().convertTo(T.class)` + AssertJ |
| `throws Exception` on every method | No checked exception |
| Hamcrest matchers | Fluent AssertJ assertions |

See [mockmvc-tester.md](mockmvc-tester.md) for the complete modern API.

## Key points

1. **Every test method must declare `throws Exception`**: `perform()` throws checked exceptions
2. **Use `andDo(print())` while debugging**: remove it before committing the change
3. **Prefer `jsonPath()` to `content().string()`**: more precise field-level assertions
4. **Static imports are required**: the IDE can add them automatically
5. **Migrate to MockMvcTester** when upgrading to Spring Boot 3.4+ for improved readability
