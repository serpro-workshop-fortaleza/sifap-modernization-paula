---
name: "azure-architecture-autopilot"
description: "Use when the user wants to design Azure infrastructure in natural language or analyze an existing Azure environment as an interactive architecture diagram, iterate, and optionally deploy. Guides a design, diagram, review, and deployment workflow with a built-in offline diagram engine (more than 605 Azure icons). Triggers include \"create X on Azure\", \"design a RAG architecture\", \"analyze my Azure resources\", and \"draw a diagram for rg-...\". Generates Bicep, which is out of scope for this kit; convert any adopted design to Terraform."
---
# Azure architecture autopilot

A pipeline that designs Azure infrastructure from natural language or analyzes existing resources. It presents the architecture as an interactive diagram and supports iteration through modifications and deployment.

> [!WARNING]
> This kit's infrastructure as code (IaC) uses **Terraform (Azure provider `~> 3.x`)**. This skill generates **Bicep**, which is **out of scope** for the kit's deliverables. Use it only for exploration, diagrams, and reference. Convert any adopted architecture to Terraform in `infra/` (created by the team in Stage 3), with the required `project`, `environment`, and `owner` tags.

> [!NOTE]
> This skill depends on a built-in Python diagram engine (`scripts/`, no installation needed). Deployment phases also require the `az` command-line interface (CLI) and Bicep tools. Microsoft Docs fact-checking uses the `web_fetch` and `web_search` tools directly in the main agent.

## When to Invoke

- "Create a RAG architecture on Azure."
- "Analyze my current Azure infrastructure and draw a diagram for rg-sifap."
- "Foundry is slow. How should I change this architecture?"
- "I want to reduce the cost or strengthen the security of this design."

## Built-in diagram engine

The diagram engine is bundled with the skill in `scripts/`. No `pip install` is needed. The included Python scripts render interactive HTML diagrams with more than 605 official Azure icons, fully offline. The entry point is [scripts/cli.py](scripts/cli.py), which imports [scripts/generator.py](scripts/generator.py) to render HTML/SVG and [scripts/icons.py](scripts/icons.py) for icon data.

## User-facing content language

Detect the language of the first message and present all user-facing content in that language, including questions, progress updates, reports, and Bicep comments. Adapt the examples; do not copy them literally.

## Tool usage

| Need | Tool | Notes |
|---|---|---|
| Fetch URL content | `web_fetch` | Microsoft Docs lookups |
| Search the web | `web_search` | URL discovery |
| Ask the user | `ask_user` | `choices` must be an array of strings |
| Subagents | `task` | explore / task / general-purpose |
| Run in the shell | shell tool | Discover `az` / `python` / `bicep` paths first |

> [!NOTE]
> Subagents cannot use `web_fetch` or `web_search`. Fact-check Microsoft Docs directly through the main agent.

## Path discovery

`az`, `python`, and `bicep` are often not on `PATH`. Discover each path once before a phase and cache the result. Do not repeat discovery on every call. Prefer direct filesystem discovery over shell aliases. See the diagram generation section in [references/phase1-advisor.md](references/phase1-advisor.md) for the Python path and integration with the bundled engine.

## Progress updates

Report progress with short status lines in the user's language, without emojis. Use one line per action:

```text
Action: reason
Completed: result
Warning: detail to watch
Failed: cause and next step
```

## Flow

There are two paths, selected automatically based on the request. If ambiguous, ask which one the user wants to follow.

### Path A: New design

Trigger phrases: "create", "configure", "deploy", "build".

```text
Phase 1 (references/phase1-advisor.md)    Interactive design + diagram
  -> Phase 2 (references/bicep-generator.md)  Bicep generation (out of scope for the kit)
  -> Phase 3 (references/bicep-reviewer.md)    Review + build check
  -> Phase 4 (references/phase4-deployer.md)    validation -> change analysis (what-if) -> deployment
```

### Path B: Analyze and modify

Trigger phrases: "analyze", "current resources", "inspect", "draw a diagram".

```text
Phase 0 (references/phase0-scanner.md)    Existing resource scan + diagram
  -> Modification discussion (natural-language change request)
  -> Phase 1 (references/phase1-advisor.md)   Change confirmation + diagram update
  -> Phases 2 through 4, as in Path A
```

## Phase transition rules

- Each phase follows the instructions in its respective `references/*.md` file.
- At every transition, always state the next step.
- Do not skip phases. In particular, never skip change analysis (`what-if`) between Phases 3 and 4.
- Transitioning from Phase 1 to Phase 2 requires `01_arch_diagram_draft.html` to have been generated and presented to the user. Never generate Bicep without a confirmed diagram.
- A modification after deployment returns to Phase 1, not Phase 0.

## Service coverage

Optimized services: Microsoft Foundry, Azure OpenAI, AI Search, ADLS Gen2, Key Vault, Microsoft Fabric, Azure Data Factory, VNet / Private Endpoint, and AML / AI Hub. All other Azure services receive the same quality standard through Microsoft Docs lookups.

| Category | Handling | Examples |
|---|---|---|
| Stable | Consult reference files first | `isHnsEnabled`, Private Endpoint trios |
| Dynamic | Always consult Microsoft Docs | API version, model availability, SKU, region |

## Reference files

| File | Purpose |
|---|---|
| [references/phase0-scanner.md](references/phase0-scanner.md) | Existing resource scan, relationship inference, and diagram |
| [references/phase1-advisor.md](references/phase1-advisor.md) | Interactive design and fact-checking |
| [references/bicep-generator.md](references/bicep-generator.md) | Bicep generation rules (out of scope for the kit) |
| [references/bicep-reviewer.md](references/bicep-reviewer.md) | Code review checklist |
| [references/phase4-deployer.md](references/phase4-deployer.md) | validation -> change analysis (`what-if`) -> deployment |
| [references/service-gotchas.md](references/service-gotchas.md) | Required properties and Private Endpoint mappings |
| [references/azure-dynamic-sources.md](references/azure-dynamic-sources.md) | Microsoft Docs URL registry |
| [references/azure-common-patterns.md](references/azure-common-patterns.md) | Private Endpoint, security, and naming patterns |
| [references/architecture-guidance-sources.md](references/architecture-guidance-sources.md) | Architecture guidance sources |
| [references/ai-data.md](references/ai-data.md) | AI and data services guide |

Output examples: [architecture diagram](assets/06-architecture-diagram.png), [resources in the Azure portal](assets/07-azure-portal-resources.png), and [successful deployment](assets/08-deployment-succeeded.png).

## Output Template

The skill produces an interactive HTML diagram and a design summary. Record the adopted design so it can be converted to Terraform:

```text
Architecture: <name>
Path: A (new design) | B (analyze + modify)
Diagram: 01_arch_diagram_draft.html (generated, presented, and confirmed)
Services: Foundry, AI Search, ADLS Gen2, Key Vault (Private Endpoints)
Bicep: generated for reference only (out of scope for the kit)
Kit follow-up: convert to Terraform in infra/ with project/environment/owner tags
```

## Quality Gate

- [ ] The path (A, new design; B, analyze and modify) was selected or confirmed.
- [ ] A diagram (`01_arch_diagram_draft.html`) was generated with the built-in engine and presented before any Bicep.
- [ ] Phases ran in order, without skipping change analysis (`what-if`) between review and deployment.
- [ ] Dynamic facts (API version, SKU, region, and model availability) were confirmed in Microsoft Docs.
- [ ] Presented content used the user's language, and the primitive itself contains no emojis.
- [ ] Any adopted architecture was flagged for conversion to Terraform in `infra/`, because Bicep is out of scope for the kit.
