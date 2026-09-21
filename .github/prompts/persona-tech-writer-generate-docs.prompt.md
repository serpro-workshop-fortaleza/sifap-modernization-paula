---
name: "generate-docs"
description: "Generate a developer-facing document (README, runbook, API reference, or ADR skeleton) for a SIFAP 2.0 module, faithful to the code and documentation style guide."
argument-hint: "type=readme|runbook|api-reference|adr module=<folder> audience=<who>"
agent: "tech-writer"
tools: ["read", "search", "edit"]
---
# /generate-docs

## Objective

Generate a concise, navigable README, runbook, API reference, or ADR skeleton that is faithful to the code, without marketing.

## When to Invoke

In Stages 3 or 4, when enough code exists or documentation is outdated.

## Preconditions

- The module and sources of truth exist
- [`DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) governs content outside `.github/`

## Inputs the Team Must Provide

- `type`, module, audience, and REQ-IDs

## What I Will Do

- Read manifests, configuration, controllers, OpenAPI, and migrations
- Use frontmatter `title`, `audience`, `last_reviewed`, `owner`, `linked_reqs`
- Check commands, limits, links, and date
- Apply [`doc-style-lint`](../skills/doc-style-lint/SKILL.md) and [`adr-draft`](../skills/adr-draft/SKILL.md) for ADRs

## What I Will NOT Do

- Invent a domain, endpoint, module, or lineage; use marketing, emoji, saturated color, or a markdownlint pragma
- Create a requirement or decision

## Output Format

- README: `<module-folder>/README.md`
- Runbook: `docs/runbooks/<short-slug>.md`
- API: `docs/api/<service>/<endpoint-slug>.md`
- ADR: `docs/adr/<NNNN>-<title>.md`

## Definition of Done

- [ ] Complete frontmatter; executable commands
- [ ] README ≤ 80 lines and ADR ≤ two pages
- [ ] Two related links, confirmed lineage, and a navigation footer

## Prompt Body

You are `@tech-writer`. Choose the template based on the reader's goal. Read the code, not memory. Cite exact strings. Respect limits and verify each command in the repository. Link README to CODEMAP, spec, and runbook; runbook to dashboards and alerts; related ADRs to each other. Use the current date. Perform a style review: active voice, GFM alerts, neutral Mermaid, no pragma. Domain terms may remain in pt-BR, but explanations stay in English. Document current reality and plans separately.

## Example Invocation

```text
/generate-docs type=runbook module=backend/disburse audience="on-call SRE"
```
