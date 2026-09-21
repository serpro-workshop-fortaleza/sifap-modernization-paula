---
description: "Use when implementing backend APIs, services, controllers, request validation, error handling, and business service boundaries."
applyTo: "backend/src/main/java/**,backend/src/test/java/**"
---

# Backend conventions - Controllers, services, and validation

This file activates when you edit Java source code or tests in `backend/`. It teaches how to structure controllers, DTOs, the service layer, request validation, and error responses in a Java 21 + Spring Boot 3.3 application. It does **not** decide module boundaries or JPA/FDT mapping, which belong to [`modular-monolith.instructions.md`](modular-monolith.instructions.md), and does not cover authentication, which belongs to [`security.instructions.md`](security.instructions.md).

> [!NOTE]
> `backend/` does not exist yet. The team creates it from scratch in Stage 3. Treat the rules below as conventions the code must follow from the moment it is written.

## Layers and boundaries

Requests flow in one direction: `Controller → Service → Repository`. Keep controllers thin (HTTP mapping only) and put all business rules in the service.

- `@Transactional` belongs **only** in the service layer, never in a controller or repository; reads use `@Transactional(readOnly = true)`.
- Public methods never return `null`; represent absence with `Optional`.
- Keep controllers and services package-private within their modules so no other module imports internals.

## Controllers and REST endpoints

Paths follow `/api/v1/{resource}` (plural and kebab-case for multiword resources). Every endpoint has OpenAPI annotations and returns the correct status: `201` on creation, `204` on deletion, `409` on conflict, and `PATCH` for partial updates.

```java
@RestController
@RequestMapping("/api/v1/resources")
@RequiredArgsConstructor
class ResourceController {

    private final ResourceService resourceService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED) // 201 on creation
    @Operation(summary = "Register a resource")
    @ApiResponse(responseCode = "201", description = "Created")
    @ApiResponse(responseCode = "409", description = "Duplicate resource")
    ResourceResponse create(@Valid @RequestBody CreateResourceRequest request) {
        return resourceService.create(request);
    }
}
```

## DTOs and validation

Expose Java 21 `record` DTOs, never JPA entities. Validate at the controller boundary with Bean Validation on the request record.

```java
public record CreateResourceRequest(
    @NotBlank @Size(max = 120) String label,
    @NotNull @Positive BigDecimal amount) {}
```

## Service layer

The service coordinates the transaction, enforces invariants, and transforms persistence results into DTOs.

```java
@Service
@RequiredArgsConstructor
class ResourceService {

    private final ResourceRepository resourceRepository;

    @Transactional(readOnly = true)
    ResourceResponse getById(UUID id) {
        return resourceRepository.findById(id)
            .map(ResourceResponse::from)
            .orElseThrow(() -> new ResourceNotFoundException(id));
    }

    @Transactional
    ResourceResponse create(CreateResourceRequest request) {
        resourceRepository.findByLabel(request.label()).ifPresent(existing -> {
            throw new ResourceConflictException(request.label());
        });
        return ResourceResponse.from(resourceRepository.save(Resource.from(request)));
    }
}
```

## Error handling

Return RFC 7807 `ProblemDetail` through a single `@RestControllerAdvice`, map validation failures to `400`, and attach a correlation ID to connect logs and responses.

```java
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        return problem(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    private ProblemDetail problem(HttpStatus status, String detail) {
        ProblemDetail body = ProblemDetail.forStatusAndDetail(status, detail);
        body.setProperty("correlationId", MDC.get("correlationId"));
        return body;
    }
}
```

## Logs and sensitive data

> [!WARNING]
> Never log CPF, benefit amounts, tokens, or other sensitive data. Log identifiers and the correlation ID, and mask every regulated field before it reaches a log or error message.

```java
// Wrong: log.info("payment for CPF {} in the amount of {}", cpf, amount);
log.info("payment processed correlationId={} resourceId={}", correlationId, id);
```

## Conventions

| Rule | Rationale |
|---|---|
| Controllers in `PascalCase`; `/api/v1/{resource}` routes in kebab-case | Predictable, versioned HTTP surface |
| `@Transactional` only in services | Repositories and controllers represent side effects honestly |
| Records for request/response DTOs | Immutable contracts with explicit boundaries |
| `@Valid` + Bean Validation in controllers | Rejects invalid input before business logic |
| `Optional` for absent results | Eliminates `NullPointerException` in public APIs |
| `ProblemDetail` (RFC 7807) for every error | A single machine-readable error format |

## Do / Don't

| Do | Don't |
|---|---|
| Return `201`/`204`/`409` where applicable | Return `200` for every outcome |
| Throw domain exceptions mapped in the advice | Return raw stack traces or `Map<String,Object>` errors |
| Inject dependencies through the constructor | Use field `@Autowired` |
| Mask CPF and amounts in logs | Log entities, request bodies, or tokens |

## PR Checklist

- [ ] Every endpoint uses `/api/v1/{resource}`, the correct verb, and the correct status
- [ ] Every endpoint has OpenAPI annotations and a validated `record` request body
- [ ] `@Transactional` appears only in services; no public method returns `null`
- [ ] Errors pass through `@RestControllerAdvice` as `ProblemDetail` with a correlation ID
- [ ] No sensitive data (CPF, amounts, tokens) reaches logs or error payloads
- [ ] Tests cover the success path, a validation failure, and an authentication failure (see [`tests.instructions.md`](tests.instructions.md))
