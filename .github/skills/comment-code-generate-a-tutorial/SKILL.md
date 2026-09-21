---
name: "comment-code-generate-a-tutorial"
description: "Refactor a Python script according to PEP 8, add instructional comments for beginners, and generate a complete README.md tutorial (overview, setup, how it works, and usage example). Use when someone wants to turn a Python script into a polished educational project or produce a step-by-step guide."
---
# Comment code and generate a tutorial

Use this skill to turn a working script into an educational artifact. Refactor the code for clarity, add instructional comments explaining the reasoning behind each decision, and write a `README.md` tutorial that lets beginners run the script and understand how it works. The example uses Python, but the same three-step procedure applies to any language.

> [!NOTE]
> In this immersion, the [`/comment-code-generate-a-tutorial`](../../prompts/comment-code-generate-a-tutorial.prompt.md) prompt applies this procedure to the kit's Java 21 and TypeScript stack. Keep this skill as the authoritative procedural source used by the prompt.

## When to Invoke

- "Refactor this Python script and write a README tutorial for it."
- "Add beginner comments to this script and explain how it works."
- "Turn this utility into an educational project with setup and usage documentation."
- "Generate a step-by-step guide for this script."

## Workflow

### 1. Refactor for clarity

- Apply the language's style guide (PEP 8 for Python).
- Rename unclear variables and functions so their names reveal intent.
- Extract long blocks into small, named functions.
- Keep the public interface and observable output identical. This step improves readability, not rewrites the program.

### 2. Add instructional comments

Explain reasoning, not syntax. A useful comment answers "why"; a poor comment repeats "what".

| Write comments that | Avoid comments that |
|---|---|
| Explain why a design decision was made | Repeat a line, such as `i += 1  # add one` |
| Introduce a language idiom on its first occurrence | Repeat the function name in prose |
| Warn about an edge case or invariant | Narrate obvious control flow |
| Name the concept a beginner should research | Add noise that becomes stale |

### 3. Generate the tutorial

Write a `README.md` alongside the script with these sections: project overview, setup instructions, how it works, usage example, and optionally sample output.

## Rules

- Preserve behavior, file encoding, and line ending style. An educational revision must never break the build.
- Use only standard keyboard characters in code and comments. Do not use emojis.
- Write all comments and tutorial sections in Brazilian Portuguese.
- Never include sensitive data (for example, CPF numbers or benefit amounts) in examples or sample output.
- Run the setup command and example before publishing the tutorial.

## Output Template

The generated `README.md` starts with an H1 naming the project, followed by these sections:

```markdown
## Project overview
`wordcount.py` counts how often each word appears in a text file and
displays the most frequent entries. It demonstrates file reading, aggregation
with dictionaries, and sorting in Python.

## Setup
- Requires Python 3.8 or later
- Has no third-party dependencies

Run from the project root:

    python3 wordcount.py sample.txt --top 10

## How it works
1. Read the file and lowercase each line to ignore case differences.
2. Split each line on whitespace and count the words in a dictionary.
3. Sort the dictionary by count and display the top N entries.

## Usage example
    python3 wordcount.py article.txt --top 5

## Sample output
    the      42
    and      31
    data     27
```

## Quality Gate

- [ ] The script still works and produces identical output after refactoring.
- [ ] Names reveal intent and no behavior changed during the readability improvement.
- [ ] Comments explain reasoning and language idioms, not obvious syntax.
- [ ] The `README.md` includes an overview, setup, how it works, and usage example.
- [ ] The setup command and example have been tested and are correct.
- [ ] Everything is written in Brazilian Portuguese, without emojis or sensitive data.
