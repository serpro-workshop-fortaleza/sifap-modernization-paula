---
description: "Use when designing or reviewing Modular Monolith architecture, package-by-feature boundaries, JPA mapping, and Strangler Fig migration."
applyTo: "backend/src/main/java/**,backend/pom.xml,backend/build.gradle*"
---

# Modular Monolith architecture guide

This file activates when you work on Java source code or backend build configurations. It teaches the target architecture: a **Modular Monolith**, not microservices, with package-by-feature boundaries, bounded contexts, Adabas FDT-to-JPA mapping, Spring Boot 3.3 architectural conventions, and the Strangler Fig migration approach. It does **not** define controller, DTO, validation, or error response details, which belong to [`backend.instructions.md`](backend.instructions.md); security belongs to [`security.instructions.md`](security.instructions.md); schema migrations belong to [`database.instructions.md`](database.instructions.md); and legacy code reading belongs to [`natural-adabas.instructions.md`](natural-adabas.instructions.md).

## Core principle: one deployable, multiple modules

The target system is a single Spring Boot application with clear internal module boundaries. Each bounded context is a Maven module (or top-level package) owning its domain, repository, and service layers.

Why use a Modular Monolith instead of microservices:

- **Immersion constraint**: 8 hours is not enough to manage distributed systems, service discovery, and inter-service communication.
- **Complexity budget**: a monolith with strong module boundaries provides 80% of microservice benefits (team autonomy and clear ownership) at 20% of the operational cost.
- **Migration path**: a well-structured Modular Monolith can be decomposed into microservices later if needed. The reverse path is much harder.

## Package-by-feature structure

Organize code by business capability, not technical layer:

```text
src/main/java/com/example/app/
├── <feature>/                  # Team-defined bounded context
│   ├── <Feature>Controller.java
│   ├── <Feature>Service.java
│   ├── <Feature>Repository.java
│   ├── <Feature>.java
│   └── <Feature>Dto.java
├── shared/                     # Shared kernel
│   ├── audit/                  # Cross-cutting: audit trail
│   └── exception/              # Cross-cutting: error handling
└── Application.java            # Spring Boot entry point
```

Rules:

- A module MUST **NEVER** directly import another module's internal classes. Use interfaces or events.
- The `shared/` package contains only cross-cutting concerns (auditing, exceptions, and base entities).
- Each module has its own `*Repository`, `*Service`, and `*Controller`.

## Bounded context boundaries

When deciding where to draw module boundaries, ask:

1. **Who owns this data?** If two features share the same table, they may belong to the same context.
2. **What changes together?** Features changed in the same sprint belong together.
3. **What can fail independently?** If Feature A's failure MUST NOT break Feature B, they belong to separate contexts.

A common pattern in Natural/Adabas legacy modernization is for each Adabas file (FNR) to map to a bounded context, although some files contain shared reference data belonging to a shared kernel.

## JPA mapping from Adabas FDT

### Simple fields

| Adabas format | Java type | JPA annotation |
|---|---|---|
| `A` (alphanumeric) | `String` | `@Column(length = N)` |
| `N` (numeric, no decimal) | `Long` or `Integer` | `@Column` |
| `N` (numeric, with decimal) | `BigDecimal` | `@Column(precision = P, scale = S)` |
| `P` (packed decimal) | `BigDecimal` | `@Column(precision = P, scale = S)` |
| `D` (date) | `LocalDate` | `@Column` |
| `T` (time/datetime) | `LocalDateTime` | `@Column` |
| `B` (binary) | `byte[]` | `@Column` / `@Lob` |

### MU fields (multiple values) → JSONB

```java
@Column(columnDefinition = "jsonb")
@JdbcTypeCode(SqlTypes.JSON)
private List<String> alternateNames;  // Was an MU field in Adabas
```

Or use `@ElementCollection` when querying is needed:

```java
@ElementCollection
@CollectionTable(name = "person_alternate_names")
private List<String> alternateNames;
```

### PE (periodic groups) → @OneToMany

```java
@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
@JoinColumn(name = "person_id")
private List<AddressHistory> addressHistory;  // Was a PE group
```

In this case, `AddressHistory` is an `@Entity` with its own table.

## Spring Boot 3.3 conventions

- **Constructor injection**: no field `@Autowired`. Use `@RequiredArgsConstructor` (Lombok) or explicit constructors.
- **Records for DTOs**: `public record ResourceDto(Long id, String label) {}`
- **Controller-layer validation**: `@Valid @RequestBody ResourceDto dto` with Bean Validation annotations on the DTO.
- **@Transactional only in the service layer**: NEVER on repositories, NEVER on controllers.
- **Optional for nullable returns**: `Optional<Resource> findById(Long id)`; NEVER return `null` from public methods.
- **Sealed interfaces for type unions**: `sealed interface ResourceState permits StateA, StateB {}`

## Error handling pattern

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ProblemDetail> handleNotFound(EntityNotFoundException ex) {
        ProblemDetail detail = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(detail);
    }
}
```

Use `ProblemDetail` (RFC 7807) in all error responses.

## Strangler Fig pattern

When the modern system needs to coexist with the legacy system:

1. **Facade**: all requests pass through a routing layer
2. **New path**: new or migrated features are handled by Spring Boot modules
3. **Legacy path**: unmigrated features are forwarded to the legacy system
4. **Gradual migration**: as each feature migrates, its route shifts from legacy to modern

This pattern applies even within the immersion scope: teams may not migrate everything, and that is acceptable. The architecture MUST properly support partial migration.

## Conventions

| Rule | Rationale |
|---|---|
| One Spring Boot deployable with multiple internal modules | Preserves immersion delivery speed and keeps boundaries explicit |
| Packages by business capability | Modules map to bounded contexts, not technical layers |
| Private internals; cross-module access through interfaces or events | Prevents hidden coupling between contexts |
| Adabas FDT types deliberately mapped to Java/JPA | Avoids silent truncation, precision loss, and incorrect relationships |
| `@Transactional` only in services and constructor injection | Keeps persistence boundaries and dependencies explicit |
| `ProblemDetail` for errors | Gives all modules a machine-readable error format |

## Do / Don't

| Do | Don't |
|---|---|
| Keep one Spring Boot application with clear internal modules | Create separate Spring Boot applications or microservices for each context |
| Put business logic in Java services | Move logic into stored procedures or PostgreSQL functions |
| Use JPA/JPQL or Spring Data derived queries | Concatenate strings to create SQL |
| Use constructor injection | Use field injection with `@Autowired` |
| Return `Optional` when the result may be absent | Return `null` from public methods |
| Support partial migration with a Strangler Fig facade | Assume the entire legacy system will be migrated at once |

## PR Checklist

- [ ] New code lives in one Spring Boot deployable and is organized by business capability
- [ ] No module directly imports another's internal classes; interfaces or events define the boundary
- [ ] Repositories, services, controllers, entities, and DTOs live in the owning module or shared kernel
- [ ] Adabas FDT fields are mapped to Java/JPA types preserving precision and MU, PE, and descriptor semantics
- [ ] `@Transactional` appears only in services, dependencies use constructor injection, and public methods do not return `null`
- [ ] The design can coexist with unmigrated legacy paths through Strangler Fig routing
