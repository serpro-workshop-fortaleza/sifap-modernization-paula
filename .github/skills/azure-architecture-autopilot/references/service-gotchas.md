# Service gotchas (stable)

Per-service summary of **non-obvious required properties**, **common errors**, and **PE mappings**.
Only nearly immutable patterns appear here. Dynamic values, such as API version, SKU lists, and region, are not included.

---

## 1. Required properties (omission causes deployment failure or functional issues)

| Service | Required property | Result of omission | Notes |
|---------|------------------|-------------------|-------|
| ADLS Gen2 | `isHnsEnabled: true` | Becomes regular Blob Storage. Not reversible | Requires `kind: 'StorageV2'` |
| Storage Account | Name without special characters or hyphens | Deployment fails | Lowercase letters and numbers only, 3 to 24 characters |
| Foundry (AIServices) | `customSubDomainName: foundryName` | Cannot create the Project or change after creation -> delete and recreate the resource | Globally unique value |
| Foundry (AIServices) | `allowProjectManagement: true` | Cannot create the Foundry Project | `kind: 'AIServices'` |
| Foundry (AIServices) | `identity: { type: 'SystemAssigned' }` | Project creation fails | |
| Foundry Project | Must be created together with the Foundry resource | Cannot be used through the portal | `accounts/projects` |
| Key Vault | `enableRbacAuthorization: true` | Risk of mixed Access Policy usage | |
| Key Vault | `enablePurgeProtection: true` | Required in production | |
| Fabric Capacity | `administration.members` required | Deployment fails | Administrator email |
| PE subnet | `privateEndpointNetworkPolicies: 'Disabled'` | PE deployment fails | |
| PE DNS Zone | `registrationEnabled: false` (VNet Link) | Possible DNS conflict | |
| PE configuration | Three-component set (PE + DNS Zone + VNet Link + Zone Group) | DNS resolution fails even with the PE present | |

---

## 2. Private Endpoint (PE) `groupId` and DNS Zone mapping (core services)

The mappings below are stable, but reconfirm them in the PE DNS integration document listed in `azure-dynamic-sources.md` when adding new services.

| Service | groupId | Private DNS Zone |
|---------|---------|-----------------|
| Azure OpenAI / CognitiveServices | `account` | `privatelink.cognitiveservices.azure.com` |
| (additional for Foundry/AIServices) | `account` | `privatelink.openai.azure.com` - **Both zones must be in the DNS Zone Group. Without this zone, OpenAI API DNS resolution fails** |
| Azure AI Search | `searchService` | `privatelink.search.windows.net` |
| Storage (Blob/ADLS) | `blob` | `privatelink.blob.core.windows.net` |
| Storage (DFS/ADLS Gen2) | `dfs` | `privatelink.dfs.core.windows.net` |
| Key Vault | `vault` | `privatelink.vaultcore.azure.net` |
| Azure ML / AI Hub | `amlworkspace` | `privatelink.api.azureml.ms` |
| Container Registry | `registry` | `privatelink.azurecr.io` |
| Cosmos DB (SQL) | `Sql` | `privatelink.documents.azure.com` |
| Azure Cache for Redis | `redisCache` | `privatelink.redis.cache.windows.net` |
| Data Factory | `dataFactory` | `privatelink.datafactory.azure.net` |
| API Management | `Gateway` | `privatelink.azure-api.net` |
| Event Hub | `namespace` | `privatelink.servicebus.windows.net` |
| Service Bus | `namespace` | `privatelink.servicebus.windows.net` |
| Monitor (AMPLS) | Complex configuration, see below | Requires multiple DNS Zones, see below |

> **ADLS Gen2 note**: when `isHnsEnabled: true`, **both `blob` and `dfs` PEs are required**.
>
> - With only the `blob` PE, the Blob API works, but Data Lake operations such as filesystem creation, directory manipulation, and the `abfss://` protocol fail.
> - DFS PE: `groupId` `dfs`, DNS Zone `privatelink.dfs.core.windows.net`
>
> **Azure Monitor Private Link (AMPLS) note**: Azure Monitor cannot be configured with a single PE and a single DNS Zone. It connects through Azure Monitor Private Link Scope (AMPLS), and **all five DNS Zones** are required:
>
> - `privatelink.monitor.azure.com`
> - `privatelink.oms.opinsights.azure.com`
> - `privatelink.ods.opinsights.azure.com`
> - `privatelink.agentsvc.azure-automation.net`
> - `privatelink.blob.core.windows.net` (for Log Analytics data ingestion)
>
> This mapping is complex and may change. Always consult and confirm Microsoft Docs when configuring a Monitor PE:
> https://learn.microsoft.com/en-us/azure/azure-monitor/logs/private-link-configure

---

## 3. Common error checklist

| Item | Incorrect example | Correct example |
|------|---------------------|-------------------|
| ADLS Gen2 HNS | `isHnsEnabled` missing or `false` | `isHnsEnabled: true` |
| PE subnet | Policy not configured | `privateEndpointNetworkPolicies: 'Disabled'` |
| DNS Zone Group | Only the PE was created | PE + DNS Zone + VNet Link + DNS Zone Group |
| Foundry resource | `kind: 'OpenAI'` | `kind: 'AIServices'` + `allowProjectManagement: true` |
| Foundry resource | `customSubDomainName` missing | `customSubDomainName: foundryName`, cannot be changed after creation |
| Foundry Project | Only Foundry exists, no Project | Must be created together |
| Key Vault authentication | Access Policy | `enableRbacAuthorization: true` |
| Public network | Not configured | `publicNetworkAccess: 'Disabled'` |
| Storage name | `st-my-storage` | `stmystorage` or `st${uniqueString(...)}` |
| API version | Copied from a previous conversation or error | Check the latest stable version in Microsoft Docs |
| Region | Fixed value (`'eastus'`) | Pass as a parameter (`param location`) |
| Sensitive values | Plaintext in `.bicepparam` | `@secure()` + Key Vault reference |

---

## 4. Decision rules for service relationships

These are **default selection rules**, not absolute mandates.

### Foundry versus Azure OpenAI versus AI Hub

```text
Default rules:
├─ AI/RAG workloads -> use Microsoft Foundry (kind: 'AIServices')
│   ├─ Create the Foundry resource + Foundry Project together
│   └─ Deploy the model at the Foundry resource level (accounts/deployments)
│
├─ ML/open-source model training required -> consider AI Hub (MachineLearningServices)
│   └─ Only upon explicit request or when capabilities unsupported by Foundry are needed
│
└─ Standalone Azure OpenAI resource ->
    Consider only upon explicit request or
    when official documentation requires a separate resource
```

> These rules are a **default selection guide** reflecting current Microsoft recommendations.
> Azure product relationships may change. Consult Microsoft Docs when in doubt.

### Monitoring

```text
Default rules:
├─ Foundry (AIServices) -> Application Insights is not required
└─ AI Hub (MachineLearningServices) -> Application Insights + Log Analytics are required
```
