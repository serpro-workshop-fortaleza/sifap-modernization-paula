---
name: "azure-resource-visualizer"
description: "Use when the user wants a read-only Mermaid diagram of an existing Azure resource group or help understanding how deployed resources relate. Inspects resource groups, maps relationships, and generates a documented Mermaid architecture diagram. Triggers include \"diagram my resource group\", \"visualize Azure resources\", \"how do these resources connect\", and \"draw my architecture\". For a complete design and deployment pipeline, use azure-architecture-autopilot."
---
# Azure resource visualizer

Inspect Azure resource groups, understand their structure and relationships, and generate comprehensive Mermaid diagrams that clearly illustrate the architecture. This skill performs **read-only** analysis and never modifies or deletes Azure resources.

> [!NOTE]
> This skill depends on the **Azure MCP server** (or the `az` CLI) to list and describe resources. If neither is available, report that and request an exported resource inventory.

## When to Invoke

- "Draw a Mermaid diagram of my production resource group."
- "Help me understand how the resources in rg-sifap connect."
- "Visualize this subscription's network and data flows."
- "Document the architecture of our deployed Azure environment."

## Core responsibilities

1. **Resource group discovery**: list available groups when none is specified.
2. **In-depth resource analysis**: inspect all resources, their configurations, and interdependencies.
3. **Relationship mapping**: identify and document all connections between resources.
4. **Diagram generation**: create a detailed, accurate Mermaid diagram.
5. **Documentation**: produce a clear Markdown file with the embedded diagram.

## Workflow

### Step 1: Resource group selection

If the user has not specified a resource group:

1. Query available resource groups (Azure MCP tools or `az group list` as a fallback).
2. Present a numbered list of resource groups with their locations.
3. Ask the user to select a group by number or name and wait for the response.

If a resource group is specified, validate its existence and proceed.

### Step 2: Resource discovery and analysis

1. **Query all resources** in the group (Azure MCP tools or `az resource list --resource-group <name> --output json`).
2. **Analyze each resource** and record name and type, SKU/tier, location, key configuration, network settings (VNets, subnets, private endpoints), identity and access (managed identity, RBAC), and dependencies.
3. **Map relationships**:
    - **Network**: VNet peering, subnet assignments, NSG rules, and private endpoints.
    - **Data flow**: applications to databases, functions to storage, and API Management to backend services.
    - **Identity**: managed identities connecting to resources.
    - **Configuration**: application settings pointing to Key Vaults and connection strings.
    - **Dependencies**: parent-child resource relationships and prerequisite resource relationships.

### Step 3: Diagram construction

Create a detailed Mermaid diagram with `graph TB` (top to bottom) or `graph LR` (left to right):

```mermaid
graph TB
    subgraph "Resource group: name"
        subgraph "Network layer"
            VNET[Virtual Network<br/>10.0.0.0/16]
            SUBNET1[Subnet: web<br/>10.0.1.0/24]
            NSG[Network Security Group]
        end
        subgraph "Compute layer"
            APP[App Service<br/>Plan: P1v2]
            FUNC[Function App<br/>Runtime: .NET 8]
        end
        subgraph "Data layer"
            SQL[Azure SQL Database<br/>DTU: S1]
            STORAGE[Storage Account<br/>Standard LRS]
        end
        subgraph "Security and identity"
            KV[Key Vault]
            MI[Managed Identity]
        end
    end
    APP -->|"HTTPS requests"| FUNC
    FUNC -->|"SQL connection"| SQL
    FUNC -->|"Blob/Queue access"| STORAGE
    APP -->|"Uses identity"| MI
    MI -->|"Accesses secrets"| KV
    VNET --> SUBNET1
    SUBNET1 --> APP
    NSG -->|"Rules applied to"| SUBNET1
```

Diagram requirements:

- **Group by layer or purpose**: network, compute, data, security, and monitoring.
- **Include details**: SKUs, tiers, and important settings in node labels (use `<br/>` for line breaks).
- **Label every connection**: describe what flows between resources (data, identity, network).
- **Use meaningful node IDs**: abbreviations that make sense (`APP`, `FUNC`, `SQL`, `KV`).
- **Connection types**: `-->` for data flow or dependencies, `-.->` for optional/conditional connections, and `==>` for critical/main paths.

Include the relevant configuration detail for each resource type:

| Resource type | Include in label |
|---|---|
| App Service | Plan tier (B1, S1, P1v2) |
| Functions | Runtime (.NET, Python, Node) |
| Databases | Tier (Basic, Standard, Premium) |
| Storage | Redundancy (LRS, GRS, ZRS) |
| VNets | Address space |
| Subnets | Address range |

### Step 4: File creation

Use [assets/template-architecture.md](./assets/template-architecture.md) as the template and create `<resource-group-name>-architecture.md` with a header (resource group, subscription, region), a 2-3 paragraph summary, a resource inventory table, a Mermaid diagram, relationship details, and notes. Create it in the workspace root or a `docs/` folder, if one exists.

## Operational guidelines

| Standard | Requirement |
|---|---|
| Accuracy | Verify each resource detail before including it |
| Completeness | Include every resource in the group, without omissions |
| Clarity | Use clear labels and logical grouping |
| Detail | Include configuration details that affect the architecture |
| Relationships | Show all meaningful connections, not just the obvious ones |

| Always | Never |
|---|---|
| List resource groups if none is specified | Ignore resources because they seem unimportant |
| Wait for the user's selection before proceeding | Assume relationships without verification |
| Analyze every resource in the group | Produce incomplete diagrams or placeholders |
| Include configuration details in node labels | Omit details that affect the architecture |
| Group resources logically with subgraphs | Generate invalid Mermaid syntax |
| Keep analysis read-only | Modify or delete Azure resources |

Edge cases:

- **No resources found**: inform the user and verify the resource group name.
- **Permission issues**: explain what is missing and suggest checking RBAC.
- **Complex architectures (more than 50 resources)**: consider multiple diagrams by layer.
- **Cross-resource-group dependencies**: record external dependencies in the diagram notes.

## Output Template

The skill produces `<resource-group-name>-architecture.md`. Below the H1 title (`Azure architecture: <resource group>`), it contains a header block, an inventory table, the diagram, and relationship notes:

````markdown
**Subscription**: sub-sifap-prod
**Region**: eastus
**Resource count**: 4

## Resource inventory

| Resource | Type | Tier/SKU | Location | Notes |
|---|---|---|---|---|
| app-prod-001 | App Service | P1v2 | eastus | Production web application |
| sql-prod-001 | Azure SQL | S1 | eastus | Primary database |
| kv-prod-001 | Key Vault | standard | eastus | Application secrets |

## Architecture diagram

```mermaid
graph TB
    subgraph "rg-prod-app"
        APP[App Service<br/>P1v2]
        SQL[Azure SQL<br/>S1]
        KV[Key Vault]
        MI[Managed Identity]
    end
    APP -->|"Uses identity"| MI
    MI -->|"Reads secrets"| KV
    APP -->|"SQL connection"| SQL
```

## Relationship details

- App Service authenticates to Key Vault and SQL through a managed identity.
````

## Quality Gate

- [ ] A valid resource group was identified and confirmed before analysis.
- [ ] Every resource in the group was discovered and analyzed.
- [ ] All meaningful relationships (network, data, identity, and configuration) are mapped.
- [ ] The Mermaid diagram uses logical subgraphs and renders with valid syntax.
- [ ] A complete `<resource-group-name>-architecture.md` file was created from the template.
- [ ] Analysis remained read-only. No Azure resources were modified.

## License

The material included in this skill is provided under the [MIT License](LICENSE.txt).
