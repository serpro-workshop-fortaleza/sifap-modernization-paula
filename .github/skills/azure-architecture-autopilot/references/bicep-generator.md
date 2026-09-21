# Bicep generator agent

Receives the final architecture specification from Phase 1 and generates deployable Bicep templates.

## Step 0: check the latest specifications (required before generating Bicep)

Do not hardcode API versions in Bicep code.
Always consult the Bicep reference on Microsoft Docs and confirm the latest stable `apiVersion` before using it.

### Verification steps

1. Identify the service list
2. Fetch each service's Microsoft Docs URL with `web_fetch`
3. Confirm the latest stable API version
4. Write Bicep using that version

### Model deployment availability check (required for Foundry/OpenAI models)

Check whether the specified model can be deployed in the target region **before generating Bicep**.
Availability varies by region and changes frequently. Do not rely on static knowledge.

**Verification methods (in priority order):**

1. Check availability on Microsoft Docs: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
2. Or query directly through the Azure CLI:

   ```powershell
   az cognitiveservices account list-models --name "<FOUNDRY_NAME>" --resource-group "<RG_NAME>" -o table
   ```

  (When the Foundry resource already exists)

**If the model is unavailable in the target region:**

- Report this and suggest available regions or alternative models
- Do not replace the model or region without approval

### Microsoft Docs URLs by service

The complete URL registry is in `references/azure-dynamic-sources.md`. Consult it when researching.
Reference files are under `.github/skills/azure-architecture-autopilot/`.

> **Important**: fetch the URL directly with `web_fetch` to confirm the latest stable `apiVersion`. Do not use fixed versions from references or previous conversations without verification.

> **Always check child resources too**: look up API versions for child resources (`accounts/projects`, `accounts/deployments`, `privateDnsZones/virtualNetworkLinks`, `privateEndpoints/privateDnsZoneGroups`, etc.) on the parent page. Versions may differ.

> **The same principle applies to errors/warnings**: if an API version error occurs during change analysis (`what-if`) or deployment, do not treat the version in the message as the latest. Check Microsoft Docs again before fixing it.

---

## Information lookup principles (stable versus dynamic)

### Always look up (dynamic)

- API version → consult the URLs in `azure-dynamic-sources.md`
- Model availability (name, version, and region) → look up
- SKU/pricing list → look up
- Regional availability → look up

### Consult references first (stable)

- Required property patterns (`isHnsEnabled`, `allowProjectManagement`, etc.) → `service-gotchas.md`
- PE `groupId` and DNS Zone mappings (major services) → `service-gotchas.md`
- Common PE, security, and naming patterns → `azure-common-patterns.md`
- AI/data service configuration guide → `ai-data.md`

> When unsure about stable information, reconfirm it on Microsoft Docs. A lookup is not required every time.

---

## Fallback flow for an unknown service

When the request includes a service outside the v1 scope (`ai-data.md`):

1. **Inform**: "This service is outside the standard v1 scope. It will be generated on a best-effort basis using Microsoft Docs."
2. **Look up the API version**: build and fetch the URL in the format `https://learn.microsoft.com/en-us/azure/templates/microsoft.{provider}/{resourceType}`
3. **Identify the type and required properties**: confirm them in the retrieved documentation
4. **Check the PE mapping**: consult `https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns` to confirm `groupId`/DNS Zone
5. **Apply common patterns**: use security, networking, and naming patterns from `azure-common-patterns.md`
6. **Write Bicep**: generate the module using the information above
7. **Hand off to the reviewer**: validate compilation with `az bicep build`

## Input information

The following information must be finalized by the end of Phase 1:

```text
- services: [Service list + SKU]
- networking: Whether private_endpoint is used
- resource_group: Resource group name
- location: Deployment location (confirmed in Phase 1)
- subscription_id: Azure subscription ID
```

## Output file structure

```text
<project-name>/
├── main.bicep              # Main orchestration: module calls and parameter passing
├── main.bicepparam         # Parameter file: environment values, no sensitive information
└── modules/
  ├── network.bicep           # VNet, Subnet (includes pe-subnet)
  ├── ai.bicep                # AI services (configured according to requirements)
  ├── storage.bicep           # ADLS Gen2 (isHnsEnabled: true required)
  ├── fabric.bicep            # Microsoft Fabric Capacity (only when needed)
    ├── keyvault.bicep          # Key Vault
  ├── monitoring.bicep        # Application Insights, Log Analytics (Hub-based configurations only)
  └── private-endpoints.bicep # All PEs + Private DNS Zones + VNet Links + DNS Zone Groups
```

## Module responsibilities

### `network.bicep`

- VNet: accepts CIDR as a parameter to avoid conflicts with existing address spaces
- pe-subnet: requires `privateEndpointNetworkPolicies: 'Disabled'`
- Additional subnets: handled through parameters as needed

### `ai.bicep`

- **Microsoft Foundry resource** (`Microsoft.CognitiveServices/accounts`, `kind: 'AIServices'`): top-level AI resource
  - `customSubDomainName: foundryName` is required. **Cannot be changed after creation. If omitted, delete and recreate the resource**
  - `identity: { type: 'SystemAssigned' }` is required
  - `allowProjectManagement: true` is required
  - Model deployment (`Microsoft.CognitiveServices/accounts/deployments`): performed at the Foundry resource level
- **Foundry Project** (`Microsoft.CognitiveServices/accounts/projects`): **must be created as a child resource**
  - Resource type: `Microsoft.CognitiveServices/accounts/projects` (never create as a standalone `accounts` resource)
  - Use `parent: foundryAccount` in Bicep
  - Incorrect example: creating a Project as a separate `kind: 'AIServices'` account → the portal does not recognize it
  - Correct example:

    ```bicep
    resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@<apiVersion>' = {
      parent: foundryAccount
      name: 'project-${uniqueString(resourceGroup().id)}'
      location: location
      kind: 'AIServices'
      properties: {}
    }
    ```

- **Azure AI Search**: Semantic Ranking and vector search configuration
- Consider the Hub-based option (`Microsoft.MachineLearningServices/workspaces`) only on explicit request or when ML training/open-source models are needed. For typical AI/RAG workloads, Foundry (AIServices) is the default

**Prohibited CognitiveServices properties:**

- `apiProperties.statisticsEnabled`: this property does not exist. Never use it. It causes the `ApiPropertiesInvalid` deployment error
- `apiProperties.qnaAzureSearchEndpointId`: exclusive to QnA Maker. Do not use with Foundry
- Do not arbitrarily add unvalidated properties to `properties.apiProperties`

### `storage.bicep`

- ADLS Gen2: `isHnsEnabled: true` ← **never omit this property**
- Containers: raw, processed, curated (or as required)
- `allowBlobPublicAccess: false`, `minimumTlsVersion: 'TLS1_2'`

### `keyvault.bicep`

- `enableRbacAuthorization: true` (do not use the Access Policy model)
- `enableSoftDelete: true`, `softDeleteRetentionInDays: 90`
- `enablePurgeProtection: true`

### `monitoring.bicep`

- Log Analytics Workspace
- Application Insights (needed only for Hub-based configurations; not required for Foundry AIServices)

### `private-endpoints.bicep`

- A set of three components for each service:
  1. `Microsoft.Network/privateEndpoints` (placed in pe-subnet)
  2. `Microsoft.Network/privateDnsZones` + VNet Link (`registrationEnabled: false`)
  3. `Microsoft.Network/privateEndpoints/privateDnsZoneGroups`
- For each service's DNS Zone mappings, see `references/service-gotchas.md`

**PE DNS rules for Foundry/AIServices:**

- PE `groupId`: `account`
- The DNS Zone Group must include **two zones**:
  1. `privatelink.cognitiveservices.azure.com`
  2. `privatelink.openai.azure.com`
- Including only one causes DNS resolution failure for OpenAI API calls → connection error

**PE rules for ADLS Gen2 (`isHnsEnabled: true`):**

- Two required PEs:
  1. `blob` → `privatelink.blob.core.windows.net`
  2. `dfs` → `privatelink.dfs.core.windows.net`
- Without the DFS PE, Data Lake operations such as filesystem creation and directory manipulation fail

### `rbac.bicep` (or embedded in main.bicep)

**RBAC role assignment: never omit**

**Every service with a Managed Identity (`identity.type: 'SystemAssigned'`) must have RBAC role assignments.**
An identity without assigned roles causes service-to-service authentication failures.
This is not optional. It is a **required item**.
The Phase 3 review will report the omission as CRITICAL.

- Required RBAC mappings:

| Source service | Target service | Role | Role definition ID |
|------------|-----------|------|-------------------|
| Foundry | Storage | `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` |
| Foundry | AI Search | `Search Index Data Contributor` | `8ebe5a00-799e-43f5-93ac-243d3dce84a7` |
| Foundry | AI Search | `Search Service Contributor` | `7ca78c08-252a-4471-8644-bb5ff32d4ba0` |
| App Service | Key Vault | `Key Vault Secrets User` | `4633458b-17de-408a-b874-0445c86b69e6` |
| AKS (kubeletIdentity) | ACR | `AcrPull` | `7f951dda-4ed3-4680-a7ca-43fe172d538d` |
| Data Factory | Storage | `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` |
| Data Factory | Key Vault | `Key Vault Secrets User` | `4633458b-17de-408a-b874-0445c86b69e6` |
| Databricks | Storage | `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` |

> **AKS special rule**: AKS uses `identityProfile.kubeletidentity.objectId`, not `identity.principalId`.

```bicep
// RBAC example: Foundry → Storage Blob Data Contributor
resource foundryStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, foundry.id, 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: foundry.identity.principalId
    principalType: 'ServicePrincipal'
  }
}
```

### SQL Server rules

- **Password management**: declare `@secure() param sqlAdminPassword string` in main.bicep and pass it to modules
  - Do not generate it with `newGuid()` inside modules, since the password changes on redeployment
  - Store it as a Key Vault secret for retrieval after deployment
- **Authentication method**: use `administrators.azureADOnlyAuthentication: true` by default
  - Many organizational policies (MCAPS, etc.) block standalone SQL authentication
  - AAD-only authentication + Managed Identity is the most secure configuration

### Network secret handling

- **VPN Gateway shared key**: `@secure() param vpnSharedKey string`; `@secure()` is required
- Never include plaintext VPN keys in `.bicepparam`; supply them at deployment or use a Key Vault reference
- The same rule applies to SQL passwords
- **Applies to**: VPN shared key, ExpressRoute authorization key, Wi-Fi PSK, and all other network secrets
- Module parameters must also include the `@secure()` decorator

### Network isolation consistency rules

- When setting `publicNetworkAccess: 'Disabled'`, you **must also** create the corresponding service PE
- Setting publicNetworkAccess to Disabled without a PE makes the service inaccessible → unusable after deployment
- The Phase 3 reviewer must report this inconsistency as **CRITICAL**
- When the inconsistency is found, add a PE module or revert publicNetworkAccess to Enabled

## Mandatory coding principles

### Naming conventions

```bicep
// Use uniqueString to avoid name collisions: always required
param foundryName string = 'foundry-${uniqueString(resourceGroup().id)}'
param searchName string = 'srch-${uniqueString(resourceGroup().id)}'
param storageName string = 'st${uniqueString(resourceGroup().id)}'  // Special characters are not allowed
param keyVaultName string = 'kv-${uniqueString(resourceGroup().id)}'
```

> **Resources requiring `customSubDomainName` (Foundry, Cognitive Services, etc.) must include `uniqueString()`.**
> Static strings, such as `'my-rag-chatbot'`, may already be used by another tenant and cause failures.
> The same applies to Foundry Project names: `'project-${uniqueString(resourceGroup().id)}'`

### Network isolation

```bicep
// Required for all services when using Private Endpoints
publicNetworkAccess: 'Disabled'
networkAcls: {
  defaultAction: 'Deny'
  ipRules: []
  virtualNetworkRules: []
}
```

### Dependency management

```bicep
// Use implicit dependencies through resource references instead of explicit dependsOn
resource aiProject '...' = {
  properties: {
    hubResourceId: aiHub.id  // Reference to aiHub → aiHub is automatically deployed first
  }
}
```

### Security

```bicep
// Use Key Vault references for sensitive values; never store plaintext in parameters
@secure()
param adminPassword string  // Do not enter plaintext values in main.bicepparam
```

### Code comments

```bicep
// Microsoft Foundry resource: kind: 'AIServices'
// customSubDomainName: required and globally unique. Cannot be changed after creation; if omitted, delete and recreate the resource
// allowProjectManagement: true is required; without it, Foundry Project creation fails
// Replace apiVersion with the latest version retrieved in Step 0
resource foundry 'Microsoft.CognitiveServices/accounts@<version fetched in Step 0>' = {
  kind: 'AIServices'
  properties: {
    customSubDomainName: foundryName
    allowProjectManagement: true
    ...
  }
}
```

### Bicep code quality validation (required after generation)

**Module declaration validation:**

- Check that the `name:` property is not duplicated in each module block
- Correct example: `name: 'deploy-sql'`
- Incorrect example: `name: 'name: 'deploy-sql'` (duplicate `name:` → compilation error)

**Duplicate property prevention:**

- Repeating a property name in the same resource block causes a compilation error
- This is common in complex resources such as VPN Gateway (`gatewayType`), Firewall, AKS, etc.
- Look for `BCP025: The property "xxx" is declared multiple times` in `az bicep build` output

**`az bicep build` must be run:**

- After generating all Bicep files, always run `az bicep build --file main.bicep`
- Fix errors and build again
- Warnings (`WARNING`, such as BCP081) may be ignored after checking the API version on Microsoft Docs

## Basic main.bicep structure

```bicep
// ============================================================
// Azure infrastructure for [Project name]: main.bicep
// Generated on: [Date]
// ============================================================

targetScope = 'resourceGroup'

// ── Common parameters ─────────────────────────────────────
param location string   // Location confirmed in Phase 1; do not hardcode the value
param projectPrefix string
param vnetAddressPrefix string    // ← Confirm. Avoids conflicts with existing networks
param peSubnetPrefix string       // ← CIDR of the dedicated PE subnet inside the VNet

// ── Network ──────────────────────────────────────────────────
module network './modules/network.bicep' = {
  name: 'deploy-network'
  params: {
    location: location
    vnetAddressPrefix: vnetAddressPrefix
    peSubnetPrefix: peSubnetPrefix
  }
}

// ── AI/data services ──────────────────────────────────
module ai './modules/ai.bicep' = {
  name: 'deploy-ai'
  params: {
    location: location
    // Add separate parameters if regions vary by service; verify them on Microsoft Docs
  }
  dependsOn: [network]
}

// ── Storage ─────────────────────────────────────────
module storage './modules/storage.bicep' = {
  name: 'deploy-storage'
  params: {
    location: location
  }
}

// ── Key Vault ─────────────────────────────────────────────
module keyVault './modules/keyvault.bicep' = {
  name: 'deploy-keyvault'
  params: {
    location: location
  }
}

// ── Private Endpoints (all services) ─────────────────
module privateEndpoints './modules/private-endpoints.bicep' = {
  name: 'deploy-private-endpoints'
  params: {
    location: location
    vnetId: network.outputs.vnetId
    peSubnetId: network.outputs.peSubnetId
    foundryId: ai.outputs.foundryId
    searchId: ai.outputs.searchId
    storageId: storage.outputs.storageId
    keyVaultId: keyVault.outputs.keyVaultId
  }
}

// ── Outputs ────────────────────────────────────────────────
output vnetId string = network.outputs.vnetId
output foundryEndpoint string = ai.outputs.foundryEndpoint
output searchEndpoint string = ai.outputs.searchEndpoint
```

## Basic main.bicepparam structure

```bicep
using './main.bicep'

param location = '<Location confirmed in Phase 1>'
param projectPrefix = '<Project prefix>'
// Do not enter sensitive values here; use Key Vault references
// Set regions after checking each service's availability on Microsoft Docs
```

### Handling @secure() parameters

When a `.bicepparam` file contains the `using` directive, additional `--parameters` options cannot be used with `az deployment`.
Therefore, `@secure()` parameters must follow these rules:

- **Set a default value when possible**: `@secure() param password string = newGuid()`
- **If @secure() parameters require input**: also generate a JSON parameter file (`main.parameters.json`) instead of using `.bicepparam`
- **Never do this**: generate a command using `.bicepparam` and `--parameters key=value` simultaneously

## Common error checklist

The complete list is in `references/service-gotchas.md`. Summary:

| Item | Incorrect | Correct |
|------|--------|----------|
| ADLS Gen2 | Missing `isHnsEnabled` | `isHnsEnabled: true` |
| PE subnet | Policy not configured | `privateEndpointNetworkPolicies: 'Disabled'` |
| PE configuration | Only the PE was created | PE + DNS Zone + VNet Link + DNS Zone Group |
| Foundry | `kind: 'OpenAI'` | `kind: 'AIServices'` + `allowProjectManagement: true` |
| Foundry | Missing `customSubDomainName` | `customSubDomainName: foundryName`; cannot be changed after creation |
| Foundry Project | Not created | Must always be created together with the Foundry resource |
| Hub usage | Used for typical AI | Only on explicit request or when ML/open-source models are needed |
| Public network | Not configured | `publicNetworkAccess: 'Disabled'` |
| Storage name | Contains hyphens | Lowercase letters + digits only; `uniqueString()` is recommended |
| API version | Copied from a previous value | Consult Microsoft Docs (dynamic) |
| Region | Hardcoded value | Parameter + verification on Microsoft Docs (dynamic) |

## After generation is complete

When Bicep generation is complete:

1. Present a summary of generated files and each file's purpose
2. Proceed immediately to Phase 3 (Bicep reviewer)
3. The reviewer performs the review and automatic fixes according to `references/bicep-reviewer.md`
