# RestTestClient

Modern REST client testing with Spring Boot 4+ (replaces TestRestTemplate).

## Overview

RestTestClient is the modern alternative to TestRestTemplate in Spring Boot 4.0+. It provides a fluent, reactive API for testing REST endpoints.

## Setup

### Dependency (Spring Boot 4+)

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-restclient-test</artifactId>
  <scope>test</scope>
</dependency>
```

### Basic setup

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class OrderIntegrationTest {

  @Autowired
  private RestTestClient restClient;
}
```

## HTTP methods

### GET request

```java
@Test
void shouldGetOrder() {
  restClient
    .get()
    .uri("/orders/1")
    .exchange()
    .expectStatus()
    .isOk()
    .expectBody(Order.class)
    .value(order -> {
      assertThat(order.getId()).isEqualTo(1L);
      assertThat(order.getStatus()).isEqualTo("PENDING");
    });
}
```

### POST request

```java
@Test
void shouldCreateOrder() {
  OrderRequest request = new OrderRequest("Laptop", 2);

  restClient
    .post()
    .uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .body(request)
    .exchange()
    .expectStatus()
    .isCreated()
    .expectHeader()
    .location("/orders/1")
    .expectBody(Long.class)
    .isEqualTo(1L);
}
```

### PUT request

```java
@Test
void shouldUpdateOrder() {
  restClient
    .put()
    .uri("/orders/1")
    .body(new OrderUpdate("COMPLETED"))
    .exchange()
    .expectStatus()
    .isOk();
}
```

### DELETE request

```java
@Test
void shouldDeleteOrder() {
  restClient
    .delete()
    .uri("/orders/1")
    .exchange()
    .expectStatus()
    .isNoContent();
}
```

## Response assertions

### Status codes

```java
restClient
  .get()
  .uri("/orders/1")
  .exchange()
  .expectStatus()
  .isOk()           // 200
  .isCreated()      // 201
  .isNoContent()    // 204
  .isBadRequest()   // 400
  .isNotFound()     // 404
  .is5xxServerError() // 5xx
  .isEqualTo(200);  // Specific code
```

### Response headers

```java
restClient
  .post()
  .uri("/orders")
  .exchange()
  .expectHeader()
  .location("/orders/1")
  .contentType(MediaType.APPLICATION_JSON)
  .exists("X-Request-Id")
  .valueEquals("X-Api-Version", "v1");
```

### Body assertions

```java
restClient
  .get()
  .uri("/orders/1")
  .exchange()
  .expectBody(Order.class)
  .value(order -> assertThat(order.getId()).isEqualTo(1L))
  .returnResult();
```

### JSON Path

```java
restClient
  .get()
  .uri("/orders")
  .exchange()
  .expectBody()
  .jsonPath("$.content[0].id").isEqualTo(1)
  .jsonPath("$.content[0].status").isEqualTo("PENDING")
  .jsonPath("$.totalElements").isNumber();
```

## Request configuration

### Request headers

```java
restClient
  .get()
  .uri("/orders/1")
  .header("Authorization", "Bearer token")
  .header("X-Api-Key", "secret")
  .exchange();
```

### Query parameters

```java
restClient
  .get()
  .uri(uriBuilder -> uriBuilder
    .path("/orders")
    .queryParam("status", "PENDING")
    .queryParam("page", 0)
    .queryParam("size", 10)
    .build())
  .exchange();
```

### Path variables

```java
restClient
  .get()
  .uri("/orders/{id}", 1L)
  .exchange();
```

## With MockMvc

RestTestClient also works with MockMvc (without starting the server):

```java
@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureRestTestClient
class OrderMockMvcTest {

  @Autowired
  private RestTestClient restClient;

  @Test
  void shouldWorkWithMockMvc() {
    // Uses MockMvc internally, without starting the server
    restClient
      .get()
      .uri("/orders/1")
      .exchange()
      .expectStatus()
      .isOk();
  }
}
```

## Comparison: RestTestClient versus TestRestTemplate

| Feature | RestTestClient | TestRestTemplate |
| ------- | -------------- | ---------------- |
| Style | Fluent/reactive | Imperative |
| Spring Boot | 4.0+ | All versions (deprecated in 4) |
| Assertions | Built-in | Manual |
| MockMvc support | Yes | No |
| Asynchronous | Native | Requires additional handling |

## Migrating from TestRestTemplate

### Before (deprecated)

```java
@Autowired
private TestRestTemplate restTemplate;

@Test
void shouldGetOrder() {
  ResponseEntity<Order> response = restTemplate
    .getForEntity("/orders/1", Order.class);

  assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
  assertThat(response.getBody().getId()).isEqualTo(1L);
}
```

### After (RestTestClient)

```java
@Autowired
private RestTestClient restClient;

@Test
void shouldGetOrder() {
  restClient
    .get()
    .uri("/orders/1")
    .exchange()
    .expectStatus()
    .isOk()
    .expectBody(Order.class)
    .value(order -> assertThat(order.getId()).isEqualTo(1L));
}
```

## Best practices

1. Use with @SpringBootTest(WebEnvironment.RANDOM_PORT) for real HTTP
2. Use with @AutoConfigureMockMvc for faster serverless tests
3. Leverage fluent assertions to improve readability
4. Test success and error scenarios
5. Verify security and API versioning headers
