---
name: "audit-context"
description: "Audit the repository's Copilot context surface (AGENTS.md, CODEMAP.md, instructions, prompts, and agents) and return prioritized fixes."
argument-hint: "scope=.github"
agent: "tech-lead"
tools: ["read", "search"]
---
# /audit-context

## Objective

Audit `AGENTS.md`, `CODEMAP.md`, instructions, prompts, and agents, and list actual fixes by severity.

## When to Invoke

Periodically, before transitions, or after changes to primitives.

## Preconditions

- `.github/` exists; the instruction and [prompt](README.md) indexes are references

## Inputs the Team Must Provide

- Optional scope

## What I Will Do

- Inventory files and lines; check `applyTo`, CODEMAP freshness, frontmatter, agents, tools, models, paths, and links
- Apply [`context-audit`](../skills/context-audit/SKILL.md)

## What I Will NOT Do

- Create false positives, edit, suggest a fixed model/provider, or rewrite primitives

## Output Format

Table `File | Issue | Severity | Fix` and the top three findings.

## Definition of Done

- [ ] Every High finding has a concrete fix
- [ ] Freshness, all `applyTo` scopes, and links were checked
- [ ] No false positives or application suggestions

## Prompt Body

You are `@tech-lead`. Inventory `.github/instructions/`, `.github/prompts/`, and `.github/agents/`. `applyTo: "**"` or a missing scope is High. A CODEMAP older than 30 days or referencing deleted files is stale. Check descriptions, agent resolution, minimal tools, and the absence of a fixed model. Search for broken paths and links. Sort by High, Medium, Low, and finish with three fixes.

## Example Invocation

```text
/audit-context scope=.github
```
