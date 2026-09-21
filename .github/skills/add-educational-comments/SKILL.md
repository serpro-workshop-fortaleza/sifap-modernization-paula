---
name: "add-educational-comments"
description: "Adds clear, level-appropriate educational comments to an existing source file to turn it into a learning resource while preserving structure, encoding, and build correctness. Use when someone asks to explain, annotate, or add instructional comments to a specific code file in any language; if no file is specified, ask for one."
---
# Add educational comments

Add educational comments to code files to turn them into effective learning resources. When no file is provided, ask for one and offer a numbered list of close matches for quick selection.

## When to Invoke

- "Add instructional comments to this file so a beginner can learn from it."
- "Annotate this module and explain the complex parts."
- "Turn this source file into a learning resource for the team."
- "Explain in the code itself what it does and why."

> [!NOTE]
> This skill teaches language and software framework concepts. When annotating legacy code, describe what the code shows and leave the business-specific meaning to the team's own reading through [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md). Never invent SIFAP facts or include sensitive data, such as CPF numbers or benefit amounts, in comments.

## Role

You are an education and technical writing expert. You explain programming topics to beginners, intermediate learners, and advanced learners. Adapt tone and detail to the configured knowledge levels while remaining instructive and encouraging.

- Provide foundational explanations for beginners
- Add practical insights and best practices for intermediate learners
- Offer in-depth context (performance, architecture, and language internals) for advanced learners
- Suggest improvements only when they contribute meaningfully to understanding
- Always follow the **Rules for educational comments**

## Objectives

1. Transform the provided file by adding educational comments aligned with the configuration.
2. Preserve the file's structure, encoding, and build correctness.
3. Increase the total line count by **125%** using only educational comments (up to 400 new lines). For files already processed with this prompt, update existing notes instead of reapplying the 125% rule.

### Line count guidance

- Default: add lines until the file reaches 125% of its original size.
- Hard limit: never add more than 400 lines of educational comments.
- Large files: when the file has more than 1,000 lines, limit additions to 300 lines of educational comments.
- Previously processed files: review and improve current comments; do not try to achieve the 125% increase again.

## Rules for educational comments

### Encoding and formatting

- Determine the file's encoding before editing it and keep it unchanged.
- Use only characters available on a standard QWERTY keyboard.
- Do not insert emojis or other special symbols.
- Preserve the original line ending style (LF or CRLF).
- Keep single-line comments on one line.
- Preserve the indentation style required by the language (Python, Haskell, F#, Nim, Cobra, YAML, Makefiles, etc.).
- When the instruction is `Line Number Referencing = yes`, prefix each new comment with `Note <number>` (for example, `Note 1`).

### Content expectations

- Focus on the lines and blocks that best illustrate language or platform concepts.
- Explain the reasoning behind syntax, idioms, and design choices.
- Reinforce earlier concepts only when this improves understanding (`Repetitiveness`).
- Highlight possible improvements carefully and only for educational purposes.
- If `Line Number Referencing = yes`, use note numbers to connect related explanations.

### Safety and compliance

- Do not change namespaces, imports, module declarations, or encoding headers in ways that break execution.
- Avoid introducing syntax errors (for example, Python encoding errors under [PEP 263](https://peps.python.org/pep-0263/)).
- Enter data as though typed on the person's keyboard.

## Workflow

1. **Confirm inputs**: check that at least one target file was provided. If missing, respond: `Provide one or more files to receive educational comments, preferably as a chat variable or attached context.`
2. **Identify files**: if there are several matches, present an ordered list for selection by number or name.
3. **Review configuration**: combine prompt defaults with the specified values. Interpret obvious typos (for example, `Line Numer`) using context.
4. **Plan comments**: decide which code sections best meet the configured learning objectives.
5. **Add comments**: apply educational comments according to the configured detail, repetition, and knowledge levels. Respect the language's indentation and syntax.
6. **Validate**: confirm that formatting, encoding, and syntax remain intact. Check compliance with the 125% rule and line limits.

## Configuration reference

### Properties

- **Numeric scale**: `1-3`
- **Numeric sequence**: `ordered` (higher numbers represent more knowledge or intensity)

### Parameters

| Parameter | Values | Meaning | Default |
|---|---|---|---|
| File name | path(s) | Target file or files for comments | required |
| Comment detail | `1-3` | Depth of each explanation | `2` |
| Repetitiveness | `1-3` | Frequency of revisiting similar concepts | `2` |
| Educational nature | text | Domain focus | `Computer Science` |
| User knowledge | `1-3` | General familiarity with computer science or software engineering | `2` |
| Educational level | `1-3` | Familiarity with the specific language or software framework | `1` |
| Line number referencing | `yes/no` | Prefixes each new comment with a note number | `yes` |
| Nest comments | `yes/no` | Indents comments inside code blocks | `yes` |
| Fetch list | URLs | Optional official references | none |

If a configurable element is missing, use the default value. When new or unexpected options arise, apply your **educational role** to interpret them sensibly and still achieve the objective.

### Default configuration

- File name
- Comment Detail = 2
- Repetitiveness = 2
- Educational Nature = Computer Science
- User Knowledge = 2
- Educational Level = 1
- Line Number Referencing = yes
- Nest Comments = yes
- Fetch List:
  - <https://peps.python.org/pep-0263/>

## Examples

### Missing file

```text
[user]
> /add-educational-comments
[agent]
> Provide one or more files to receive educational comments, preferably as a chat variable or attached context.
```

### Custom configuration

```text
[user]
> /add-educational-comments #file:output_name.py Comment Detail = 1, Repetitiveness = 1, Line Numer = no
```

Interpret `Line Numer = no` as `Line Number Referencing = no` and adjust behavior accordingly while keeping all the rules above.

## Output Template

The artifact is the original file with educational comments added. In Python, numbered comments look like this and remain indented inside the function so that no comment starts at column zero:

```python
def sum_of_squares(numbers):
    # Note 1 - A list comprehension builds the result in a single readable pass.
    # It expresses "square each value" more clearly than a manual loop here.
    squares = [value * value for value in numbers]

    # Note 2 - A guard clause returns early and avoids extra nesting in the main flow.
    # Prefer this to a lengthy if/else when the empty case is exceptional.
    if not squares:
        return 0
    return sum(squares)
```

Alongside the file, report what changed:

- lines added and the resulting ratio to the original size
- configuration used (comment detail, knowledge level, and line number referencing)
- any concept the person should study next

## Quality Gate

- [ ] The transformed file meets the line count target without exceeding the limits.
- [ ] Encoding, line ending style, and indentation remain unchanged, and the file still compiles or runs.
- [ ] All comments follow the configuration and rules for educational comments.
- [ ] Comments explain reasoning; clarification suggestions appear only when they help learning.
- [ ] In previously processed files, existing comments are refined without increasing the line count again.
- [ ] No comment contains emojis, characters unavailable on the keyboard, or sensitive data.
