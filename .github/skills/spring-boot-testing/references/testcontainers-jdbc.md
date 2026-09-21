# Testcontainers JDBC

Testing JPA repositories with real databases using Testcontainers.

## Overview

Testcontainers provides real database instances in Docker containers for integration tests. It is more reliable than H2 for maintaining production parity.

## PostgreSQL setup

### Dependencies

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers-postgresql</artifactId>
  <scope>test</scope>
</dependency>
```

### Basic test

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryPostgresTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private OrderRepository orderRepository;

  @Autowired
  private TestEntityManager entityManager;
}
```

## MySQL setup

```xml
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers-mysql</artifactId>
  <scope>test</scope>
</dependency>
```

```java
@Container
@ServiceConnection
static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.4");
```

## Multiple databases

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class MultiDatabaseTest {

  @Container
  @ServiceConnection(name = "primary")
  static PostgreSQLContainer<?> primaryDb = new PostgreSQLContainer<>("postgres:16");

  @Container
  @ServiceConnection(name = "analytics")
  static PostgreSQLContainer<?> analyticsDb = new PostgreSQLContainer<>("postgres:16");
}
```

## Container reuse (speed optimization)

Add to `~/.testcontainers.properties`:

```properties
testcontainers.reuse.enable=true
```

Then enable reuse in the code:

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .withReuse(true);
```

## Database initialization

### With SQL scripts

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .withInitScript("schema.sql");
```

### With Flyway

```java
@SpringBootTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MigrationTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private Flyway flyway;

  @Test
  void shouldApplyMigrations() {
    flyway.migrate();
    // Test code
  }
}
```

## Advanced configuration

### Custom database or schema

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .withDatabaseName("testdb")
  .withUsername("testuser")
  .withPassword("testpass")
  .withInitScript("init-schema.sql");
```

### Wait strategies

```java
@Container
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .waitingFor(Wait.forLogMessage(".*database system is ready.*", 1));
```

## Test example

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

  @Test
  void shouldFindOrdersByStatus() {
    // Given
    entityManager.persist(new Order("PENDING"));
    entityManager.persist(new Order("COMPLETED"));
    entityManager.flush();

    // When
    List<Order> pending = orderRepository.findByStatus("PENDING");

    // Then
    assertThat(pending).hasSize(1);
    assertThat(pending.get(0).getStatus()).isEqualTo("PENDING");
  }

  @Test
  void shouldSupportPostgresSpecificFeatures() {
    // Can use Postgres-specific features, such as:
    // - JSONB columns
    // - array types
    // - full-text search
  }
}
```

## Alternative with @DynamicPropertySource

If not using @ServiceConnection:

```java
@SpringBootTest
@Testcontainers
class OrderServiceTest {

  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
  }
}
```

## Supported databases

| Database | Container class | Maven artifact |
| -------- | --------------- | -------------- |
| PostgreSQL | PostgreSQLContainer | testcontainers-postgresql |
| MySQL | MySQLContainer | testcontainers-mysql |
| MariaDB | MariaDBContainer | testcontainers-mariadb |
| SQL Server | MSSQLServerContainer | testcontainers-mssqlserver |
| Oracle | OracleContainer | testcontainers-oracle-free |
| MongoDB | MongoDBContainer | testcontainers-mongodb |

## Best practices

1. Use @ServiceConnection when possible (Spring Boot 3.1+)
2. Enable container reuse to speed up local builds
3. Use specific versions (postgres:16), not the latest version
4. Keep container configuration in a static field
5. Use @DataJpaTest with AutoConfigureTestDatabase.Replace.NONE
