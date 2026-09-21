---
name: "implement-rest-controller"
description: "Implements a Spring REST controller from an OpenAPI endpoint definition and connects it to the bounded context's services."
argument-hint: "endpoint=\"<METHOD /api/v1/resource>\" context=<context> service=<Service>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /implement-rest-controller

## Objective

Generate a Spring Boot REST controller from OpenAPI. The controller is a thin adapter: it validates, delegates, and returns, without business logic.

## When to Invoke

After the service layer exists and the team wants to expose it through REST.

## Preconditions

- OpenAPI contains the endpoint
- The service or interface exists
- DTOs exist or will be records

## Inputs the Team Must Provide

- OpenAPI method and path
- Context and package
- Target service

## What I Will Do

- Read OpenAPI, generate `@RestController`, records with Bean Validation, constructor injection, and `@ControllerAdvice` if needed
- Compile the project

## What I Will NOT Do

- Put logic in the controller, omit `@Valid`, use `@Autowired` field injection, hardcode messages, or invent behavior
- Errors will use RFC 7807 `ProblemDetail`

## Output Format

1. `src/main/java/[package]/api/[Name]Controller.java`
2. DTOs in `src/main/java/[package]/api/dto/`
3. `src/main/java/[package]/shared/exception/GlobalExceptionHandler.java`, if absent

## Definition of Done

- [ ] Compiles; Javadoc cites `operationId` and REQ-IDs
- [ ] The DTO uses `@NotNull`, `@Size`, etc.
- [ ] Status codes are 201 for POST, 200 for GET, and 204 for DELETE
- [ ] The controller only validates, delegates, and maps
- [ ] Errors use `ProblemDetail`

## Prompt Body

You are `@builder`. Implement the specified OpenAPI endpoint.

**Step 1 - Read OpenAPI.** Extract the method, path, operation ID, summary, schemas, parameters, and REQ-IDs.

**Step 2 - Generate records.**

```java
public record [RequestName](
    @NotNull [FieldType] [requiredField],
    @Size(max = [maxLength]) String [optionalTextField]
) {}
```

**Step 3 - Generate the controller.** Use `@RestController`, `@RequestMapping`, `@Tag`, a `private final` field, a constructor, `@Operation`, `@Valid`, service delegation, and `ResponseEntity`. Preserve technical placeholders and OpenAPI data.

**Step 4 - Ensure error handling.** If needed, create handlers: `MethodArgumentNotValidException` -> 400; `EntityNotFoundException` -> 404; `IllegalStateException` -> 409; `Exception` -> safe 500, without a stack trace.

**Step 5 - Compile.** Run `mvn compile` or equivalent and fix errors. If the interface is missing, generate a minimal signature with a TODO implementation for the team.

## Example Invocation

```text
/implement-rest-controller endpoint="<METHOD /api/v1/resource>" context=<context> service=<Service>
```
