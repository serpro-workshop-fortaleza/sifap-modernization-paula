---
name: "az-cost-optimize"
description: "Analyze Azure resources and Terraform IaC to reduce costs and open tracking issues on GitHub, delegating the workflow to the az-cost-optimize skill."
argument-hint: "rg=<resource-group> repo=<owner/name>"
agent: "devops-engineer"
tools: ["read", "search", "execute", "Azure MCP Server/*", "github/*"]
---
# /az-cost-optimize

## Objective

Analyze deployed Azure resources and their Terraform IaC, produce evidence-based cost optimization recommendations, and open a GitHub issue for each opportunity plus a coordinating EPIC. The complete workflow is in the [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 kit without repeating it.

> [!IMPORTANT]
> The kit's IaC uses Terraform only. Treat the skill's Bicep/ARM references as out of scope and never open an issue about savings that are not supported by validated pricing.

## When to Invoke

During Stage 4 (Evolution), after the team provisions Azure resources and wants to track cost reductions as GitHub issues.

## Preconditions

- The team is authenticated to Azure and the target GitHub repository
- The `Azure MCP Server/*` and `github/*` toolsets are available; for a cloud coding agent, configure Azure MCP through the supported `azd coding-agent config` workflow
- Terraform for the modern system exists in `infra/` (created by the team in Stages 3 or 4)
- The target resource group and subscription are known

## Inputs the Team Must Provide

- `rg`: the target Azure resource group
- `repo`: the `owner/name` of the GitHub repository for the issues
- Ask the user for any missing information.

## What I Will Do

- Follow the discovery, metrics, and recommendations workflow in the [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) skill
- Read only Terraform in `infra/` as the IaC source of truth
- Validate each current and target cost against Azure pricing before recommending
- After explicit confirmation, search for duplicates and create one GitHub issue per optimization plus a coordinating epic with GitHub tools

## What I Will NOT Do

- Analyze Bicep or ARM templates, as they are outside this kit's scope
- Invent resources or savings when Terraform is missing; I will report the situation and stop
- Open issues before the team confirms the summary
- Recommend a change without validated evidence and consideration of rollback

## Output Format

```markdown
### Summary
Resources analyzed: <observed count>
Current estimate: <amount and currency/month>
Potential savings: <validated amount and currency/month>
Opportunities: <evidence-backed count>

### Issues to create
- [COST-OPT] <resource> — <validated amount and currency/month> (<evidence-backed risk>)
- [EPIC] Azure cost optimization — <validated amount and currency/month> potential savings
```

## Definition of Done

- [ ] All savings have been validated against the resource SKU/tier and Azure pricing
- [ ] Recommendations reference Terraform in `infra/`, not Bicep/ARM
- [ ] One issue per opportunity and an epic have been created with GitHub tools after confirmation, with returned URLs recorded
- [ ] Each issue contains evidence, risk, and validation steps

## Prompt Body

The [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) skill defines the discovery, metrics, scoring, and issue creation procedure. Read it and apply it to the target resource group.

**Step 1 — Discover.**
List the resources in `rg` and read Terraform in `infra/` as the intended configuration.

**Step 2 — Apply the skill.**
Collect usage metrics, validate current costs, and generate scored recommendations according to the skill.

**Step 3 — Follow the kit's rules.**
Ignore Bicep/ARM. If Terraform is missing, report it and stop. Keep GitHub as the source of truth.

**Step 4 — Confirm and create.**
Present the evidence-backed summary and wait for explicit approval. Use GitHub tools to identify the authenticated user and repository, search for duplicate open issues, list issue types for an organization repository, and create the approved issues and epic. Record returned URLs. If either toolset is unavailable, report the workflow as blocked; do not substitute unsupported estimates or claim issue creation.

## Example Invocation

```text
/az-cost-optimize rg=sifap-prod-rg repo=my-org/sifap-2
```
