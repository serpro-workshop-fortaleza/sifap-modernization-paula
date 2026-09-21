---
name: "codemap"
description: "Produce a navigable service-level code map for a SIFAP 2.0 module: components, direct dependencies, REQ-ID coverage, legacy lineage, and integration points."
argument-hint: "service=<name> path=<root created by the team> spec=specs/<NNN>-<feature>/spec.md"
agent: "software-architect"
tools: ["read", "search", "edit"]
---
# /codemap

## Objective

Produce `docs/codemap-<service>.md` to locate components, direct dependencies, REQ-IDs, and lineage within ten minutes.

## When to Invoke

After the team creates a service and whenever its structure changes.

## Preconditions

- The service and `spec.md` exist
- [`modular-monolith.instructions.md`](../instructions/modular-monolith.instructions.md) governs dependencies

## Inputs the Team Must Provide

- Service, root, specification, whether to include tests, and previous map

## What I Will Do

- Group Java by `controller`, `service`, `domain`, `repository`, `infrastructure`, `config`; TypeScript by `app/`, `components/`, `lib/`, `server/`
- Record confirmed purpose, direct dependencies, `@implements REQ-NNN`, state, API, tests, and confirmed lineage
- Generate Mermaid and a searchable table; flag wrong direction, more than five outgoing dependencies, and code without incoming dependencies

## What I Will NOT Do

- Generate automatically from imports, list transitive dependencies, or invent REQ-IDs, endpoints, responsibilities, or Natural facts
- Decide contexts; use `/impl-plan` or [`adr-draft`](../skills/adr-draft/SKILL.md)

## Output Format

A document with a diagram, a `Type | FQN | Purpose | REQ-IDs | Incoming | Outgoing` table, API, state, lineage, and observed issues.

## Definition of Done

- [ ] Mermaid reflects actual components; the table covers the service
- [ ] Missing REQ-IDs are explicit; dependencies are direct
- [ ] Lineage has evidence and the document is linked to `docs/CODEMAP.md`

## Prompt Body

You are `@software-architect`. Confirm the scope and previous map. List components by layer and verified purpose. Map direct calls and stable contracts. Locate `@implements REQ-NNN` without inventing gaps. Record only confirmed Natural origins; use "unmapped" for the rest. Flag layer violations, god classes, and code without incoming dependencies. Write Mermaid and tables and link to `docs/CODEMAP.md`.

## Example Invocation

```text
/codemap service=registration path=backend/src/main/java/app/registration spec=specs/014-registration/spec.md
```
