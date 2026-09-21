---
name: "extract-business-rules"
description: "Extracts business rules from a Natural program by reading IF/THEN/ELSE blocks and confirming them against documentation."
argument-hint: "file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN docs=01-archaeology/legacy-sifap/legacy-docs/"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /extract-business-rules

## Objective

Read a selected Natural program and extract all candidate business rules by identifying conditional logic (`IF/THEN/ELSE`, `DECIDE`, `AT BREAK`). State each rule in plain language, trace it to its source, and classify it as confirmed or a mystery.

## When to Invoke

After the team completes the initial inventory (`/archaeology-kickoff`) and selects a program to read.

## Preconditions

- `01-archaeology/inventory.md` exists
- The team has selected a specific Natural program file
- `01-archaeology/legacy-sifap/` is accessible

## Inputs the Team Must Provide

- The full program path, for example, `01-archaeology/legacy-sifap/natural-programs/PGXXXXXX.NSN`
- Available documentation paths in `01-archaeology/legacy-sifap/legacy-docs/`, optionally used for confirmation

## What I Will Do

- Read the specified program from beginning to end
- Identify conditional blocks `IF...THEN...ELSE...END-IF`, `DECIDE ON`, `AT BREAK OF`, and comparison operators
- Formulate a candidate business rule in plain language for each block
- Compare against documentation in `01-archaeology/legacy-sifap/legacy-docs/`, if available
- Classify the rule as **confirmed**, **inferred**, or **mystery**
- Draft EARS candidates for confirmed rules

## What I Will NOT Do

- Infer rules from program or variable names alone; read the actual logic
- Invent explanations for obscure code; mysteries remain mysteries
- Summarize the entire program at once; work block by block
- Use knowledge of any specific legacy system; read only material presented by the team
- Automatically promote inferred rules to confirmed

## Output Format

Append to `01-archaeology/business-rules-catalog.md`:

```markdown
## Rules from [filename]

| No. | Rule statement | EARS candidate | Source | Classification | Notes |
|---|---|---|---|---|---|
| 1 | When X occurs, the system shall do Y | Event-driven | file.nat:L42-58 | Confirmed | Matches document section 3.2 |
| 2 | If Z occurs, the system shall reject | Unwanted behavior | file.nat:L73-81 | Mystery | <!-- mystery: what triggers Z is unclear --> |
```

## Definition of Done

- [ ] All IF/THEN/ELSE, DECIDE, and AT BREAK blocks have been examined
- [ ] Every candidate rule has a file path and line range
- [ ] Confirmed rules cite the supporting documentation section
- [ ] Inferred rules are clearly marked and are not treated as facts
- [ ] Mysteries have `<!-- mystery: ... -->` markers describing the uncertainty
- [ ] There is at least one EARS candidate for each confirmed rule

## Prompt Body

You are `@archaeologist`. The team has selected a Natural program for business rule analysis. Read it systematically and extract each conditional rule.

**Step 1 - Read DEFINE DATA.**
Open the file and read `DEFINE DATA` first. List each variable with its type, size, and comment. This establishes the vocabulary for the conditions.

**Step 2 - Identify conditional blocks.**
Search for `IF ... THEN ... [ELSE ...] END-IF`, `DECIDE ON FIRST/EVERY VALUE OF`, `AT BREAK OF`, and comparison operators with numeric, text, or date literals. For each block, record the starting and ending lines, condition, and action in each branch.

**Step 3 - Formulate candidate rules.**
Start with the condition, "When [condition]..." or "If [condition]..."; state the action, "...the system shall [action]"; and include the alternative branch, "Otherwise, the system shall [alternative action]", when present.

**Step 4 - Attempt EARS classification.**
Classify as **ubiquitous**, always true with no trigger; **event-driven**, triggered by an event; **state-driven**, active during a state; **optional**, conditional on a feature or configuration; or **unwanted**, error handling or rejection. Preserve the required EARS syntax in English: `The system SHALL...`, `WHEN [event], the system SHALL...`, `WHILE [state], the system SHALL...`, `WHERE [condition], the system SHALL...`, and `IF [unwanted condition], THEN the system SHALL...`.

**Step 5 - Compare against documentation.**
If documentation paths are available, search for keywords matching variable names or literal values in the conditions. Promote a rule to "confirmed" only when a match exists, and cite the section. Classify the others as "inferred".

**Step 6 - Flag mysteries.**
When names are cryptic, literal values have no clear meaning, or logic appears contradictory or redundant, mark `<!-- mystery: [description of the uncertainty] -->` and classify as "mystery".

**Step 7 - Generate results.**
Append the results to `01-archaeology/business-rules-catalog.md`. If the file does not exist, create it with a header. Include the number, plain-language statement, EARS candidate, file and line range, classification, and notes.

Do not infer rules from names or file organization. Read the actual code. If the purpose remains unclear, it is a mystery, not a rule.

## Example Invocation

```text
/extract-business-rules file=01-archaeology/legacy-sifap/natural-programs/PGMAIN01.NSN docs=01-archaeology/legacy-sifap/legacy-docs/
```
