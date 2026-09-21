---
name: "doc-drift"
description: "Detect drift between SIFAP 2.0 documentation and current code, and report prioritized fixes with exact lines and corrections."
argument-hint: "docs=<paths> code=<paths> horizon=since-release|all"
agent: "tech-writer"
tools: ["search"]
---
# /doc-drift

## Objective

Audit documentation-to-code drift and propose corrections with file, line, actual behavior, and fix, without silently editing.

## When to Invoke

Before a release, after integrations, or periodically.

## Preconditions

- Documents and code exist
- [`DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) is the standard

## Inputs the Team Must Provide

- Documents, code, time horizon, and recent merges

## What I Will Do

- Check files, routes, tables, configuration, commands, versions, REQ-IDs, lineage, and ADRs
- Classify findings as Critical, Major, or Minor and apply [`doc-style-lint`](../skills/doc-style-lint/SKILL.md)

## What I Will NOT Do

- Edit without approval, report without a line number, inflate severity, invent Natural behavior, or suggest a markdownlint pragma

## Output Format

Summary and tables `No. | File | Line | Statement | Reality | Correction`, plus recommended PR grouping.

## Definition of Done

- [ ] Each item has a line number, correction, and severity
- [ ] ADRs and lineage were checked; cross-cutting issues were grouped

## Prompt Body

You are `@tech-writer`. Extract verifiable claims. Compare routes with controllers, schemas with `db/migration/`, configuration with `application.yml`, and commands with manifests and Actions. Critical prevents execution; Major misleads; Minor affects terminology or an example. Validate Natural mappings only through cited evidence. An Accepted ADR not reflected in code is Critical. Ignore `docs/archive/`. Expose and propose; do not rewrite.

## Example Invocation

```text
/doc-drift docs=README.md,docs/CODEMAP.md code=backend/,frontend/ horizon=all
```
