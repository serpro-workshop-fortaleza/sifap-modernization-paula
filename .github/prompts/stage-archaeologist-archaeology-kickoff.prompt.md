---
name: "archaeology-kickoff"
description: "Starts Stage 1, guides the team through the legacy directory, and produces an initial inventory."
argument-hint: "path=01-archaeology/legacy-sifap/"
agent: "archaeologist"

tools: ["read", "search", "edit"]
---
# /archaeology-kickoff

## Objective

Guide the team through the legacy codebase with a top-down inventory before reading any program. This is the first Stage 1 activity: map the terrain before investigating.

## When to Invoke

At the start of Stage 1, immediately after the team receives access to the `01-archaeology/legacy-sifap/` directory.

## Preconditions

- The `01-archaeology/legacy-sifap/` directory is available in the workspace; it is part of the kit and does not depend on a setup script
- The team has not opened individual programs yet

## Inputs the Team Must Provide

- The legacy directory path, usually `01-archaeology/legacy-sifap/`
- Confirmation that the team has not started reading individual files; this prompt is for orientation, not in-depth reading

## What I Will Do

- Recursively traverse `01-archaeology/legacy-sifap/` and list all directories
- Count files by extension (`.NSN`, `.cpy`, `.ddm`, `.map`, and any others)
- Classify programs by naming prefixes, for example, `BN-*` for batch and `PG-*` for online
- Flag the three items that appear unusual by name length, file size, or location
- Propose a reading order based on the classification

## What I Will NOT Do

- Open or read individual program files; later prompts will handle this
- State what the programs do; the team will discover that independently
- Invent explanations for naming conventions; mark unexplained prefixes as unknown
- Reference system-specific internals; work only with what the directory structure reveals

## Output Format

A Markdown file at `01-archaeology/inventory.md` containing:

```markdown
# Legacy inventory - [Team name]
## Directory structure
## File counts by type
## Naming patterns
## Unusual items (top three)
## Proposed reading order
```

## Definition of Done

- [ ] The inventory file exists and documents the directory structure
- [ ] Counts are correct and another team member can verify them with `find`
- [ ] At least three naming patterns have been identified with their counts
- [ ] Three apparently unusual items have been flagged with paths and reasons
- [ ] The proposed reading order is justified by naming patterns or structural position

## Prompt Body

You are `@archaeologist`, starting a Stage 1 orientation with the team. The team has just received the legacy codebase and has not opened any files yet.

Execute the following steps in order. Do not skip any.

**Step 1 - Map the directory tree.**
List all directories and subdirectories under the supplied legacy path. Display the tree and count the total directories.

**Step 2 - Count files by extension.**
Report the count for every extension found (`.NSN`, `.cpy`, `.ddm`, `.map`, `.txt`, `.md`, or another). Present the table `| Extension | Count | Likely purpose |`. For "Likely purpose", use only general Natural/Adabas knowledge, for example, `.NSN` = Natural source program, `.cpy` = copycode, and `.ddm` = Data Definition Module. Do not assume specific file contents.

**Step 3 - Identify naming patterns.**
Examine names without opening files. Group them by the prefix formed by the first two or three characters before delimiters such as `-`, `_`, or a digit. For patterns with two or more files, present `| Prefix | Count | Hypothesis |`. Base the hypothesis only on general knowledge of Natural conventions. If the pattern is unclear, use `Unknown - investigate in the next step`.

**Step 4 - Flag unusual items.**
Identify the three most unusual items: largest file, deepest nesting, unique naming pattern, or unique extension. Report the path, reason, and suggested investigation action.

**Step 5 - Propose a reading order.**
Prioritize: (a) batch entry points, usually recognizable by prefixes; (b) DDM files, to understand data before code; and (c) the most connected programs, whose names appear as arguments in other filenames and suggest CALLNAT relationships. State that this is a hypothesis and the order will change when the team traces dependencies.

**Step 6 - Generate the inventory.**
Write the complete inventory to `01-archaeology/inventory.md` in the format above. Include the date, a team-name placeholder, and a note that this is the initial analysis, to be revised while reading the files.

Do not open files to read their contents. This prompt operates only on names and directory structure. If the team asks to read a file, direct them to `/extract-business-rules` or `/map-dependencies`.

## Example Invocation

```text
/archaeology-kickoff path=01-archaeology/legacy-sifap/
```
