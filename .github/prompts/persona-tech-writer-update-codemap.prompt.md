---
name: "update-codemap"
description: "Generate or update docs/CODEMAP.md, a curated, navigable index of the SIFAP 2.0 codebase: modules, owners, entry points, and tests."
argument-hint: "mode=update|rebuild root=<repo-root>"
agent: "tech-writer"
tools: ["search", "edit"]
---
# /update-codemap

## Objective

Maintain `docs/CODEMAP.md` as a one-page guide that locates a module, its owner, entry points, and tests in ten minutes.

## When to Invoke

In Stages 3 or 4, after an addition or rename.

## Preconditions

- The team has created a module
- [`DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) and owners from [`05-personas/`](../../05-personas/) apply

## Inputs the Team Must Provide

- Root, `update` or `rebuild`, and the previous map

## What I Will Do

- Record purpose, entry points, state, REQ-IDs, owning persona, tests, and confirmed lineage
- Flag more than three dependencies, order by value, and limit to 200 lines
- Apply [`doc-style-lint`](../skills/doc-style-lint/SKILL.md)

## What I Will NOT Do

- Turn `find` into a map, invent Natural behavior, list every file, use `*` for endpoints, teams as owners, emojis, or a pragma

## Output Format

`docs/CODEMAP.md` with a guide, backend, frontend, infrastructure, libraries, concerns, and update information.

## Definition of Done

- [ ] Each module has Purpose, Path, Tests, Entry Points, State, REQ-IDs, and Owner
- [ ] Lineage is confirmed; dependencies are declared; date and footer are present

## Prompt Body

You are `@tech-writer`. Confirm the mode and preserve curation during an update. Locate the services, routes, and infrastructure modules that have been created. Record five facts and the persona from `05-personas/`, link tests, and cite only proven lineage. Flag dependencies and place critical journeys before infrastructure. Limit to 200 lines or split with links. Update the date and footer. Do not generate automatically.

## Example Invocation

```text
/update-codemap mode=update root=.
```
