---
name: "translate-natural-to-java"
description: "Translates a Natural program into idiomatic Java 21 + Spring Boot 3.3, preserving business semantics."
argument-hint: "file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN context=<context> package=<java.package>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /translate-natural-to-java

## Objective

Translate Natural into idiomatic Java 21 + Spring Boot 3.3, preserving semantics, with compilation and traceable Javadoc.

## When to Invoke

At the start of Stage 3, when implementing Stage 2 contexts.

## Preconditions

- `plan.md` and `spec.md` exist
- The context, package, Natural source, and REQ-IDs are known

## Inputs the Team Must Provide

- Natural path, context, package, and REQ-IDs

## What I Will Do

- Read block by block, identify purpose, translate using Java 21 features, and generate Javadoc and test stubs
- Flag orphan logic without a REQ-ID

## What I Will NOT Do

- Port line by line ("JOBOL"), silently combine concepts, invent meaning, or ignore EARS

## Output Format

Files in `src/main/java/` and stubs in `src/test/java/`, with source Javadoc.

## Definition of Done

- [ ] Compiles
- [ ] Public methods cite the Natural file and lines
- [ ] Each EARS rule has a method
- [ ] Orphans use `// ORPHAN: [file:line] - Team decision required`
- [ ] There is a stub per method and idiomatic use of Java 21

## Prompt Body

You are `@builder`. Translate the selected program.

**Step 1 - Read EARS.** Read `spec.md` and list relevant requirements.

**Step 2 - Read Natural.** Analyze `DEFINE DATA`, `IF` decisions, `READ`/`FIND` access, `CALLNAT` dependencies, and `PERFORM` subroutines.

**Step 3 - Map blocks.** Associate each block with a REQ-ID. For orphans:

```java
// ORPHAN: [natural-file.NSN:L42-58] - No matching REQ. Team decision required: keep, modify, or remove?
```

Consult the team before proceeding.

**Step 4 - Translate.** Map variables to Java types; conditions to `if/else` or `switch`; `READ LOGICAL BY` to `findBy*`; `FIND WITH` to named `@Query`; `CALLNAT` to an injected service; decimals to `BigDecimal` with scale and rounding; and strings with attention to charset. Use records, sealed interfaces, `Optional`, constructor injection, `@Valid`, and `@Transactional` only on services.

**Step 5 - Generate Javadoc.**

```java
/**
 * [Business description].
 *
 * <p>Translated from: {@code [natural-file.NSN#L42-L58]}</p>
 * <p>Implements: REQ-NNN</p>
 */
```

**Step 6 - Create stubs.**

```java
@Test
void should_[expected]_when_[condition]() {
    // Arrange: [describe the setup based on the Natural input parameters]
    // Act: [call the translated method]
    // Assert: [verify against the EARS acceptance criteria]
    fail("TODO: implement — see REQ-NNN acceptance criteria");
}
```

**Step 7 - Compile.** Fix errors. If there is no clean equivalent, present two alternatives and let the team choose.

## Example Invocation

```text
/translate-natural-to-java file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN context=<context> package=<java.package>
```
