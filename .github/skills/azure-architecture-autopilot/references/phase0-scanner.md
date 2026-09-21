# Phase 0: existing resource scanner

This file contains detailed Phase 0 instructions. Read and follow it when analysis of existing Azure resources is requested (Path B).

Results appear in an architecture diagram. Subsequent natural-language modification requests proceed to Phase 1.

> **Output storage path rule**: save all outputs (scan JSON, diagram HTML, and Bicep code) in **a project folder in the current working directory (cwd)**. NEVER save to `~/.copilot/session-state/`. That directory is temporary and may be deleted when the session ends.

---

## Step 1: Azure authentication and scope selection

### 1-A: check Azure authentication

```powershell
az account show 2>&1
```

- If authenticated → proceed to Step 1-B
- If not authenticated → ask the user to run `az login`

### 1-B: select subscriptions (multiple selection supported)

```powershell
az account list --output json
```

Present the subscription list as `ask_user` options. **Multiple subscriptions can be selected:**

```text
ask_user({
  question: "Select the Azure subscriptions to analyze. To select several, add one at a time.",
  choices: [
    "sub-002 (Current default subscription) (Recommended)",
    "sub-001",
    "Analyze all subscriptions above"
  ]
})
```

- One subscription selected → scan only that subscription
- "Analyze all" selected → scan all subscriptions
- To add subscriptions → use `ask_user` again

### 1-C: select scope (multiple RGs supported)

```text
ask_user({
  question: "Which Azure resource scope would you like to analyze?",
  choices: [
    "Specify a resource group (Recommended)",
    "Select multiple resource groups",
    "All resource groups in the current subscription"
  ]
})
```

- **Specific resource group (RG)** → select from the list or enter manually
- **Multiple RGs** → repeat `ask_user` to add one at a time. Stop when the user says they are done.
  Alternatively, accept multiple comma-separated RGs (for example, `rg-prod, rg-dev, rg-network`)
- **Entire subscription** → `az group list` → scan all RGs (warn that many resources may take time)

**Multiple subscriptions and multiple RGs can be combined:**

- rg-prod from subscription A + rg-network from subscription B → scan both and present a single diagram

---

## Diagram hierarchy: displaying multiple subscriptions/RGs

**One subscription + one RG**: VNet boundary only
**Multiple RGs (same subscription)**: dashed boundary for each RG
**Multiple subscriptions**: two-level boundary, subscription > RG

Pass hierarchy information in the diagram JSON:

**Add the `subscription` and `resourceGroup` fields to the `services` JSON:**

```json
{
  "id": "foundry",
  "name": "foundry-xxx",
  "type": "ai_foundry",
  "subscription": "sub-002",
  "resourceGroup": "rg-prod",
  "details": [...]
}
```

**Pass the hierarchy through the `--hierarchy` parameter:**

```text
--hierarchy '[{"subscription":"sub-002","resourceGroups":["rg-prod","rg-dev"]},{"subscription":"sub-001","resourceGroups":["rg-network"]}]'
```

With this information, the diagram script:

- Multiple RGs → represents each RG as a group with a dashed boundary (label: RG name)
- Multiple subscriptions → nests RG boundaries within larger subscription boundaries
- Displays VNet boundaries inside the RG to which it belongs

---

## Step 2: scan resources

**az command-line interface (CLI) output principles:**

- az CLI output must **always be saved to a file** and read with `view`. Direct terminal output may be truncated.
- Batch **at most three az commands** per PowerShell call. Too many commands may time out.
- Use JMESPath `--query` to extract only required fields and reduce output.

```powershell
# Correct approach: save to a file, then read
az resource list -g "<RG>" --query "[].{name:name,type:type,kind:kind,location:location}" -o json | Set-Content -Path "$outDir/resources.json"

# Incorrect approach: direct terminal output (may be truncated)
az resource list -g "<RG>" -o json
```

### 2-A: list and present all resources

```powershell
$outDir = "<project-name>/azure-scan"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

# Step 1: basic resource list (name, type, kind, and location)
az resource list -g "<RG>" --query "[].{name:name,type:type,kind:kind,location:location,id:id}" -o json | Set-Content "$outDir/resources.json"
```

**Immediately after reading resources.json, present the complete resource table:**

```text
Resource list for rg-<RG> (N resources)

┌─────────────────────────┬──────────────────────────────────────────────┬─────────────────┐
│ Name                    │ Type                                         │ Location        │
├─────────────────────────┼──────────────────────────────────────────────┼─────────────────┤
│ my-storage              │ Microsoft.Storage/storageAccounts             │ koreacentral    │
│ my-keyvault             │ Microsoft.KeyVault/vaults                    │ koreacentral    │
│ ...                     │ ...                                          │ ...             │
└─────────────────────────┴──────────────────────────────────────────────┴─────────────────┘

Fetching detailed information...
```

Present this table **first**. Do not leave the user waiting without knowing which resources exist.

### 2-B: dynamic detail queries based on resources.json

**Determine query commands dynamically based on the types found in resources.json.**

Do not use a fixed command list. Run only commands for types present in resources.json, according to the table.

**Type → detail query command mapping:**

| Type in resources.json | Detail query command | Output file |
|---|---|---|
| `Microsoft.Network/virtualNetworks` | `az network vnet list -g "<RG>" --query "[].{name:name,addressSpace:addressSpace.addressPrefixes,subnets:subnets[].{name:name,prefix:addressPrefix,pePolicy:privateEndpointNetworkPolicies}}" -o json` | `vnets.json` |
| `Microsoft.Network/privateEndpoints` | `az network private-endpoint list -g "<RG>" --query "[].{name:name,subnetId:subnet.id,targetId:privateLinkServiceConnections[0].privateLinkServiceId,groupIds:privateLinkServiceConnections[0].groupIds,state:provisioningState}" -o json` | `pe.json` |
| `Microsoft.Network/networkSecurityGroups` | `az network nsg list -g "<RG>" --query "[].{name:name,location:location,subnets:subnets[].id,nics:networkInterfaces[].id}" -o json` | `nsg.json` |
| `Microsoft.CognitiveServices/accounts` | `az cognitiveservices account list -g "<RG>" --query "[].{name:name,kind:kind,sku:sku.name,endpoint:properties.endpoint,publicAccess:properties.publicNetworkAccess,location:location}" -o json` | `cognitive.json` |
| `Microsoft.Search/searchServices` | `az search service list -g "<RG>" --query "[].{name:name,sku:sku.name,publicAccess:properties.publicNetworkAccess,semanticSearch:properties.semanticSearch,location:location}" -o json 2>$null` | `search.json` |
| `Microsoft.Compute/virtualMachines` | `az vm list -g "<RG>" --query "[].{name:name,size:hardwareProfile.vmSize,os:storageProfile.osDisk.osType,location:location,nicIds:networkProfile.networkInterfaces[].id}" -o json` | `vms.json` |
| `Microsoft.Storage/storageAccounts` | `az storage account list -g "<RG>" --query "[].{name:name,sku:sku.name,kind:kind,hns:properties.isHnsEnabled,publicAccess:properties.publicNetworkAccess,location:location}" -o json` | `storage.json` |
| `Microsoft.KeyVault/vaults` | `az keyvault list -g "<RG>" --query "[].{name:name,location:location}" -o json 2>$null` | `keyvault.json` |
| `Microsoft.ContainerService/managedClusters` | `az aks list -g "<RG>" --query "[].{name:name,kubernetesVersion:kubernetesVersion,sku:sku,agentPoolProfiles:agentPoolProfiles[].{name:name,count:count,vmSize:vmSize},networkProfile:networkProfile.networkPlugin,location:location}" -o json` | `aks.json` |
| `Microsoft.Web/sites` | `az webapp list -g "<RG>" --query "[].{name:name,kind:kind,sku:appServicePlan,state:state,defaultHostName:defaultHostName,httpsOnly:httpsOnly,location:location}" -o json` | `webapps.json` |
| `Microsoft.Web/serverFarms` | `az appservice plan list -g "<RG>" --query "[].{name:name,sku:sku.name,tier:sku.tier,kind:kind,location:location}" -o json` | `appservice-plans.json` |
| `Microsoft.DocumentDB/databaseAccounts` | `az cosmosdb list -g "<RG>" --query "[].{name:name,kind:kind,databaseAccountOfferType:databaseAccountOfferType,locations:locations[].locationName,publicAccess:publicNetworkAccess}" -o json` | `cosmosdb.json` |
| `Microsoft.Sql/servers` | `az sql server list -g "<RG>" --query "[].{name:name,fullyQualifiedDomainName:fullyQualifiedDomainName,publicAccess:publicNetworkAccess,location:location}" -o json` | `sql-servers.json` |
| `Microsoft.Databricks/workspaces` | `az databricks workspace list -g "<RG>" --query "[].{name:name,sku:sku.name,url:workspaceUrl,publicAccess:parameters.enableNoPublicIp.value,location:location}" -o json 2>$null` | `databricks.json` |
| `Microsoft.Synapse/workspaces` | `az synapse workspace list -g "<RG>" --query "[].{name:name,sqlAdminLogin:sqlAdministratorLogin,publicAccess:publicNetworkAccess,location:location}" -o json 2>$null` | `synapse.json` |
| `Microsoft.DataFactory/factories` | `az datafactory list -g "<RG>" --query "[].{name:name,publicAccess:publicNetworkAccess,location:location}" -o json 2>$null` | `adf.json` |
| `Microsoft.EventHub/namespaces` | `az eventhubs namespace list -g "<RG>" --query "[].{name:name,sku:sku.name,location:location}" -o json` | `eventhub.json` |
| `Microsoft.Cache/redis` | `az redis list -g "<RG>" --query "[].{name:name,sku:sku.name,port:port,sslPort:sslPort,publicAccess:publicNetworkAccess,location:location}" -o json` | `redis.json` |
| `Microsoft.ContainerRegistry/registries` | `az acr list -g "<RG>" --query "[].{name:name,sku:sku.name,adminUserEnabled:adminUserEnabled,publicAccess:publicNetworkAccess,location:location}" -o json` | `acr.json` |
| `Microsoft.MachineLearningServices/workspaces` | `az resource show --ids "<ID>" --query "{name:name,sku:sku,kind:kind,location:location,publicAccess:properties.publicNetworkAccess,hbiWorkspace:properties.hbiWorkspace,managedNetwork:properties.managedNetwork.isolationMode}" -o json` | `mlworkspace.json` |
| `Microsoft.Insights/components` | `az monitor app-insights component show -g "<RG>" --app "<NAME>" --query "{name:name,kind:kind,instrumentationKey:instrumentationKey,workspaceResourceId:workspaceResourceId,location:location}" -o json 2>$null` | `appinsights-<NAME>.json` |
| `Microsoft.OperationalInsights/workspaces` | `az monitor log-analytics workspace show -g "<RG>" -n "<NAME>" --query "{name:name,sku:sku.name,retentionInDays:retentionInDays,location:location}" -o json` | `log-analytics-<NAME>.json` |
| `Microsoft.Network/applicationGateways` | `az network application-gateway list -g "<RG>" --query "[].{name:name,sku:sku,location:location}" -o json` | `appgateway.json` |
| `Microsoft.Cdn/profiles` / `Microsoft.Network/frontDoors` | `az afd profile list -g "<RG>" --query "[].{name:name,sku:sku.name,location:location}" -o json 2>$null` | `frontdoor.json` |
| `Microsoft.Network/azureFirewalls` | `az network firewall list -g "<RG>" --query "[].{name:name,sku:sku,threatIntelMode:threatIntelMode,location:location}" -o json` | `firewall.json` |
| `Microsoft.Network/bastionHosts` | `az network bastion list -g "<RG>" --query "[].{name:name,sku:sku.name,location:location}" -o json` | `bastion.json` |

**Dynamic query process:**

1. Read `resources.json`
2. Extract distinct values of the `type` field
3. Run **only commands for matching types** in the table (skip absent types)
4. For a type absent from the table → use the generic query: `az resource show --ids "<ID>" --query "{name:name,sku:sku,kind:kind,location:location,properties:properties}" -o json`
5. Run commands in batches of two or three (not all at once)

### 2-C: query model deployments (when Cognitive Services is present)

```powershell
# Query model deployments for each Cognitive Services resource
az cognitiveservices account deployment list --name "<NAME>" -g "<RG>" --query "[].{name:name,model:properties.model.name,version:properties.model.version,sku:sku.name}" -o json | Set-Content "$outDir/<NAME>-deployments.json"
```

### 2-D: query NIC + public IP (when VMs are present)

```powershell
az network nic list -g "<RG>" --query "[].{name:name,subnetId:ipConfigurations[0].subnet.id,privateIp:ipConfigurations[0].privateIPAddress,publicIpId:ipConfigurations[0].publicIPAddress.id}" -o json | Set-Content "$outDir/nics.json"
az network public-ip list -g "<RG>" --query "[].{name:name,ip:ipAddress,sku:sku.name}" -o json | Set-Content "$outDir/public-ips.json"
```

From the VNet:

- `addressSpace.addressPrefixes` → CIDR
- `subnets[].name`, `subnets[].addressPrefix` → subnet information
- `subnets[].privateEndpointNetworkPolicies` → PE policies

---

## Step 3: infer resource relationships

Automatically infer **relationships (connections)** between scanned resources to create the `connections` JSON.

### Relationship inference rules

**With few connection lines, the diagram loses its meaning. Infer as many relationships as possible.**

#### Confirmed inference (directly verifiable through IDs/properties)

| Relationship type | Inference method | Connection type |
|---|---|---|
| PE → service | Extract the service ID from the PE's `privateLinkServiceId` | `private` |
| PE → VNet | Extract the VNet from the PE's `subnet.id` | (Represented by the VNet boundary) |
| Foundry → Project | Parent resource of `accounts/projects` | `api` |
| VM → NIC → subnet | Infer VNet/subnet from the NIC's `subnet.id` | (VNet boundary) |
| NSG → subnet | Check connected subnets in the NSG's `subnets[].id` | `network` |
| NSG → NIC | Check connected VMs in the NSG's `networkInterfaces[].id` | `network` |
| NIC → public IP | Check the PIP in the NIC's `publicIPAddress.id` | (Included in details) |
| Databricks → VNet | Workspace VNet injection configuration | (VNet boundary) |

#### Reasonable inference (common patterns between services in the same RG)

| Relationship type | Inference condition | Connection type |
|---|---|---|
| Foundry → AI Search | Both in the same RG → infer RAG connection | `api` (label: "RAG Search") |
| Foundry → Storage | Both in the same RG → infer data connection | `data` (label: "Data") |
| AI Search → Storage | Both in the same RG → infer indexing connection | `data` (label: "Indexing") |
| Service → Key Vault | Key Vault in the same RG → infer secret management | `security` (label: "Secrets") |
| VM → Foundry/Search | VM + AI services in the same RG → infer API calls | `api` (label: "API") |
| DI → Foundry | Document Intelligence + Foundry in the same RG → infer OCR/extraction | `api` (label: "OCR/Extraction") |
| ADF → Storage | ADF + Storage in the same RG → infer data flow | `data` (label: "Flow") |
| ADF → SQL | ADF + SQL in the same RG → infer data source | `data` (label: "Source") |
| Databricks → Storage | Both in the same RG → infer data lake connection | `data` (label: "Data Lake") |

#### Confirmation after inference

Present the inferred connection list and request confirmation:

```text
> **Resource relationships were inferred**. Please check whether they are correct.

Inferred connections:
- Foundry → AI Search (RAG Search)
- Foundry → Storage (Data)
- VM → Foundry (API Call)
- Document Intelligence → Foundry (OCR/Extraction)

Is this correct? Let me know whether you would like to add or remove connections.
```

#### Relationships that cannot be inferred

Some connections may not be inferred by these rules. Allow connections to be added freely.

### Query model deployments (when Foundry resources are present)

```powershell
az cognitiveservices account deployment list --name "<FOUNDRY_NAME>" -g "<RG>" --query "[].{name:name,model:properties.model.name,version:properties.model.version,sku:sku.name}" -o json
```

Add the model name, version, and SKU of each deployment to the Foundry node's `details`.

---

## Step 4: convert to services/connections JSON

Convert results to the built-in engine's input format.

### Resource type → diagram type mapping

| Azure resource type | Diagram type |
|---|---|
| `Microsoft.CognitiveServices/accounts` (kind: AIServices) | `ai_foundry` |
| `Microsoft.CognitiveServices/accounts` (kind: OpenAI) | `openai` |
| `Microsoft.CognitiveServices/accounts` (kind: FormRecognizer) | `document_intelligence` |
| `Microsoft.CognitiveServices/accounts` (kind: TextAnalytics etc.) | `ai_foundry` (default) |
| `Microsoft.CognitiveServices/accounts/projects` | `ai_foundry` |
| `Microsoft.Search/searchServices` | `search` |
| `Microsoft.Storage/storageAccounts` | `storage` |
| `Microsoft.KeyVault/vaults` | `keyvault` |
| `Microsoft.Databricks/workspaces` | `databricks` |
| `Microsoft.Sql/servers` | `sql_server` |
| `Microsoft.Sql/servers/databases` | `sql_database` |
| `Microsoft.DocumentDB/databaseAccounts` | `cosmos_db` |
| `Microsoft.Web/sites` | `app_service` |
| `Microsoft.ContainerService/managedClusters` | `aks` |
| `Microsoft.Web/sites` (kind: functionapp) | `function_app` |
| `Microsoft.Synapse/workspaces` | `synapse` |
| `Microsoft.Fabric/capacities` | `fabric` |
| `Microsoft.DataFactory/factories` | `adf` |
| `Microsoft.Compute/virtualMachines` | `vm` |
| `Microsoft.Network/privateEndpoints` | `pe` |
| `Microsoft.Network/virtualNetworks` | (Represented by the VNet boundary; not included in services) |
| `Microsoft.Network/networkSecurityGroups` | `nsg` |
| `Microsoft.Network/bastionHosts` | `bastion` |
| `Microsoft.OperationalInsights/workspaces` | `log_analytics` |
| `Microsoft.Insights/components` | `app_insights` |
| Other | `default` |

### Rules for constructing services JSON

```json
{
  "id": "resource name (lowercase, no special characters)",
  "name": "actual resource name",
  "type": "determined by the table above",
  "sku": "actual SKU (if available)",
  "private": true/false,  // true if a PE is connected
  "details": ["property1", "property2", ...]
}
```

**Information to include in details:**

- Endpoint URL
- SKU/tier details
- kind (AIServices, OpenAI, etc.)
- Model deployment list (Foundry)
- Key properties (`isHnsEnabled`, `semanticSearch`, etc.)
- Region

### VNet information → `--vnet-info` parameter

If a VNet is found, display it in the boundary label through `--vnet-info`:

```text
--vnet-info "10.0.0.0/16 | pe-subnet: 10.0.1.0/24 | <region>"
```

### PE node generation

If PEs exist, add each PE as a separate node and connect it to the corresponding service with type `private`:

```json
{"id": "pe_<serviceId>", "name": "PE: <serviceName>", "type": "pe", "details": ["groupId: <groupId>", "<status>"]}
```

---

## Step 5: generate and present the diagram

Diagram filename: `<project-name>/00_arch_current.html`

Use the scanned RG name as the default project name:

```text
ask_user({
  question: "Choose a project name. It will be the name of the results folder.",
  choices: ["<RG-name>", "azure-analysis"]
})
```

After generating the diagram, present:

```text
## Current Azure architecture

[Interactive diagram: 00_arch_current.html]

Scanned resources (N total):
[Summary table by type]

What would you like to change?
- Improve performance ("it is slow", "increase throughput")
- Optimize costs ("reduce costs", "make it cheaper")
- Strengthen security ("add PE", "block public access")
- Change the network ("separate the VNet", "add Bastion")
- Add/remove resources ("add a VM", "delete this")
- Monitor ("configure logs", "add alerts")
- Diagnose ("is this architecture appropriate?", "what is wrong?")
- Or just get the diagram and finish
```

---

## Step 6: discuss modifications → transition to Phase 1

When modifications are requested, proceed to Phase 1 (`phase1-advisor.md`).
This is the **Path B entry point**, which uses existing results as a baseline.

### Handling natural-language requests: clarification question patterns

Ask questions to make vague requests more specific:

**Performance**

| Request | Example clarification question |
|---|---|
| "It is slow" / "Responses take too long" | "Which service is slow? Should we increase the SKU or change the region?" |
| "I want to increase throughput" | "For which service? Should we scale out or increase DTU/RU?" |
| "AI Search indexing is slow" | "Should we add partitions or use the S2 SKU?" |

**Cost**

| Request | Example clarification question |
|---|---|
| "I want to reduce costs" | "For which service? Should we reduce the SKU or remove unused resources?" |
| "How much does it cost?" | Look up prices on Microsoft Docs and estimate based on current SKUs |
| "It is a development environment, keep it cheap" | "Which services should move to Free/Basic tiers?" |

**Security**

| Request | Example clarification question |
|---|---|
| "Strengthen security" | "Should we add PEs to services without one, check RBAC, and disable publicNetworkAccess?" |
| "Block public access" | "Should we apply PE + publicNetworkAccess: Disabled to all services?" |
| "Manage keys" | "Should we add Key Vault and connect it using Managed Identity?" |

**Network**

| Request | Example clarification question |
|---|---|
| "Add PE" | "To which service? Should we add it to all at once?" |
| "Separate the VNet" | "Which subnets should be separated? Should we add NSGs?" |
| "Add Bastion" | "To add Azure Bastion for VM access, provide the subnet CIDR." |

**Add/remove resources**

| Request | Example clarification question |
|---|---|
| "Add a VM" | "How many? Which SKU? In the same VNet? Which operating system?" |
| "Add Fabric" | "Which SKU? What is the administrator's email?" |
| "Delete this" | "Confirm removal of [resource name]? Connected PEs will also be removed." |

**Monitoring/operations**

| Request | Example clarification question |
|---|---|
| "I want to see the logs" | "Should we add a Log Analytics Workspace and connect Diagnostic Settings?" |
| "Configure alerts" | "For which metrics: CPU, error rate, or response time?" |
| "Attach Application Insights" | "To which service: App Service or Function App?" |

**Migration/changes**

| Request | Example clarification question |
|---|---|
| "Change the region" | "To which region? I will check availability for all services." |
| "Replace SQL with Cosmos" | "Which Cosmos DB API type (SQL/MongoDB/Cassandra)? I can also provide a migration guide." |
| "Replace Foundry with Hub" | "Hub is suitable when ML/open-source model training is needed. Let us check the use case." |

**Diagnosis/questions**

| Request | Example clarification question |
|---|---|
| "What is wrong?" | Analyze the current configuration (open `publicNetworkAccess`, disconnected PE, unsuitable SKU, etc.) and suggest improvements |
| "Is this architecture appropriate?" | Review with the Well-Architected Framework: security, reliability, performance, cost, and operations |
| "Is the PE connected correctly?" | Check with `az network private-endpoint show` and report |
| "I only want the diagram" | Do not proceed to Phase 1; provide the path to 00_arch_current.html and finish |

After finalizing modifications:

1. Apply the Phase 1 Change Confirmation Rule
2. Verify facts (cross-validation on Microsoft Docs)
3. Generate the updated diagram (`01_arch_diagram_draft.html`)
4. After confirmation → proceed to Phases 2 through 4

---

## Scan performance optimization

- If there are more than 50 resources, warn: "There are many resources; scanning may take time."
- Run `az resource list` first to count resources, then perform detail queries
- Query major services first (Foundry, Search, Storage, Key Vault, VNet, and PE); retrieve only basic information for the rest with `az resource show`
- Report progress:
  > **Scanning resources**: M of N resources completed

---

## Handling unsupported resources

For types absent from the diagram mapping:

- Display with type `default` (question mark icon)
- Include the resource name and type in `details`
- Present the resource, but do not attempt to infer relationships
