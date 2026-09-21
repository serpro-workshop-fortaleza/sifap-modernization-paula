---
name: "map-dependencies"
description: "Maps program-to-program (CALLNAT, INCLUDE) and program-to-data (DDM access) dependencies in the selected scope."
argument-hint: "scope=01-archaeology/legacy-sifap/natural-programs/ recursive=true"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /map-dependencies

## Objective

Build a dependency graph for a selected scope of the legacy codebase by tracing CALLNAT calls, INCLUDE directives, and DDM data access patterns. Generate a Mermaid diagram in which every edge cites its source.

## When to Invoke

After the team completes the initial inventory and wants to understand relationships between programs and data.

## Preconditions

- `01-archaeology/inventory.md` exists
- `01-archaeology/legacy-sifap/` is accessible
- The team has selected a scope: a program, batch flow, or transaction family

## Inputs the Team Must Provide

- The scope: a file path, directory, or set of files
- Whether tracing will be recursive, following CALLNAT targets, or only one level deep

## What I Will Do

- Search for all `CALLNAT`, `PERFORM`, and `INCLUDE` statements in scope
- Identify each CALLNAT target subprogram and verify its existence
- Search for `READ`, `FIND`, `GET`, `STORE`, `UPDATE`, `DELETE`, and `HISTOGRAM`, with references to the target DDM or file
- Build a Mermaid graph with program-to-program and program-to-data dependencies
- List broken references to missing programs

## What I Will NOT Do

- Invent connections absent from the source code; every edge will have a file and line
- Assume a CALLNAT target's function from its name; map only the edge
- Assume structures; read what actually exists
- Follow references outside `01-archaeology/legacy-sifap/`

## Output Format

A Mermaid file at `01-archaeology/dependency-map.mmd` and a supporting file at `01-archaeology/dependency-map.md`:

```markdown
# Dependency map - [Scope description]
## Mermaid diagram
## Program-to-program edges
| Source | Target | Type | File | Line |
## Program-to-data edges
| Program | DDM/file | Operation | File | Line |
## Broken references
## Notes
```

## Definition of Done

- [ ] The Mermaid file exists and renders a valid graph
- [ ] Every node corresponds to a real file
- [ ] Every edge cites its source file and line
- [ ] Broken references are explicitly listed
- [ ] Data access edges distinguish READ, FIND, STORE, UPDATE, and DELETE

## Prompt Body

You are `@archaeologist`. The team wants to map dependencies in part of the legacy codebase. Trace all program-to-program and program-to-data relationships.

**Step 1 - Identify the scope.**
Confirm whether it is a program, directory, or named set. Record the boundary and do not search beyond it without an explicit request for recursive tracing.

**Step 2 - Search for CALLNAT.**
For each `CALLNAT`, extract the calling program, target subprogram name, line, and passed parameters without interpreting them. Check whether the target exists in `01-archaeology/legacy-sifap/`; otherwise, record a broken reference.

**Step 3 - Search for INCLUDE.**
For each `INCLUDE`, extract the program, copycode name, and line. Verify that the copycode exists.

**Step 4 - Search for PERFORM.**
Record `PERFORM` as an internal dependency. Do not create program-to-program graph edges for these dependencies; list them in a separate section.

**Step 5 - Search for data access.**
For `READ`, `FIND`, `GET`, `STORE`, `UPDATE`, `DELETE`, and `HISTOGRAM`, extract the program, DDM or file number, operation, line, and descriptor used in FIND or READ LOGICAL.

**Step 6 - Build the Mermaid graph.**
Use rectangles for programs, cylinders `[(name)]` for data, solid "CALLNAT" arrows, dashed "INCLUDE" arrows, and data edges labeled with the operation. Preserve the palette: fill `#0f172a`, stroke `#334155`, text `#e2e8f0`.

**Step 7 - Document broken references and notes.**
List CALLNAT and INCLUDE statements whose targets do not exist. Record the total programs, total edges, most connected program, most accessed DDM, and isolated programs.

**Step 8 - Write the files.**
Write the diagram to `01-archaeology/dependency-map.mmd` and the documentation to `01-archaeology/dependency-map.md`.

Every edge must cite a file and line. Without a verified source, do not include the edge. Do not invent connections.

## Example Invocation

```text
/map-dependencies scope=01-archaeology/legacy-sifap/natural-programs/ recursive=true
```
