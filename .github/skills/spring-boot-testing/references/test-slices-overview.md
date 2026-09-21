# Test slices overview

Quick reference for selecting the appropriate Spring Boot test slice.

## Decision matrix

| Annotation | When to use | Loads | Speed |
| ---------- | -------- | ----- | ----- |
| **None** (plain JUnit) | Pure business logic | Nothing | Fastest |
| `@WebMvcTest` | Controller + HTTP layer | Controllers, MVC, Jackson | Fast |
| `@DataJpaTest` | Repository queries | Repositories, JPA, DataSource | Fast |
| `@RestClientTest` | REST client code | RestTemplate/RestClient, Jackson | Fast |
| `@JsonTest` | JSON serialization | ObjectMapper only | Fastest slice |
| `@WebFluxTest` | Reactive controllers | Controllers, WebFlux | Fast |
| `@DataJdbcTest` | JDBC repositories | Repositories, JDBC | Fast |
| `@DataMongoTest` | MongoDB repositories | Repositories, MongoDB | Fast |
| `@DataRedisTest` | Redis repositories | Repositories, Redis | Fast |
| `@SpringBootTest` | Full integration | Entire application | Slow |

## Selection guide

### No annotation (plain unit test)

```java
class PriceCalculatorTest {
  private PriceCalculator calculator = new PriceCalculator();

  @Test
  void shouldApplyDiscount() {
    var result = calculator.applyDiscount(100, 0.1);
    assertThat(result).isEqualTo(new BigDecimal("90.00"));
  }
}
```

**When**: pure business logic, with no dependencies or simple dependencies that can be mocked through constructor injection.

### Use @WebMvcTest

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
  @Autowired private MockMvcTester mvc;
  @MockitoBean private OrderService orderService;
}
```

**When**: testing request mapping, validation, JSON mapping, security, and filters.

**What you get**: MockMvc, ObjectMapper, Spring Security (if present), and exception handlers.

### Use @DataJpaTest

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {
  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
}
```

**When**: testing custom JPA queries, entity mappings, transactional behavior, and cascading operations.

**What you get**: repository beans, EntityManager, TestEntityManager, and transaction support.

### Use @RestClientTest

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {
  @Autowired private WeatherService weatherService;
  @Autowired private MockRestServiceServer server;
}
```

**When**: testing REST clients that call external APIs.

**What you get**: MockRestServiceServer to configure HTTP responses.

### Use @JsonTest

```java
@JsonTest
class OrderJsonTest {
  @Autowired private JacksonTester<Order> json;
}
```

**When**: testing custom serializers and deserializers and complex JSON mapping.

### Use @SpringBootTest

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class OrderIntegrationTest {
  @Autowired private RestTestClient restClient;
}
```

**When**: testing the complete request flow, security filters, and database interactions together.

**What you get**: full application context, optional embedded server, and real beans.

## Common mistakes

1. **Using @SpringBootTest for everything**: makes the suite unnecessarily slow
2. **Using @WebMvcTest without mocking services**: causes context loading failures
3. **Using @DataJpaTest with @MockBean**: defeats the purpose, since real repositories are needed
4. **Using multiple slices in one test**: each slice should be in a separate test class

## Java 21 features in tests

### Records for test data

```java
record OrderRequest(String product, int quantity) {}
record OrderResponse(Long id, String status, BigDecimal total) {}
```

### Pattern matching in tests

```java
@Test
void shouldHandleDifferentOrderTypes() {
  var order = orderService.create(new OrderRequest("Product", 2));

  switch (order) {
    case PhysicalOrder po -> assertThat(po.getShippingAddress()).isNotNull();
    case DigitalOrder do_ -> assertThat(do_.getDownloadLink()).isNotNull();
    default -> throw new IllegalStateException("Unknown order type");
  }
}
```

### Text blocks for JSON

```java
@Test
void shouldParseComplexJson() {
  var json = """
    {
      "id": 1,
      "status": "PENDING",
      "items": [
        {"product": "Laptop", "price": 999.99},
        {"product": "Mouse", "price": 29.99}
      ]
    }
    """;

  assertThat(mvc.post().uri("/orders")
    .contentType(APPLICATION_JSON)
    .content(json))
    .hasStatus(CREATED);
}
```

### Sequenced collections

```java
@Test
void shouldReturnOrdersInSequence() {
  var orders = orderRepository.findAll();

  assertThat(orders.getFirst().getStatus()).isEqualTo("NEW");
  assertThat(orders.getLast().getStatus()).isEqualTo("COMPLETED");
  assertThat(orders.reversed().getFirst().getStatus()).isEqualTo("COMPLETED");
}
```

## Dependencies by slice

```xml
<!-- WebMvcTest -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-webmvc-test</artifactId>
  <scope>test</scope>
</dependency>

<!-- DataJpaTest -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<!-- RestClientTest -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-restclient-test</artifactId>
  <scope>test</scope>
</dependency>

<!-- Testcontainers -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
```
