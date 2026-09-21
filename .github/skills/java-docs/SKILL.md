---
name: "java-docs"
description: "Apply Javadoc best practices to correctly document Java types and members: summary sentences, @param/@return/@throws, {@code} blocks, @since, and inherited documentation. Use when someone requests creating, reviewing, or improving Javadoc or API documentation for Java code."
---
# Java documentation (Javadoc)

Write and review Javadoc for the SIFAP 2.0 backend (Java 21 + Spring Boot 3.3) so that every public and protected member has a correct, consistent contract. This skill defines Javadoc conventions: it teaches how to document behavior, does not decide code design, and never includes real regulated values, such as CPF or benefit amounts, in examples.

## When to Invoke

- "Write Javadoc for this service class."
- "Review this package's Javadoc and fill in any gaps."
- "Document this module's public API before release."
- "Add `@param`/`@return`/`@throws` to these methods."

## What to document

| Visibility | Rule |
|---|---|
| `public`, `protected` | Javadoc is required because these members form the API contract |
| package-private (package-restricted access) | Document when the intent is not obvious from the name |
| `private` | Document only genuinely complex logic; prefer clear code to comments |

> [!NOTE]
> Document the contract, meaning what the caller can rely on, not the implementation. Never include real CPF, benefit amounts, tokens, or other sensitive data in a Javadoc example. Use clearly fictitious placeholders.

## Summary sentence

- The first sentence is the summary. It ends with a period and should be a short verb phrase ("Returns...", "Registers...").
- Start method summaries with a third-person verb ("Calculates the tax..."), not "This method...".
- Focus the summary on the contract and move details to subsequent paragraphs.

## Block tags

| Tag | When to use | Format rule |
|---|---|---|
| `@param name` | Every method or constructor parameter | The description starts with a lowercase letter and has no final period |
| `@param <T>` | Every type parameter of a generic type or method | The same lowercase and no-period rule |
| `@return` | Every value-returning method (omit for `void`) | Describe the value, including `Optional` semantics |
| `@throws` / `@exception` | Every checked exception and every documented unchecked exception | State the triggering condition |
| `@see` | Cross-references to related types or members | Link without repeating content |
| `@since` | When the member was introduced | Use the project or module version |
| `@deprecated` | A member scheduled for removal | Identify the replacement and add `@Deprecated` to the code |

Optional: include `@author` and `@version` only if the team's convention requires them. Many style guides omit `@author` and prefer version control history.

> [!WARNING]
> Order the tags: `@param` (in declaration order), followed by `@return` and `@throws`. A missing or out-of-order `@param` is the most common defect in Javadoc reviews.

## Inline tags and code

- Use `{@code ...}` for identifiers, keywords, and inline literals (`{@code null}`, `{@code Optional.empty()}`).
- Use `{@link Type#member}` to link to another element and `{@linkplain ...}` for plain link text.
- Use `<pre>{@code ... }</pre>` for multiline examples so that generics and angle brackets render literally.
- Use `{@inheritDoc}` to inherit a supertype's contract, but document any genuinely different behavior again.

## How to document Java 21 records

A record's Javadoc belongs on the type. Document each component with `@param`. Do not add accessors just to attach Javadoc to them.

## Output Template

```java
/**
 * Registers a payment resource and returns its stored representation.
 *
 * <p>The label must be unique; a duplicate is rejected, not merged.
 *
 * @param request the validated creation request; must not be {@code null}
 * @return the persisted resource as a response DTO
 * @throws ResourceConflictException if a resource with the same label already exists
 * @since 1.0.0
 * @see ResourceService#getById(java.util.UUID)
 */
ResourceResponse create(CreateResourceRequest request);

/**
 * Immutable creation request for a payment resource.
 *
 * @param label  a unique, human-readable label (maximum 120 characters)
 * @param amount the positive monetary amount to register
 */
public record CreateResourceRequest(String label, BigDecimal amount) {}
```

## Quality Gate

- [ ] Every public and protected member has a Javadoc summary sentence ending with a period.
- [ ] Every parameter, including `<T>` type parameters, has a `@param`; every non-`void` method has a `@return`.
- [ ] Every documented exception has a `@throws` describing its triggering condition.
- [ ] `{@code}` and `{@link}` wrap identifiers instead of plain text, and block tags are in the correct order.
- [ ] No example contains real CPF, benefit amounts, or other sensitive data.
- [ ] `mvn javadoc:javadoc` (or Gradle's `javadoc` task) generates documentation without warnings.
