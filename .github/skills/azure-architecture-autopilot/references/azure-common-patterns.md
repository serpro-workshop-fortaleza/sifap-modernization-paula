# Common Azure patterns (stable)

This file contains only **nearly immutable patterns** recurring across Azure services.
Dynamic information, such as API version, SKU, and region, does not appear here -> see `azure-dynamic-sources.md`.

---

## 1. Network isolation patterns

### Private Endpoint three-component set

All services using PE must have these three components configured:

1. **Private Endpoint**: placed in pe-subnet
2. **Private DNS Zone** + **VNet Link** (`registrationEnabled: false`)
3. **DNS Zone Group**: linked to the PE

> If any component is missing, DNS resolution will fail even with the PE present, preventing connection.

### Required PE subnet settings

```bicep
resource peSubnet 'Microsoft.Network/virtualNetworks/subnets' = {
  properties: {
    addressPrefix: peSubnetPrefix              // CIDR as a parameter to avoid conflicts with existing networks
    privateEndpointNetworkPolicies: 'Disabled'  // Required. PE deployment fails without this setting
  }
}
```

### publicNetworkAccess pattern

Services using PE must include:

```bicep
properties: {
  publicNetworkAccess: 'Disabled'
  networkAcls: {
    defaultAction: 'Deny'
  }
}
```

---

## 2. Security patterns

### Key Vault

```bicep
properties: {
  enableRbacAuthorization: true    // Do not use the Access Policy method
  enableSoftDelete: true
  softDeleteRetentionInDays: 90
  enablePurgeProtection: true
}
```

### Managed Identity

When AI services access other resources:

```bicep
identity: {
  type: 'SystemAssigned'  // or 'UserAssigned'
}
```

### Sensitive information

- Use the `@secure()` decorator
- Do not store plaintext in `.bicepparam` files
- Use Key Vault references

---

## 3. Naming conventions (CAF-based)

```text
rg-{project}-{env}          Resource Group
vnet-{project}-{env}        Virtual Network
st{project}{env}             Storage Account (no special characters; lowercase letters and numbers only)
kv-{project}-{env}           Key Vault
srch-{project}-{env}         AI Search
foundry-{project}-{env}      Cognitive Services (Foundry)
```

> Name collision prevention: using `uniqueString(resourceGroup().id)` is recommended
>
> ```bicep
> param storageName string = 'st${uniqueString(resourceGroup().id)}'
> ```

---

## 4. Bicep module structure

```text
<project>/
├── main.bicep              # Orchestration: module calls + parameter passing
├── main.bicepparam         # Environment-specific values (no sensitive information)
└── modules/
  ├── network.bicep           # VNet, subnet
  ├── <service>.bicep         # Per-service modules
    ├── keyvault.bicep          # Key Vault
  └── private-endpoints.bicep # All PEs + DNS Zone + VNet Link
```

### Dependency management

```bicep
// Correct: implicit dependency through resource reference
resource project '...' = {
  properties: {
  parentId: foundry.id  // reference to foundry -> automatically deploys foundry first
  }
}

// Avoid: explicit dependsOn (use only when needed)
```

---

## 5. Common PE Bicep template

```bicep
// ── Private Endpoint ──
resource pe 'Microsoft.Network/privateEndpoints@<fetch>' = {
  name: 'pe-${serviceName}'
  location: location
  properties: {
    subnet: { id: peSubnetId }
    privateLinkServiceConnections: [{
      name: 'pls-${serviceName}'
      properties: {
        privateLinkServiceId: serviceId
        groupIds: ['<groupId>']  // Varies by service. See service-gotchas.md
      }
    }]
  }
}

// ── Private DNS Zone ──
resource dnsZone 'Microsoft.Network/privateDnsZones@<fetch>' = {
  name: '<dnsZoneName>'  // Varies by service
  location: 'global'
}

// ── VNet Link ──
resource vnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@<fetch>' = {
  parent: dnsZone
  name: '${dnsZone.name}-link'
  location: 'global'
  properties: {
    virtualNetwork: { id: vnetId }
    registrationEnabled: false  // Must be false
  }
}

// ── DNS Zone Group ──
resource dnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@<fetch>' = {
  parent: pe
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [{
      name: 'config'
      properties: { privateDnsZoneId: dnsZone.id }
    }]
  }
}
```

> `@<fetch>`: always check the latest stable API version in Microsoft Docs before deployment.
