---
name: "java-docs"
description: "Apply Javadoc best practices to Java types and members, delegating the complete checklist to the java-docs skill."
argument-hint: "target=<file-or-package>"
agent: "tech-writer"
tools: ["read", "edit", "search"]
---
# /java-docs

## Objective

Bring the Javadoc of a Java file or package into line with the project standard: summary sentences, `@param`, `@return`, `@throws`, generics, and `{@code}` blocks. This documents public and protected members correctly and consistently. The detailed checklist is in the [`java-docs`](../skills/java-docs/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 backend without repeating it.

> [!NOTE]
> Document the why, not the what: the summary sentence states intent and does not repeat the method signature.

## When to Invoke

During Stages 3 or 4, when implementing or reviewing backend Java, after the class or package compiles and its public interface is stable enough for documentation.

## Preconditions

- The target `.java` file or package exists and compiles
- The public and protected interface to document has been identified
- The code follows the Java 21 conventions in [`backend.instructions.md`](../instructions/backend.instructions.md)

## Inputs the Team Must Provide

- `target`: the file or package to document, for example, `backend/src/main/java/com/sifap/payment`
- Domain terms that clarify the intent of the summary sentence
- Ask the user for any missing information.

## What I Will Do

- Apply the Javadoc conventions in the [`java-docs`](../skills/java-docs/SKILL.md) skill to all public and protected members of the target
- Write a concise summary sentence for each member and document parameters, return values, thrown exceptions, and type parameters
- Use `{@inheritDoc}` when behavior is unchanged and document the difference when it changes
- Keep compiled behavior unchanged; modify documentation only

## What I Will NOT Do

- Add unnecessary comments that repeat the signature or the obvious
- Change method bodies, signatures, or visibility to make documentation easier
- Include sensitive data, such as CPF and benefit amounts, in `{@code}` examples; I will mask it
- Write Javadoc in any language other than English

## Output Format

The target files with Javadoc added in place, plus a brief summary:

```markdown
### Documented
| Member | Javadoc added |
|---|---|
| `PaymentService#approve(PaymentId)` | summary, `@param`, `@return`, `@throws` |

### Skipped
- `PaymentService#toString()` — self-explanatory; no Javadoc needed.
```

## Definition of Done

- [ ] Each public and protected member has a summary sentence ending with a period
- [ ] `@param`, `@return`, `@throws`, and `@param <T>` are present where applicable
- [ ] No example contains sensitive data
- [ ] All Javadoc is in English and the file still compiles

## Prompt Body

The [`java-docs`](../skills/java-docs/SKILL.md) skill defines all Javadoc conventions. Read it and apply it to the target.

**Step 1 — Locate the interface.**
Open `target` and list all public and protected types and members without correct Javadoc.

**Step 2 — Apply the skill.**
Document each member according to the skill: a summary sentence first; then lowercase `@param` descriptions without a final period, `@return`, `@throws`, `@param <T>`, and `{@code}` or `<pre>{@code ...}</pre>` where useful.

**Step 3 — Follow the kit's rules.**
Keep behavior unchanged, write in English, and mask CPF and benefit amounts in examples.

**Step 4 — Report.**
Summarize what was documented and what was deliberately skipped.

## Example Invocation

```text
/java-docs target=backend/src/main/java/com/sifap/payment
```
