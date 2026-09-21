# Agent Index

This directory contains the immersion's custom GitHub Copilot agents: **17** in total, each in its own `<name>.agent.md`.

> [!NOTE]
> Copilot discovers `*.agent.md` files in `.github/agents/`. Invoke an agent by its `name` with `@<name>` (for example, `@archaeologist`). The `name` also binds prompts: a `*.prompt.md` file selects its agent through the frontmatter `agent:` key. The agent ID is therefore a contract, not a label.

The kit uses **two agent layers**. This is the central mental model, so agents are grouped by layer instead of appearing in a flat list:

- **Stage agents (4)**: one per immersion stage, used sequentially throughout the day.
- **Persona agents (10)**: one per team role, used by the pair responsible for that role.

Three additional **specialist agents** sit outside these two layers. They provide deeper expertise for specific work and appear at the end.

## Stage Agents

Four sequential agents, one per immersion stage. They are chained through the frontmatter `handoffs:` key: `archaeologist -> architect -> builder` pass work to the next agent; the terminal Stage 4 agent (`evolution`) has no handoff.

| Stage | Agent | Invocation | Linked prompts | Description |
| --- | --- | --- | --- | --- |
| Stage 1 | [`archaeologist`](archaeologist.agent.md) | `@archaeologist` | 5 | Stage 1 agent: reads legacy Natural/Adabas code, extracts business rules, maps dependencies, and records open questions |
| Stage 2 | [`architect`](architect.agent.md) | `@architect` | 4 | Stage 2 agent: defines bounded contexts, writes EARS specifications, generates ADRs, and designs a Modular Monolith architecture |
| Stage 3 | [`builder`](builder.agent.md) | `@builder` | 5 | Stage 3 agent: translates Natural to Java, generates JPA from FDTs, writes equivalence tests, and builds REST + Next.js |
| Stage 4 | [`evolution`](evolution.agent.md) | `@evolution` | 4 | Stage 4 agent: writes GitHub Issues for Copilot Agent, reviews AI-generated PRs, and configures CI/CD and IaC |

## Persona Agents

Ten agents, one per team role. The [`implementer`](implementer.agent.md) agent serves the Developer persona. Its prompts are therefore named `persona-developer-*`, but bind to `agent: "implementer"`.

| Agent | Invocation | Linked prompts | Description |
| --- | --- | --- | --- |
| [`product-owner`](product-owner.agent.md) | `@product-owner` | 3 | Product Owner assistant for specification writing, backlog refinement, and acceptance validation with EARS notation and the SDD workflow |
| [`requirements-engineer`](requirements-engineer.agent.md) | `@requirements-engineer` | 4 | Requirements Engineer assistant for EARS notation, specification validation, and legacy-traceable requirements in the SDD workflow |
| [`enterprise-architect`](enterprise-architect.agent.md) | `@enterprise-architect` | 3 | Enterprise architecture assistant for the Spec-Kit constitution, ADRs, external integration mapping, and cross-cutting design |
| [`software-architect`](software-architect.agent.md) | `@software-architect` | 3 | Software architecture assistant for CODEMAP, bounded contexts, module topology, and API contracts |
| [`tech-lead`](tech-lead.agent.md) | `@tech-lead` | 3 | Technical leadership assistant for CODEMAP and context curation, Copilot guidance, and code-review standards |
| [`implementer`](implementer.agent.md) | `@implementer` | 6 | Developer assistant for Java 21 and Next.js 15: TDD, bug fixes, and refactoring with REQ-ID traceability |
| [`dba`](dba.agent.md) | `@dba` | 4 | Database assistant for PostgreSQL migrations, query optimization, indexing strategy, and SQL injection auditing |
| [`qa-engineer`](qa-engineer.agent.md) | `@qa-engineer` | 5 | Quality assurance assistant for specification-based test generation, coverage-gap analysis, and CI quality gates |
| [`devops-engineer`](devops-engineer.agent.md) | `@devops-engineer` | 5 | DevOps Engineer assistant for GitHub Actions pipelines, Terraform IaC, container builds, observability, and incident analysis |
| [`tech-writer`](tech-writer.agent.md) | `@tech-writer` | 5 | Tech Writer assistant for API documentation, runbooks, ADRs, CODEMAP, and Diataxis-style content with drift detection |

## Specialist Agents

Three specialists outside the stage and persona layers. None has prompts; invoke them directly with `@<name>`.

| Agent | Invocation | Linked prompts | Description |
| --- | --- | --- | --- |
| [`se-ux-ui-designer`](se-ux-ui-designer.agent.md) | `@se-ux-ui-designer` | 0 | UX/UI research specialist for the modern SIFAP UI: Jobs-to-be-Done (needs to address), user journeys, and accessibility specifications that guide frontend development. Use for research and design intent; use @expert-react-frontend-engineer or @implementer to write Next.js code. |
| [`expert-react-frontend-engineer`](expert-react-frontend-engineer.agent.md) | `@expert-react-frontend-engineer` | 0 | Deep frontend specialist for the SIFAP UI: React 19 + Next.js 15 App Router, Server/Client boundaries, Server Actions, optimistic UI, accessibility, and performance. Use for frontend-focused work; use @implementer for a single traceable tasks.md item or any backend change. |
| [`java-mcp-expert`](java-mcp-expert.agent.md) | `@java-mcp-expert` | 0 | Greenfield specialist for building Model Context Protocol (MCP) servers in Java with the official MCP Java SDK, Project Reactor, and Spring Boot 3.3. Use when the team extends the toolchain with a custom MCP server; SIFAP legacy-to-Java modernization belongs to @archaeologist, @architect, and @builder. |

## Prompt Ownership

The 59 prompts in [`../prompts/`](../prompts/) bind to an agent through their `agent:` key:

- All **59** bind to one of the **14** named agents above (stage + persona); no prompt remains on the generic built-in `agent: "agent"`. Per-agent counts appear in the tables' **Linked prompts** columns.
- The three specialist agents (`se-ux-ui-designer`, `expert-react-frontend-engineer`, `java-mcp-expert`) have **0** prompts and are invoked directly.

Recalculate the counts with `grep -h '^agent:' ../prompts/*.prompt.md | sort | uniq -c`.

## Maintenance Rules

- Renaming an agent silently breaks **every** prompt bound to it through `agent:`. Rename the agent and all prompt bindings together and rerun the validator.
- `description` is the only frontmatter key strictly required by the gate; `handoffs` is for stage agents only and only when a next stage exists.
- The required body sections (`Mission`, `Leading Personas`, `Operating Principles`, `What This Agent Knows`, `What This Agent Does NOT Know`, `Available Prompts`, a `Definition of Done` heading, `Anti-Patterns This Agent Rejects`), the recommended `SDD Workflow` section, and the complete schema are defined in [`../PRIMITIVE-STANDARD.md`](../PRIMITIVE-STANDARD.md); required structure is enforced by [`../scripts/validate-copilot-primitives.py`](../scripts/validate-copilot-primitives.py).
- When adding an agent, include its row in the correct layer above. If a prompt needs to invoke it, set the prompt's `agent:` to this `name`.
