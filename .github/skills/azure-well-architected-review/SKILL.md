---
name: "azure-well-architected-review"
description: "Use when the user requests an Azure Well-Architected Framework review, an architecture assessment, or an audit of an Azure workload's reliability, security, cost, performance, or operational excellence. Reviews the five WAF pillars against workload IaC (Terraform in this kit; Bicep/ARM can also be read) and deployed resources, and opens GitHub Issues for findings. Triggers include \"WAF review\", \"Well-Architected\", \"architecture assessment\", \"reliability audit\", and \"Azure security review\"."
---
# Azure Well-Architected review

This workflow performs a structured Azure Well-Architected Framework (WAF) review of a workload's IaC files and deployed infrastructure. It identifies risks across the five WAF pillars and creates GitHub Issues to track remediation.

> [!NOTE]
> This kit's IaC is **Terraform (`azurerm ~> 3.x`)**. The review reads any existing IaC (Terraform, Bicep, or ARM), but remediation examples are written in Terraform. Bicep/ARM snippets are illustrative only and out of scope for the kit's deliverables. This skill also depends on authentication with the **`az` CLI** and the **GitHub MCP server** (or `gh`).

## When to Invoke

- "Run a Well-Architected review of our Azure workload."
- "Audit this architecture for reliability and security risks."
- "Are we following Azure best practices across all five pillars?"
- "Open GitHub Issues for the WAF gaps in our infrastructure."

## Prerequisites

- Azure CLI (`az`) configured and authenticated.
- IaC files present in the repository (preferably Terraform; Bicep or ARM can also be read).
- GitHub MCP server (or `gh`) configured and authenticated.

## Workflow steps

### Step 1: Load the Well-Architected Framework reference

Consult current Azure WAF best practices:

- `https://learn.microsoft.com/en-us/azure/well-architected/`
- Guides for the Azure services in use (`https://learn.microsoft.com/en-us/azure/well-architected/service-guides/`)
- Specific guidance relevant to the workload type (SaaS, mission-critical, AI, and similar)

If the `microsoft.docs.mcp` MCP server is available, use it to query the latest pillar checklists and service-specific recommendations.

### Step 2: Discover IaC and architecture

Define the review scope and inventory the code and live environment:

1. **Confirm Azure scope**: ask which subscriptions and resource groups are in scope, or infer them from IaC parameters and confirm.
2. **Scan the repository for IaC files**:
   - Terraform: `**/*.tf` (azurerm/azapi providers), this kit's primary IaC
   - Bicep: `**/*.bicep`, `bicepconfig.json`
   - ARM templates: `**/azuredeploy*.json`, `**/*.template.json`, files whose `$schema` contains `deploymentTemplate`
3. **Always inventory live resources**, even when IaC exists: `az resource list --resource-group <rg> --output json` (or subscription-wide), plus targeted `az <service> show` calls for configuration details required by pillar checks.
4. **Compare IaC with the live inventory**: flag drift, such as resources present in Azure but absent from IaC (created through the portal), resources defined in IaC but not deployed, and configuration differences. Record drift findings for Step 3. They generally map to the Operational Excellence pillar.

Identify the main Azure services in use (compute, data, network, security, and observability) and generate a Mermaid architecture diagram.

### Step 3: Review by pillar

#### Pillar 1: Reliability

- [ ] Availability zones enabled for zonal services (VMs, VMSS, AKS node pools, App Service, SQL, Storage ZRS)
- [ ] Production SKUs support the required SLA (no Basic/Free tiers on critical paths)
- [ ] Azure SQL/Cosmos DB backup and point-in-time restore configured with appropriate retention
- [ ] Geo-redundancy configured where required by RPO (GRS/RA-GRS storage, SQL failover groups, multi-region Cosmos DB)
- [ ] Autoscale rules configured for App Service plans, VMSS, and AKS (no fixed single instance in production)
- [ ] Health probes configured on Load Balancer/Application Gateway/Front Door backends
- [ ] Dead-letter queues enabled on Service Bus queues/subscriptions and Event Grid subscriptions
- [ ] Retry policies with exponential backoff implemented to handle transient failures
- [ ] Disaster recovery plan defined (RTO/RPO documented and failover tested)

#### Pillar 2: Security

- [ ] Managed identities used instead of service principals with secrets or connection strings
- [ ] No credentials, keys, or connection strings hardcoded in IaC or code
- [ ] Secrets stored in Azure Key Vault with RBAC authorization (not access policies)
- [ ] Storage accounts deny public blob access and disable shared key access where possible
- [ ] Private endpoints (or at least service endpoints with firewall rules) for PaaS data services
- [ ] NSGs restrict inbound traffic to the minimum required ports/CIDRs (no `*` to `*` allow rules)
- [ ] TLS 1.2 or higher enforced on all endpoints (`minimumTlsVersion`, `httpsOnly`)
- [ ] Azure RBAC follows least privilege (no subscription-scoped Owner/Contributor for workload identities)
- [ ] Microsoft Defender for Cloud enabled for relevant resource types (`az security pricing list`)
- [ ] Azure WAF (Application Gateway or Front Door) configured for public web endpoints
- [ ] Diagnostic settings send security logs to Log Analytics/Microsoft Sentinel

#### Pillar 3: Cost Optimization

- [ ] Reservations or savings plans evaluated for steady-use compute (VMs, App Service, SQL)
- [ ] Storage lifecycle policies move blobs to cool/archive tiers
- [ ] SKUs sized according to actual utilization (no oversized VMs or App Service plans)
- [ ] Development/test environments use auto-shutdown schedules and Dev/Test pricing when eligible
- [ ] Azure Budgets and cost alerts configured (`az consumption budget list`)
- [ ] Unattached managed disks and orphaned public IPs identified and removed
- [ ] Consumption/serverless tiers used for spiky or low-volume workloads (Functions, Container Apps, SQL serverless)
- [ ] Log Analytics retention and data caps tuned to prevent excessive ingestion

#### Pillar 4: Operational Excellence

- [ ] All infrastructure defined as IaC (no manual portal changes; deny assignments or policies where feasible)
- [ ] Consistent tagging strategy applied to all resources (owner, environment, cost center)
- [ ] Azure Monitor alerts defined for key metrics and service health
- [ ] Automated deployment pipeline present (GitHub Actions/Azure Pipelines, no manual deployments)
- [ ] Azure Activity Log and resource diagnostic settings directed to Log Analytics
- [ ] Application Insights (or OpenTelemetry equivalent) instrumented for application workloads
- [ ] Azure Policy assignments enforce organizational standards (allowed locations, SKUs, and tags)
- [ ] Runbooks or operational documentation present

#### Pillar 5: Performance Efficiency

- [ ] Compute SKUs sized and validated against load requirements
- [ ] Caching implemented where beneficial (Azure Cache for Redis, CDN/Front Door caching)
- [ ] Azure Front Door or CDN used for global static content delivery
- [ ] Autoscaling based on load metrics, not fixed instance counts
- [ ] Appropriate database performance tier (DTU or vCore, elastic pools, Cosmos DB RU autoscale)
- [ ] Premium/zone-redundant storage used for latency-sensitive disk workloads
- [ ] Connection pooling and asynchronous patterns used in database and HTTP clients

### Step 4: Risk classification

Classify each finding:

| Risk | Meaning |
|---|---|
| High | Security vulnerability, single point of failure, missing backup/recovery |
| Medium | Suboptimal reliability, cost inefficiency, performance concern |
| Low | Best practice deviation, minor optimization opportunity |

### Step 5: User confirmation

Present the summary and require explicit approval before creating any GitHub Issues:

```text
Azure Well-Architected review summary

Review results:
- IaC files analyzed: X
- Azure services identified: Y
- Total findings: Z
  - High risk: A (requires immediate action)
  - Medium risk: B (should be addressed soon)
  - Low risk: C (nice-to-have improvement)

Top high-risk findings:
1. [Pillar]: [Finding] - [Why it matters]
2. [Pillar]: [Finding] - [Why it matters]

This will create Z individual GitHub Issues and 1 epic (EPIC).

Proceed with creating GitHub Issues? (y/n)
```

> [!IMPORTANT]
> Proceed to Steps 6 and 7 only if the user gives an explicit affirmative response (for example, "y" or "yes"). If the response is negative, ambiguous, or absent, **do not** create GitHub Issues. Display all findings as formatted Markdown in the console and stop.

### Step 6: Create individual finding issues

Use the `well-architected` label and the pillar name (for example, `security`, `reliability`).

Title: `[WAF-<PILLAR>] <Brief Finding> - <Risk Level>`

Body:

````markdown
## Well-Architected finding: <Brief Title>

**Pillar**: <Name> | **Risk level**: <High/Medium/Low> | **Effort**: <Low/Medium/High>

### Description
<Clear explanation of the finding and why it matters>

### Remediation

IaC remediation (preferred, Terraform, this kit's IaC):
```hcl
resource "azurerm_storage_account" "data" {
  name                            = "sifapdata"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "ZRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false

  tags = {
    project     = "sifap"
    environment = "prod"
    owner       = "platform-team"
  }
}
```

Azure CLI alternative:
```bash
az storage account update --name <name> --resource-group <rg> \
  --min-tls-version TLS1_2 --allow-blob-public-access false --https-only true
```

### Azure reference
- <WAF best-practice link>
- <Microsoft Learn documentation link>

### Validation
- [ ] Change implemented in Terraform and applied
- [ ] Azure Policy compliance passed (if applicable)
- [ ] Microsoft Defender for Cloud recommendation resolved (if applicable)

**Well-Architected recommendation**: <WAF checklist item this maps to>
````

### Step 7: Create the tracking EPIC issue

Use the `well-architected` and `epic` labels.

Title: `[EPIC] Azure Well-Architected review - X findings across 5 pillars`

Body: an executive summary with a table by pillar (finding counts by pillar and risk level), a Mermaid architecture diagram, a prioritized checklist linking all individual issues (High, Medium, and Low), and success criteria:

- All High-risk findings resolved
- Medium-risk findings have accepted mitigation plans
- No regression in existing Azure Monitor alerts or Azure Policy compliance

## Error handling

| Situation | Action |
|---|---|
| No IaC files found | Limit the review to live resource discovery through `az resource list` and record the gap |
| Insufficient Azure permissions | List required read-only roles (Reader, Security Reader) |
| GitHub creation failure | Display all findings as formatted Markdown in the console |

## Output Template

When issue creation is skipped (or in the console summary), deliver findings in a table grouped by pillar:

```markdown
## Well-Architected review: <workload>

| Pillar | Finding | Risk | Remediation |
|---|---|---|---|
| Security | Storage allows public blob access | High | Set allow_nested_items_to_be_public = false |
| Reliability | App Service runs a single instance | Medium | Enable autoscaling, with a minimum of 2 instances |
| Cost | Log Analytics has no data cap | Low | Set a daily cap and a retention policy |

Totals: 1 High, 1 Medium, and 1 Low across the 5 pillars.
Conclusion: address the High-risk security finding before the next release.
```

## Quality Gate

- [ ] All five WAF pillars were reviewed against IaC and live infrastructure.
- [ ] Each finding is classified by risk level and mapped to a pillar.
- [ ] Each finding has actionable Terraform remediation (Bicep/ARM for illustration only).
- [ ] Drift between IaC and deployed resources was recorded as Operational Excellence findings.
- [ ] GitHub Issues were created only after explicit user approval. Otherwise, findings were displayed in the console.
- [ ] A Mermaid architecture diagram and Microsoft Learn references are included.
