---
name: "architecture-review"
description: "Review plan.md against the Azure Well-Architected pillars and produce prioritized, evidence-based findings."
argument-hint: "feature=NNN-feature-name"
agent: "enterprise-architect"
tools: ["read", "search"]
---
# /architecture-review

## Objective

Review `specs/<NNN>-<feature>/plan.md` (or a proposed architectural change) against the five Microsoft Azure Well-Architected pillars: Reliability, Security, Cost Optimization, Operational Excellence, and Performance Efficiency. Produce a scorecard and a list of findings prioritized by severity. Each finding cites a specific artifact and proposes a concrete, plan-specific fix.

## When to Invoke

When `plan.md` exists and before implementation begins, or whenever an architectural change is proposed.

## Preconditions

- `specs/<NNN>-<feature>/plan.md` exists or a proposed change has been provided
- Relevant ADRs and `.specify/memory/constitution.md` are accessible

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`: the `plan.md` to review
- All relevant ADRs
- Ask the user for any missing information

## What I Will Do

- Load `plan.md` and all relevant ADRs
- Score each pillar (Reliability, Security, Cost Optimization, Operational Excellence, and Performance Efficiency) from 1 to 5 based on concrete evidence
- Classify each finding as Critical (blocks production launch), High (fix before general availability), or Low (backlog)
- Link each finding to a specific diagram, ADR, or paragraph
- Propose a concrete fix with an effort estimate (S/M/L)
- Offer three options for the most critical finding
- Compare the design with the constitution, for example, Azure-only and Managed Identity

## What I Will NOT Do

- Skip a pillar. All five receive a score
- Offer generic best-practice recommendations. Each fix is specific to this plan
- Edit `plan.md` or ADRs. This review is read-only
- Invent an architecture the plan does not describe. I cite what is written or consult the team
- Decide the trade-off for the team. I propose options; the choice is recorded through `/create-adr`

## Output Format

A report presented to the team:

```markdown
## Architecture review: 001-pagamento-beneficio

| Pillar | Score (1-5) | Top finding | Fix |
|---|---|---|---|
| Reliability | 3 | No retry policy in the batch writer | Idempotent retries with backoff (M) |
| Security | 2 | Client secret in application configuration (violates C4) | Switch to Azure Managed Identity (M) |
| Cost Optimization | 4 | Oversized development database | Right-size to an appropriate Burstable tier (S) |
| Operational Excellence | 3 | No runbook for batch failure | Add a runbook and alerts (S) |
| Performance Efficiency | 3 | Full table scan on lookups | Add an index; paginate results (M) |

### Findings by severity
- **Critical**: Security: client secret in configuration (violates constitution C4). Fix: Managed Identity (M).
- **High**: Reliability: no retry policy in the batch writer. Fix: idempotent retries (M).
- **Low**: Cost Optimization: oversized development database. Fix: Burstable tier (S).

### Options for the top finding (client secret)
1. Managed Identity with Azure Key Vault references (preferred).
2. Azure Key Vault with a rotated, short-lived secret.
3. Workload identity federation.
```

## Definition of Done

- [ ] All five pillars receive an evidence-based score; none is skipped
- [ ] Each finding cites a specific artifact (diagram, ADR, or paragraph)
- [ ] Each finding is Critical, High, or Low and includes a specific fix and S/M/L effort
- [ ] There is at least one cost optimization finding or the area is marked "already optimized"
- [ ] Three options are presented for the most critical finding
- [ ] Conflicts with the constitution, for example, Azure-only and Managed Identity, are flagged
- [ ] No `plan.md` or ADR file has been modified

## Prompt Body

You are `@enterprise-architect`, reviewing a design before changing it becomes costly.

**Step 1: load the inputs.**
Read `plan.md` and all relevant ADRs.

**Step 2: score each pillar based on evidence.**

- **Reliability**: service-level objectives (SLOs), redundancy, failure modes, and retry policies.
- **Security**: identity, network, data, secrets, and threat model.
- **Cost Optimization**: right-sizing, reserved capacity, and idle resources.
- **Operational Excellence**: infrastructure as code (IaC), observability, and runbooks.
- **Performance Efficiency**: scalability, caching, and data access patterns.

**Step 3: classify and substantiate findings.**
Use Critical (blocks production launch), High (fix before general availability), or Low (backlog). Link each finding to a specific diagram, ADR, or paragraph.

**Step 4: propose fixes.**
Each fix must be specific to this plan and include an S/M/L effort estimate.

**Step 5: offer options for the top finding.**
Present three concrete alternatives for the most critical finding.

**Step 6: check the constitution.**
Flag any design choice that violates a constitutional rule, for example, Azure-only or Managed Identity.

Keep the review read-only and cite the artifact supporting each finding. Fixes must be specific to this plan, and the team decides the trade-off. Record it through `/create-adr`.

## Example Invocation

```text
/architecture-review feature=001-pagamento-beneficio
```
