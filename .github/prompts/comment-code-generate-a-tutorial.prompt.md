---
name: "comment-code-generate-a-tutorial"
description: "Refactor a source file, add educational comments for beginners, and generate a README tutorial, delegating the workflow to the comment-code-generate-a-tutorial skill."
argument-hint: "file=<path-to-source>"
agent: "tech-writer"
tools: ["read", "edit", "search"]
---
# /comment-code-generate-a-tutorial

## Objective

Turn a single source file into educational material: refactor it for clarity, add instructional comments that explain the reasoning, and generate a `README.md` tutorial. The complete workflow is in the [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 stack without repeating it.

> [!NOTE]
> The skill's example uses Python. In this kit, apply it to Java 21 or TypeScript and follow the corresponding style guide.

## When to Invoke

During Stages 3 or 4, when preparing a guided walkthrough for the immersion, for example, to explain a translated module to the rest of the team.

## Preconditions

- The target source file exists and runs or compiles
- The audience and concept to teach are known
- The file contains no unmasked sensitive data

## Inputs the Team Must Provide

- `file`: the path of the source file to document
- The intended audience and educational objective
- Ask the user for any missing information.

## What I Will Do

- Follow the refactor → comment → create tutorial procedure in the [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) skill
- Apply the procedure to the kit's languages: Java 21 on the backend or TypeScript with Next.js 15 on the frontend
- Add instructional comments that explain intent and reasoning, not syntax
- Generate a `README.md` with an overview, setup, how it works, and a usage example

## What I Will NOT Do

- Apply Python or PEP 8 conventions unless the file is actually Python
- Add superficial comments that merely repeat the code
- Include sensitive data, such as CPF and benefit amounts, in examples or outputs
- Write the tutorial in any language other than English

## Output Format

```markdown
### Refactored
`backend/.../PaymentRules.java` — clearer names and instructional comments added

### Tutorial (README.md)
- Project overview
- Setup instructions
- How it works
- Usage example
- Output example (optional)
```

## Definition of Done

- [ ] The code has been refactored for clarity and follows the language's style guide
- [ ] Instructional comments explain the reasoning without adding noise
- [ ] The `README.md` presents an overview, setup, how it works, and a usage example
- [ ] There is no sensitive data and all text is in English

## Prompt Body

The [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) skill defines the refactoring, commenting, and tutorial procedure. Read it and apply it to the file.

**Step 1 — Read and refactor.**
Understand the file and improve names and structure according to best practices for the language, Java 21 or TypeScript.

**Step 2 — Apply the skill.**
Add beginner-friendly instructional comments and generate the `README.md` sections prescribed by the skill.

**Step 3 — Follow the kit's rules.**
Use the correct style guide for the language, write in English, and mask sensitive data.

**Step 4 — Review.**
Confirm that the comments teach intent and that the tutorial is understandable on its own.

## Example Invocation

```text
/comment-code-generate-a-tutorial file=backend/src/main/java/com/sifap/payment/PaymentRules.java
```
