# Migration to Spring Boot 4.0

Key testing changes when migrating from Spring Boot 3.x to 4.0.

## Dependency changes

### Modular test starters

Spring Boot 4.0 introduces modular test starters:

**Before (3.x):**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
```

**After (4.0), WebMvc tests:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-webmvc-test</artifactId>
  <scope>test</scope>
</dependency>
```

**After (4.0), REST client tests:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-restclient-test</artifactId>
  <scope>test</scope>
</dependency>
```

## Annotation migration

### @MockBean → @MockitoBean

**Deprecated (3.x):**

```java
@MockBean
private OrderService orderService;
```

**New (4.0):**

```java
@MockitoBean
private OrderService orderService;
```

### @SpyBean → @MockitoSpyBean

**Deprecated (3.x):**

```java
@SpyBean
private PaymentGatewayClient paymentClient;
```

**New (4.0):**

```java
@MockitoSpyBean
private PaymentGatewayClient paymentClient;
```

## New testing features

### RestTestClient

Replaces TestRestTemplate (deprecated):

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class OrderIntegrationTest {

  @Autowired
  private RestTestClient restClient;

  @Test
  void shouldCreateOrder() {
    restClient
      .post()
      .uri("/orders")
      .body(new OrderRequest("Product", 2))
      .exchange()
      .expectStatus()
      .isCreated()
      .expectHeader()
      .location("/orders/1");
  }
}
```

## JUnit 6 compatibility

Spring Boot 4.0 uses JUnit 6 by default:

- JUnit 4 is deprecated (use JUnit Vintage temporarily)
- All JUnit 5 features continue to work
- Remove JUnit 4 dependencies for a clean migration

## Testcontainers 2.0

Module names have changed:

**Before (1.x):**

```xml
<artifactId>postgresql</artifactId>
```

**After (2.0):**

```xml
<artifactId>testcontainers-postgresql</artifactId>
```

## Mocking non-singleton beans

Spring Framework 7 supports mocking prototype-scoped beans:

```java
@Component
@Scope("prototype")
public class OrderProcessor { }

@SpringBootTest
class OrderServiceTest {
  @MockitoBean
  private OrderProcessor orderProcessor; // Now works!
}
```

## SpringExtension context changes

The extension context is now scoped to the test method by default.

If tests fail with @Nested classes:

```java
@SpringExtensionConfig(useTestClassScopedExtensionContext = true)
@SpringBootTest
class OrderTest {
  // Uses the old behavior
}
```

## Migration checklist

- [ ] Replace @MockBean with @MockitoBean
- [ ] Replace @SpyBean with @MockitoSpyBean
- [ ] Update Testcontainers dependency names for 2.0
- [ ] Add modular test starters as needed
- [ ] Migrate TestRestTemplate to RestTestClient
- [ ] Remove JUnit 4 dependencies
- [ ] Update custom TestExecutionListener implementations
- [ ] Test @Nested class behavior

## Backward compatibility

Use "classic" starters for a gradual migration:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test-classic</artifactId>
  <scope>test</scope>
</dependency>
```

This preserves the old behavior during incremental migration.
