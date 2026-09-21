---
name: "java-springboot"
description: "Apply Spring Boot best practices to the SIFAP 2.0 backend, delegating the detailed checklist to the java-springboot skill."
argument-hint: "target=<file-or-module>"
agent: "implementer"
tools: ["read", "search", "edit"]
---
# /java-springboot

## Objective

Guide building or reviewing a Spring Boot slice of the SIFAP 2.0 backend: package-by-feature organization, constructor injection, DTOs, global exception handling, service-layer transactions, and test slices. This aligns the code with the kit's fixed stack. The detailed checklist is in the [`java-springboot`](../skills/java-springboot/SKILL.md) skill. This prompt applies it without repeating it.

> [!IMPORTANT]
> The stack is fixed: Java 21 + Spring Boot 3.3 + JPA/Hibernate + PostgreSQL 16. Do not offer another framework or database as an alternative.

## When to Invoke

During Stages 3 or 4, when building or reviewing a backend module, after its bounded context is known.

## Preconditions

- The `backend/` module has been created; see `/create-spring-boot-java-project`
- The bounded context and its package have been identified; see [`modular-monolith.instructions.md`](../instructions/modular-monolith.instructions.md)
- The REQ-IDs implemented by the module are known

## Inputs the Team Must Provide

- `target`: the file or module to build or review
- The corresponding bounded context and the REQ-IDs it satisfies
- Ask the user for any missing information.

## What I Will Do

- Follow the best practices in the [`java-springboot`](../skills/java-springboot/SKILL.md) skill and apply them to the target
- Require constructor injection, `private final` fields, DTO boundaries, and request records with `@Valid`
- Keep `@Transactional` in the service layer and route data access through Spring Data JPA
- Source secrets from environment variables backed by Azure Key Vault and Managed Identity

## What I Will NOT Do

- Substitute Quarkus, Micronaut, MongoDB, Redis, or any component outside the kit
- Recommend HashiCorp Vault or AWS Secrets Manager; the kit uses Azure Key Vault
- Expose JPA entities directly through a controller or return `null` from a public method
- Put `@Transactional` on a repository or hardcode a secret

## Output Format

The built or reviewed code, accompanied by a brief compliance note:

```markdown
### Applied
- Constructor injection and `private final` in `PaymentService`
- `/api/v1/payments` controller with `@Valid PaymentRequest` and OpenAPI annotations
- `@Transactional` on the service method only

### Flagged
- `PaymentController` returned the JPA entity → replaced with a `PaymentResponse` DTO
```

## Definition of Done

- [ ] Code is organized by feature, with constructor injection and immutable fields
- [ ] REST paths use `/api/v1/{resource}` and each endpoint has OpenAPI annotations and `@Valid`
- [ ] `@Transactional` appears only in the service layer; no entities are exposed
- [ ] Secrets come from the environment through Azure Key Vault and are never hardcoded

## Prompt Body

The [`java-springboot`](../skills/java-springboot/SKILL.md) skill defines layered best practices. Read it and apply them to the target.

**Step 1 — Place the code.**
Confirm the feature package and bounded context. Organize by domain, not by layer.

**Step 2 — Apply the skill.**
Build or review the web, service, and data layers according to the skill: DTOs at the boundary, exception handling with `@ControllerAdvice`, typed configuration through `@ConfigurationProperties`, and parameterized logging with SLF4J.

**Step 3 — Follow the kit's rules.**
Keep Java 21 + Spring Boot 3.3 + PostgreSQL 16, obtain secrets from Azure Key Vault, and validate all input with `@Valid`.

**Step 4 — Report.**
List the practices applied and violations corrected.

## Example Invocation

```text
/java-springboot target=backend/src/main/java/com/sifap/payment
```
