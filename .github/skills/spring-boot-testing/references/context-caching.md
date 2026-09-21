# Context caching

Optimize Spring Boot test suite performance with context caching.

## How context caching works

Spring's TestContext Framework caches application contexts based on the configuration "key". Tests with identical configurations reuse the same context.

### What affects the cache key

- @ContextConfiguration
- @TestPropertySource
- @ActiveProfiles
- @WebAppConfiguration
- @MockitoBean definitions
- @TestConfiguration imports

## Cache key examples

### Same key (context reused)

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest1 {
  @MockitoBean private OrderService orderService;
}

@WebMvcTest(OrderController.class)
class OrderControllerTest2 {
  @MockitoBean private OrderService orderService;
}
// The same context is reused
```

### Different key (new context)

```java
@WebMvcTest(OrderController.class)
@ActiveProfiles("test")
class OrderControllerTest1 { }

@WebMvcTest(OrderController.class)
@ActiveProfiles("integration")
class OrderControllerTest2 { }
// Different contexts are loaded
```

## Viewing cache statistics

### Spring Boot Actuator

```yaml
management:
  endpoints:
    web:
      exposure:
        include: metrics
```

Access: `GET /actuator/metrics/spring.test.context.cache`

### Debug logging

```properties
logging.level.org.springframework.test.context.cache=DEBUG
```

## Optimizing the cache hit rate

### Group tests by configuration

```text
 tests/
  unit/           # No context
   web/            # @WebMvcTest
   repository/     # @DataJpaTest
   integration/    # @SpringBootTest
```

### Minimize @TestPropertySource variations

**Bad (multiple contexts):**

```java
@TestPropertySource(properties = "app.feature-x=true")
class FeatureXTest { }

@TestPropertySource(properties = "app.feature-y=true")
class FeatureYTest { }
```

**Better (grouped):**

```java
@TestPropertySource(properties = {"app.feature-x=true", "app.feature-y=true"})
class FeaturesTest { }
```

### Use @DirtiesContext sparingly

Only when the context state actually changes:

```java
@Test
@DirtiesContext // Forces a context rebuild after the test
void testThatModifiesBeanDefinitions() { }
```

## Best practices

1. **Group by configuration**: keep tests with the same configuration together
2. **Limit property variations**: prefer profiles to individual properties
3. **Avoid @DirtiesContext**: prefer cleaning up test data
4. **Use narrow slices**: @WebMvcTest instead of @SpringBootTest
5. **Monitor cache hits**: enable debug logging occasionally
