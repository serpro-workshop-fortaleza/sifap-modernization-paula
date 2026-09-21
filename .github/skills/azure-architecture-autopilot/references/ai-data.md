# Domain pack: AI/data (v1)

Service configuration guide specialized in Azure AI/data workloads.
v1 scope: Foundry, AI Search, ADLS Gen2, Key Vault, Fabric, ADF, and VNet/PE.

> Required properties and common errors -> `service-gotchas.md`
> Dynamic information (API version, SKU, and region) -> `azure-dynamic-sources.md`
> Common patterns (PE, security, and naming) -> `azure-common-patterns.md`

---

## 1. Microsoft Foundry (CognitiveServices)

### Resource hierarchy

```text
Microsoft.CognitiveServices/accounts (kind: 'AIServices')
├── /projects          - Foundry Project (required for portal access)
└── /deployments       - Model deployments (GPT-4o, `embedding`, etc.)
```

### Core Bicep structure: 1. Microsoft Foundry (CognitiveServices)

```bicep
// Foundry resource
resource foundry 'Microsoft.CognitiveServices/accounts@<fetch>' = {
  name: foundryName
  location: location
  kind: 'AIServices'
  sku: { name: '<confirm with user>' }               // SKU confirmed after consulting Microsoft Docs in Phase 1
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: foundryName  // Required and globally unique. Cannot be changed after creation; if missing, delete and recreate
    allowProjectManagement: true
    publicNetworkAccess: 'Disabled'
    networkAcls: { defaultAction: 'Deny' }
  }
}

// Foundry Project: must be created together with Foundry
resource project 'Microsoft.CognitiveServices/accounts/projects@<fetch>' = {
  parent: foundry
  name: '${foundryName}-project'
  location: location
  sku: { name: '<same as parent>' }
  kind: 'AIServices'
  identity: { type: 'SystemAssigned' }
  properties: {}
}

// Model deployment: at the Foundry resource level
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@<fetch>' = {
  parent: foundry
  name: '<model-name>'                              // Confirmed in Phase 1
  sku: {
    name: '<deployment-type>'                        // GlobalStandard, Standard, etc.; consult Microsoft Docs
    capacity: <confirm with user>                    // Capacity units; check the range in Microsoft Docs
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: '<model-name>'                           // Availability verification is required
      version: '<fetch>'                             // Look up the version too
    }
  }
}
```

> `@<fetch>`: check the API version at the URLs in `azure-dynamic-sources.md`.
> Model name/version, deployment type, and capacity are all dynamic. Confirm them after consulting Microsoft Docs in Phase 1.

---

## 2. Azure AI Search

### Core Bicep structure: 2. Azure AI Search

```bicep
resource search 'Microsoft.Search/searchServices@<fetch>' = {
  name: searchName
  location: location
  sku: { name: '<confirm with user>' }
  identity: { type: 'SystemAssigned' }
  properties: {
    hostingMode: 'default'
    publicNetworkAccess: 'disabled'
    semanticSearch: '<confirm with user>'    // disabled | free | standard; check Microsoft Docs
  }
}
```

### Design notes: 2. Azure AI Search

- PE support: Basic SKU or higher (check the latest restrictions in Microsoft Docs)
- Semantic Ranker: enabled through the `semanticSearch` property (`disabled` | `free` | `standard`); check per-SKU support in Microsoft Docs
- Vector search: available in paid SKUs (check Microsoft Docs)
- Usually used with Foundry in RAG configurations

---

## 3. ADLS Gen2 (Storage Account)

### Core Bicep structure: 3. ADLS Gen2 (Storage Account)

```bicep
resource storage 'Microsoft.Storage/storageAccounts@<fetch>' = {
  name: storageName        // Lowercase letters and numbers only, no hyphens
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    isHnsEnabled: true                 // Never omit this property
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Disabled'
    networkAcls: { defaultAction: 'Deny' }
  }
}

// Container
resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@<fetch>' = {
  name: '${storage.name}/default/raw'
}
```

### Design notes: 3. ADLS Gen2 (Storage Account)

- `isHnsEnabled` cannot be changed after creation -> recreate the resource if the property was omitted
- PE: the use case may require both `blob` and `dfs` PEs
- Common containers: `raw`, `processed`, `curated`

---

## 4. Microsoft Fabric

### Core Bicep structure: 4. Microsoft Fabric

```bicep
resource fabric 'Microsoft.Fabric/capacities@<fetch>' = {
  name: fabricName
  location: location
  sku: { name: '<confirm with user>', tier: 'Fabric' }
  properties: {
    administration: {
      members: [ '<admin-email>' ]    // Required; without this value, deployment fails
    }
  }
}
```

### Design notes: 4. Microsoft Fabric

- Only Capacity can be provisioned through Bicep
- Workspace, Lakehouse, Warehouse, etc. must be created manually in the portal
- Confirm the administrator email with `ask_user`

### Required confirmation items when adding in Phase 1

When Fabric is added during the conversation, confirm the following items through `ask_user` before updating the diagram:

- [ ] **SKU/Capacity**: F2, F4, F8...; offer options after looking up available SKUs in Microsoft Docs
- [ ] **administration.members**: administrator email; without it, deployment fails

> Do not arbitrarily include unspecified subworkloads (OneLake, dataflows, Warehouse, etc.). Only Capacity can be provisioned through Bicep.

---

## 5. Azure Data Factory

### Core Bicep structure: 5. Azure Data Factory

```bicep
resource adf 'Microsoft.DataFactory/factories@<fetch>' = {
  name: adfName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    publicNetworkAccess: 'Disabled'
  }
}
```

### Design notes: 5. Azure Data Factory

- Self-hosted Integration Runtime requires manual configuration outside Bicep
- Used mainly in on-premises data ingestion scenarios
- PE `groupId`: `dataFactory`

---

## 6. AML / AI Hub (MachineLearningServices)

### When to use

```text
Decision rule:
├─ General AI/RAG -> use Foundry (AIServices)
└─ ML training or open-source models required -> consider AI Hub
  └─ Only upon explicit request
```

### Core Bicep structure: 6. AML / AI Hub (MachineLearningServices)

```bicep
resource hub 'Microsoft.MachineLearningServices/workspaces@<fetch>' = {
  name: hubName
  location: location
  kind: 'Hub'
  sku: { name: '<confirm with user>', tier: '<confirm with user>' }  // for example, Basic/Basic; check SKUs in Microsoft Docs
  identity: { type: 'SystemAssigned' }
  properties: {
    friendlyName: hubName
    storageAccount: storage.id
    keyVault: keyVault.id
    applicationInsights: appInsights.id    // Required for the Hub
    publicNetworkAccess: 'Disabled'
  }
}
```

### AI Hub dependencies

Additional resources required when using the Hub:

- Storage Account
- Key Vault
- Application Insights + Log Analytics Workspace
- Container Registry (optional)

---

## 7. Common AI/data architecture combinations

### RAG chat assistant

```text
Foundry (AIServices) + Project
├── <chat-model> (chat)              - Confirmed after checking availability in Phase 1
├── <embedding-model> (embedding)    - Confirmed after checking availability in Phase 1
├── AI Search (vector + semantic)
├── ADLS Gen2 (document storage)
└── Key Vault (secrets)
+ Complete VNet/PE configuration
```

### Data platform

```text
Fabric Capacity (analytics)
├── ADLS Gen2 (data lake)
├── ADF (ingestion)
└── Key Vault (secrets)
+ VNet/PE configuration
```
