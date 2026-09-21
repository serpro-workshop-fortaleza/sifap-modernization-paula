---
name: "azure-resource-health-diagnose"
description: "Diagnose Azure resource health using logs and telemetry and produce a remediation plan, delegating the workflow to the azure-resource-health-diagnose skill."
argument-hint: "resource=<name> rg=<resource-group>"
agent: "devops-engineer"
tools: ["read", "search", "execute", "Azure MCP Server/*"]
---
# /azure-resource-health-diagnose

## Objective

Assess the health of an Azure resource, diagnose problems using logs and telemetry, and produce a prioritized remediation plan. The complete workflow is in the [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 kit without repeating it.

> [!NOTE]
> Diagnose before changing: classify problems by severity and check any fix against Terraform in `infra/`.

## When to Invoke

During Stage 4 (Evolution), when a deployed Azure resource behaves unexpectedly and the team needs a structured diagnosis before acting.

## Preconditions

- The team is authenticated to Azure
- The resource is deployed and emitting logs or telemetry
- Diagnostic settings route logs to an accessible Log Analytics workspace
- The `Azure MCP Server/*` toolset is available; for a cloud coding agent, configure Azure MCP through the supported `azd coding-agent config` workflow

## Inputs the Team Must Provide

- `resource`: the resource name and, if known, its resource group and subscription
- The observed symptom and when it began
- Ask the user for any missing information.

## What I Will Do

- Follow the health assessment and log analysis workflow in the [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) skill
- Prioritize the kit's resource types: Azure Database for PostgreSQL 16 and containerized Spring Boot services
- Classify problems as Critical, High, Medium, or Low and record a confirmed cause, a bounded hypothesis with confidence, or `unknown`
- Produce a phased remediation plan with validation and rollback steps

## What I Will NOT Do

- Apply remediation before diagnosis and team confirmation
- Recommend a manual change that diverges from Terraform in `infra/`
- Ignore Managed Identity; I will flag resources that still use shared keys or connection strings
- Overstate certainty when logs are missing; I will record the limitation
- Fall back to an unobserved diagnosis when Azure tools or telemetry are unavailable; I will report the blocker

## Output Format

```markdown
### Health assessment — <resource> (<resource type>)
Status: <observed state> · Analyzed at: <timestamp>

### Problems
| Severity | Observed problem | Cause status | Evidence |
|---|---|---|---|
| <level> | <symptom> | confirmed / hypothesis / unknown | <metric, log, or trace> |

### Phased remediation
1. Immediate containment — <evidence-backed proposal and rollback>
2. Short term — <Terraform or application change requiring approval>
```

## Definition of Done

- [ ] The health state is stated with supporting metrics
- [ ] Problems are classified by severity, and each distinguishes confirmed cause, hypothesis, or unknown
- [ ] The remediation plan is phased, with validation and rollback
- [ ] Every fix is expressed in relation to Terraform in `infra/`

## Prompt Body

The [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) skill defines resource-specific diagnostics and KQL queries. Read it and apply it to the target resource.

**Step 1 — Identify.**
Locate the resource, its type, and its dependencies.

**Step 2 — Apply the skill.**
Run the health checks and log or telemetry queries according to the skill and identify failure patterns.

**Step 3 — Follow the kit's rules.**
Prioritize PostgreSQL 16 and Spring Boot services, flag authentication that does not use Managed Identity, and link fixes to Terraform in `infra/`.

**Step 4 — Plan.**
Classify the problems and produce the phased remediation plan. Wait for confirmation before acting.

## Example Invocation

```text
/azure-resource-health-diagnose resource=payment-db rg=sifap-prod-rg
```
