# Azure dynamic sources registry

This file manages **only the sources (URLs) of frequently changing information**.
Actual values (API version, SKU, region, etc.) are not recorded here.
Always consult the URLs below to verify the latest information before generating Bicep.

---

## 1. Bicep API version (required lookup)

Microsoft Docs Bicep reference by service. Check the latest stable `apiVersion` at these URLs before using it.

| Service | Microsoft Docs URL |
|---------|-------------|
| CognitiveServices (Foundry/OpenAI) | https://learn.microsoft.com/en-us/azure/templates/microsoft.cognitiveservices/accounts |
| AI Search | https://learn.microsoft.com/en-us/azure/templates/microsoft.search/searchservices |
| Storage Account | https://learn.microsoft.com/en-us/azure/templates/microsoft.storage/storageaccounts |
| Key Vault | https://learn.microsoft.com/en-us/azure/templates/microsoft.keyvault/vaults |
| Virtual Network | https://learn.microsoft.com/en-us/azure/templates/microsoft.network/virtualnetworks |
| Private Endpoints | https://learn.microsoft.com/en-us/azure/templates/microsoft.network/privateendpoints |
| Private DNS Zones | https://learn.microsoft.com/en-us/azure/templates/microsoft.network/privatednszones |
| Fabric | https://learn.microsoft.com/en-us/azure/templates/microsoft.fabric/capacities |
| Data Factory | https://learn.microsoft.com/en-us/azure/templates/microsoft.datafactory/factories |
| Application Insights | https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/components |
| ML Workspace (Hub) | https://learn.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces |

> **Always check child resources too**: resources such as `accounts/projects`, `accounts/deployments`, and `privateDnsZones/virtualNetworkLinks` may have different API versions from the parent resource. Follow child resource links on the parent resource page to verify.

### Services missing from the table

The table includes only services in the v1 scope. For other services, construct and query the URL in this format:

```text
https://learn.microsoft.com/en-us/azure/templates/microsoft.{provider}/{resourceType}
```

---

## 2. Model availability (required when using Foundry/OpenAI models)

Check whether the model can be deployed in the target region. Do not rely on static knowledge.

| Verification method | URL / command |
|--------------------|---------------|
| Model availability in Microsoft Docs | https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models |
| Azure command-line interface (CLI), for existing resources | `az cognitiveservices account list-models --name "<NAME>" --resource-group "<RG>" -o table` |

> If the model is unavailable in the target region -> inform the user and suggest available alternative regions or models. Do not substitute without approval.

---

## 3. Private Endpoint mapping when adding new services

Azure may change PE `groupId` and DNS Zone mappings. When adding new services or when verification is needed:

| Verification method | URL |
|--------------------|-----|
| Official PE DNS integration documentation | https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns |

> Core service mappings in `service-gotchas.md` are stable, but always reconfirm at the URL above when adding new services.

---

## 4. Regional service availability

Check whether a specific service is available in a given region:

| Verification method | URL |
|--------------------|-----|
| Azure service availability by region | https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/ |

---

## 5. Azure Updates (secondary source)

The sources below are **for reference only**. The primary source is always official Microsoft Docs documentation.

| Source | URL | Purpose |
|--------|-----|---------|
| Azure Updates | https://azure.microsoft.com/en-us/updates/ | Track service changes |
| What's new in Azure | Official What's New pages for each service in Microsoft Docs | Check feature changes |

---

## Decision rule: when to look up?

| Information type | Lookup required? | Reason |
|-----------------|-------------|-----------|
| API version | **Always** | Changes frequently; incorrect values cause deployment failure |
| Model availability (name, region) | **Always** | Varies by region and changes frequently |
| SKU list | **Always** | May change by service |
| Regional availability | **Always** | Each service's regional support changes frequently. Always check whether the service is available in the specified region |
| PE `groupId` and DNS Zone | May consult `service-gotchas.md` for core v1 services; **must look up new services or complex configurations (Monitor, etc.)** | Core mappings are stable, but new or complex services introduce risks |
| Required property patterns | Consult reference files first | Nearly immutable (`isHnsEnabled`, etc.) |
