---
name: "setup-project"
description: "Initialize a project's Copilot context-engineering structure: AGENTS.md, CODEMAP.md, and the foundation of instructions, prompts, and agents in .github."
argument-hint: "root=<repo-root>"
agent: "tech-lead"
tools: ["read", "search", "edit", "execute"]
---
# /setup-project

## Objective

Create `AGENTS.md`, `CODEMAP.md`, `.github/copilot-instructions.md`, and stack-specific foundations for instructions, prompts, and agents, scoped and free of secrets. Do not create a prototype.

## When to Invoke

At the start of a project or when the context surface is missing.

## Preconditions

- Writable root and agreement with [`copilot-instructions.md`](../copilot-instructions.md)

## Inputs the Team Must Provide

- Root and stack, if undetectable

## What I Will Do

- Detect the stack from manifests; create AGENTS with verified commands, CODEMAP with Modules/Data Flow/External Integrations, and `.github/` files with specific `applyTo` scopes
- Stage the changes without committing, list files, and recommend `/audit-context`

## What I Will NOT Do

- Create an application, `backend/`, `frontend/`, or `infra/`; use generic content, `applyTo: "**"`, secrets, credentials, or `TODO`; add an unapproved tool

## Output Format

List of staged files, suggested commit message, and three manual follow-ups.

## Definition of Done

- [ ] AGENTS is specific; all scopes are concrete
- [ ] No secrets or TODO; `.gitignore` adjusted
- [ ] Changes staged, not committed, and follow-ups listed

## Prompt Body

You are `@tech-lead`. Detect `package.json`, `pom.xml`, `requirements.txt`, and `*.csproj`; ask if none exist. Write AGENTS with the stack and commands. Create CODEMAP with `## Modules`, `## Data Flow`, `## External Integrations`, leaving modules to `/update-codemap`. Record language, tone, security, and tools in copilot-instructions without repeating global guidance. Create instructions with globs such as `backend/**/*.java`, never `**`, following [`instructions/README.md`](../instructions/README.md). Stage with git without committing and report absolute paths, a suggested message, and three actions. Do not create a prototype or placeholder.

## Example Invocation

```text
/setup-project root=.
```
