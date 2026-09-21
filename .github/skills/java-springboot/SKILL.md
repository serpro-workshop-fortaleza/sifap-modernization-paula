---
name: "java-springboot"
description: "Best practices for Spring Boot applications: package-by-feature structure, constructor injection, DTOs and validation, service-layer transactions, Spring Data JPA, and configuration and secret handling. Use when creating or reviewing Spring Boot backend code to apply idiomatic structures and conventions. Complements the kit's Java 21 + Spring Boot 3.3 stack."
---
# Spring Boot best practices

Create and review idiomatic Spring Boot 3.3 slices for the SIFAP 2.0 backend (Java 21, PostgreSQL 16): package-by-feature structure, constructor injection, record DTOs, service-layer transactions, and Spring Data JPA. This skill is a quick best-practices checklist. The authoritative conventions, enforced by CI, are in the instruction files. Follow them where there is overlap:

- [`backend.instructions.md`](../../instructions/backend.instructions.md): controllers, DTOs, validation, and error handling.
- [`modular-monolith.instructions.md`](../../instructions/modular-monolith.instructions.md): module boundaries and Adabas FDT-to-JPA mapping.

## When to Invoke

- "Scaffold a new feature slice (controller, service, and repository) for this module."
- "Review this Spring Boot code's structure and conventions."
- "Configure this service's properties and secrets."
- "Turn this JPA entity into a proper DTO-based endpoint."

## Project setup and structure

- **Build tool:** use Maven (`pom.xml`) or Gradle (`build.gradle`) to manage dependencies.
- **Starters:** use Spring Boot starters, such as `spring-boot-starter-web` and `spring-boot-starter-data-jpa`, to simplify dependency management.
- **Package structure:** organize code by feature or domain, such as `com.example.app.order` and `com.example.app.user`, not by layer, such as `com.example.app.controller` and `com.example.app.service`.

## Dependency injection and components

- **Constructor injection:** always use constructor injection for required dependencies. This makes dependencies explicit and components easier to test.
- **Immutability:** declare dependency fields as `private final`.
- **Component stereotypes:** use `@Component`, `@Service`, `@Repository`, and `@Controller`/`@RestController` annotations appropriately to define beans.

## Configuration

- **Externalized configuration:** use `application.yml` (or `application.properties`) for configuration. YAML is often preferable for its readability and hierarchical structure.
- **Type-safe properties:** use `@ConfigurationProperties` to bind configuration to strongly typed Java objects.
- **Profiles:** use Spring profiles (`application-dev.yml`, `application-prod.yml`) to manage environment-specific settings.
- **Secret management:** never hardcode secrets. Use environment variables locally and Azure Key Vault through Managed Identity in Azure. Never use `application.yml`, `locals`, or source code. See [`security.instructions.md`](../../instructions/security.instructions.md).

## Web layer (controllers)

- **RESTful APIs:** use `/api/v1/{resource}` paths, correct verbs and status codes (`201`/`204`/`409`), and OpenAPI annotations on every endpoint.
- **Record DTOs:** expose Java 21 `record` DTOs at boundaries; never return JPA entities to the client.
- **Validation:** apply Bean Validation (`@Valid`, `@NotBlank`, `@Positive`, `@Size`) to the request record at the controller boundary.
- **Error handling:** centralize errors in a `@RestControllerAdvice` returning RFC 7807 `ProblemDetail`. See [`backend.instructions.md`](../../instructions/backend.instructions.md) for the full controller and error format.

## Service layer

- **Business logic:** encapsulate all business logic in `@Service` classes.
- **Statelessness:** services must not retain state.
- **Transaction management:** use `@Transactional` only in the service layer, never in controllers or repositories. For reads, use `@Transactional(readOnly = true)`.
- **No null returns:** represent absence with `Optional`; never return `null` from a public method.
- **Type unions:** use a `sealed interface` with records for discriminated domain states (Java 21).

## Data layer (repositories)

- **Spring Data JPA:** use Spring Data JPA repositories extending `JpaRepository` or `CrudRepository` for standard database operations.
- **Custom queries:** use `@Query` or the JPA Criteria API for complex queries.
- **Projections:** use DTO projections to fetch only the required data from the database.

## Logging

- **SLF4J:** use the SLF4J API for logging.
- **Logger declaration:** `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`
- **Parameterized logging:** use parameterized messages (`logger.info("Processing user {}...", userId);`) instead of string concatenation to improve performance.

## Testing

- **Unit tests:** test services and components with JUnit 5 + Mockito. See [`java-junit`](../java-junit/SKILL.md).
- **Slice and integration tests:** use `@WebMvcTest`, `@DataJpaTest`, and `@SpringBootTest` with Testcontainers and a real PostgreSQL 16 instance. See [`spring-boot-testing`](../spring-boot-testing/SKILL.md).

## Security

- **Spring Security:** use Spring Security for authentication and authorization (OAuth2/JWT).
- **Password encoding:** always hash passwords with a strong algorithm such as BCrypt.
- **Input handling:** use Spring Data JPA / JPQL (never string-concatenated SQL) and encode output to prevent XSS. See [`security.instructions.md`](../../instructions/security.instructions.md).

## Output Template

```java
// com.sifap.payment: one bounded context per package
@RestController
@RequestMapping("/api/v1/payments")
@RequiredArgsConstructor
class PaymentController {
    private final PaymentService service;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Register a payment")
    PaymentResponse create(@Valid @RequestBody CreatePaymentRequest request) {
        return service.create(request);
    }
}

public record CreatePaymentRequest(@NotBlank String reference, @NotNull @Positive BigDecimal amount) {}

@Service
@RequiredArgsConstructor
class PaymentService {
    private final PaymentRepository repository;

    @Transactional
    PaymentResponse create(CreatePaymentRequest request) {
        return PaymentResponse.from(repository.save(Payment.from(request)));
    }
}

interface PaymentRepository extends JpaRepository<Payment, UUID> {}
```

## Quality Gate

- [ ] Code is organized by feature or bounded context; no module imports another module's internals.
- [ ] Dependencies use constructor injection (`private final`); no field uses `@Autowired`.
- [ ] Endpoints use `/api/v1/{resource}`, correct status codes, OpenAPI annotations, and `record` DTOs.
- [ ] `@Transactional` appears only in services; no public method returns `null`.
- [ ] Errors go through a single `@RestControllerAdvice` as `ProblemDetail`; no secrets or sensitive data are logged.
- [ ] Unit tests (Mockito) and relevant slice tests pass. See `java-junit` and `spring-boot-testing`.
