# @DataJpaTest

Testing JPA repositories with an isolated data-layer slice.

## Basic structure

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private OrderRepository orderRepository;

  @Autowired
  private TestEntityManager entityManager;
}
```

## What is loaded

- Repository beans
- EntityManager / TestEntityManager
- DataSource
- Transaction manager
- No web layer, services, or controllers

## Testing custom queries

```java
@Test
void shouldFindOrdersByStatus() {
  // Given: using var for cleaner code
  var pending = new Order("PENDING");
  var completed = new Order("COMPLETED");
  entityManager.persist(pending);
  entityManager.persist(completed);
  entityManager.flush();

  // When
  var pendingOrders = orderRepository.findByStatus("PENDING");

  // Then: using sequenced collection methods
  assertThat(pendingOrders).hasSize(1);
  assertThat(pendingOrders.getFirst().getStatus()).isEqualTo("PENDING");
}
```

## Testing native queries

```java
@Test
void shouldExecuteNativeQuery() {
  entityManager.persist(new Order("PENDING", BigDecimal.valueOf(100)));
  entityManager.persist(new Order("PENDING", BigDecimal.valueOf(200)));
  entityManager.flush();

  var total = orderRepository.calculatePendingTotal();

  assertThat(total).isEqualTo(new BigDecimal("300.00"));
}
```

## Testing pagination

```java
@Test
void shouldReturnPagedResults() {
  // Inserts 20 orders using IntStream
  IntStream.range(0, 20).forEach(i -> {
    entityManager.persist(new Order("PENDING"));
  });
  entityManager.flush();

  var page = orderRepository.findByStatus("PENDING", PageRequest.of(0, 10));

  assertThat(page.getContent()).hasSize(10);
  assertThat(page.getTotalElements()).isEqualTo(20);
  assertThat(page.getContent().getFirst().getStatus()).isEqualTo("PENDING");
}
```

## Testing lazy loading

```java
@Test
void shouldLazyLoadOrderItems() {
  var order = new Order("PENDING");
  order.addItem(new OrderItem("Product", 2));
  entityManager.persist(order);
  entityManager.flush();
  entityManager.clear(); // Detaches from the persistence context

  var found = orderRepository.findById(order.getId());

  assertThat(found).isPresent();
  // This will trigger lazy loading
  assertThat(found.get().getItems()).hasSize(1);
  assertThat(found.get().getItems().getFirst().getProduct()).isEqualTo("Product");
}
```

## Testing cascading operations

```java
@Test
void shouldCascadeDelete() {
  var order = new Order("PENDING");
  order.addItem(new OrderItem("Product", 2));
  entityManager.persist(order);
  entityManager.flush();

  orderRepository.delete(order);
  entityManager.flush();

  assertThat(entityManager.find(OrderItem.class, order.getItems().getFirst().getId()))
    .isNull();
}
```

## Testing @Query methods

```java
@Query("SELECT o FROM Order o WHERE o.createdAt > :date AND o.status = :status")
List<Order> findRecentByStatus(@Param("date") LocalDateTime date,
                               @Param("status") String status);

@Test
void shouldFindRecentOrders() {
  var old = new Order("PENDING");
  old.setCreatedAt(LocalDateTime.now().minusDays(10));
  var recent = new Order("PENDING");
  recent.setCreatedAt(LocalDateTime.now().minusHours(1));

  entityManager.persist(old);
  entityManager.persist(recent);
  entityManager.flush();

  var recentOrders = orderRepository.findRecentByStatus(
    LocalDateTime.now().minusDays(1), "PENDING");

  assertThat(recentOrders).hasSize(1);
  assertThat(recentOrders.getFirst().getId()).isEqualTo(recent.getId());
}
```

## Using H2 versus a real database

### H2 (default, not recommended for production parity)

```java
@DataJpaTest // Uses embedded H2 by default
class OrderRepositoryH2Test {
  // Fast, but may not catch database-specific issues
}
```

### Testcontainers (recommended)

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryPostgresTest {
  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
}
```

## Transaction behavior

Tests are @Transactional by default and roll back after each test.

```java
@Test
@Rollback(false) // Does not roll back (rarely needed)
void shouldPersistData() {
  orderRepository.save(new Order("PENDING"));
  // Data will remain in the database after the test
}
```

## Key points

1. Use TestEntityManager to prepare data
2. Always call flush() after persist() to trigger SQL
3. Call clear() on the entity manager to test lazy loading
4. Use a real database (Testcontainers) for accurate results
5. Test success and failure cases
6. Leverage Java 21's var keyword for cleaner declarations
7. Use sequenced collection methods (getFirst(), getLast(), reversed())
