---
name: "doc-style-lint"
description: "Use when reviewing documentation for style, clarity, inclusive language, or compliance with Microsoft or Google style guides. Triggers include \"documentation review\", \"style guide\", \"plain language\", \"inclusive language\", and \"readability\"."
---
# Documentation style lint

## When to Invoke

- "Check this README against our style guide."
- "Rewrite this API documentation in plain language."
- "Look for exclusionary terms and jargon."

## Rules

### Voice and tone

- **Active voice**. Use "The system stores the file", not "The file is stored by the system".
- **Present tense**. Use "Returns a JSON response", not "Will return a JSON response".
- **Second person** ("you") in how-to guides; **third person** in reference documentation.
- **Sentence case headings**, not title case.

### Clarity

- One idea per sentence.
- Use 25 words per sentence as a practical maximum.
- Use at most five sentences per paragraph.
- Avoid words that minimize difficulty ("just", "simply", "easily"). They mislead readers.
- Do not use em dashes. Use commas, parentheses, or colons.

### Inclusive language

Replace:

- `master/slave` -> "primary/replica" or "leader/follower"
- `whitelist/blacklist` -> "allowlist/blocklist"
- `guys` -> "folks", "everyone", "team"
- `crazy/insane` (as intensifiers) -> "significant", "unusual"
- `dummy` (in variable names) -> `example`, `sample`
- `sanity check` -> "quick check", "verification"

### Structure

- **Lead with the outcome**, not the context. Readers should know why to continue.
- **State up front what will be learned**.
- **Summarize at the end** of long documents.
- **Use descriptive headings** to support scanning.

### Hyperlinks

- Link text describes the destination. Never use "click here" or "this link".
- Use absolute URLs for external sources and relative URLs for internal content.
- Check links in continuous integration (CI).

### Code examples

- Test every executable snippet.
- Use realistic examples, not `foo/bar/baz`.
- Clearly identify placeholders: `<YOUR-API-KEY>`.

### Numbers and units

- Use numerals for 10 or more and words for zero through nine (Microsoft style).
- Use metric units and include conversions for mixed audiences.
- Always specify the unit: "100 MB", not "100".

## Review steps

1. **Read once as the target audience**. Are the length and level of detail appropriate?
2. **Run the automated checks configured in the repository**, such as Vale, Alex.js, or markdownlint. Report missing tools without installing them.
3. **Apply the style rules** section by section.
4. **Test all code examples**.
5. **Ask**: would a new hire understand this on their first day?

## Anti-patterns

- Reviewing without first running automated checkers.
- Prioritizing style over substance.
- Rewriting the author's voice instead of refining it.
- Ignoring accessibility (alt text, heading levels, and link text).

## Output Template

```markdown
## Style review: <Document>

### Summary
- Readability (Flesch-Kincaid grade): 11 (target: <=12)
- Passive voice: 8% (target: <10%)
- Inclusive language issues: 2
- Broken links: 0
- Untested code examples: 3

### Recommendations (top 10)
| ID | Location | Issue | Fix |
|----|----------|-------|-----|
| 01 | Installation section | Passive voice | Rewrite in active voice |
| 02 | Troubleshooting | "the guys" | Replace with "the team" |
| 03 | API reference | "just call" | Remove "just" |
```

## Quality Gate

- [ ] The document passes the repository's configured checkers (for example, Vale, Alex.js, and markdownlint) before human review.
- [ ] Text uses active voice and present tense, with sentence case headings.
- [ ] No exclusionary terms remain; flagged terms were replaced with inclusive alternatives.
- [ ] All code examples have been tested and all links work.
