---
name: "azure-role-selector"
description: "Use when the user asks which Azure RBAC role to assign to an identity, how to grant least-privilege permissions, or how to create a custom role when no built-in role fits. Recommends the narrowest built-in role and generates the assignment as Terraform (azurerm_role_assignment), this kit's IaC. Triggers include \"which Azure role\", \"least privilege\", \"role assignment\", \"custom role definition\", and \"grant permissions\"."
---
# Azure role selector

Recommend the **least-privilege** Azure RBAC role for an identity based on the actions it needs to perform. Then express the assignment as Terraform (`azurerm_role_assignment`), this kit's IaC. Always prefer a built-in role at the narrowest scope. Create a custom role definition only when no built-in role fits.

This skill teaches how to choose and apply a role. It does not decide which identity or scope your workload needs. That comes from the team's specification and investigation.

> [!NOTE]
> This skill depends on the **Azure MCP server** (or the `az` CLI) to query role definitions and generate assignment commands. If neither is installed, report that and use the public Azure built-in roles documentation.

## When to Invoke

- "Which Azure role should I assign to this managed identity?"
- "Grant this service principal least-privilege read-only access to a storage account."
- "No built-in role fits. Help me write a custom role definition."
- "Give the application identity permission to read Key Vault secrets."

## Selection procedure

1. **Record the required actions.** List the exact operations the identity must perform (for example: read blobs, list secrets, send to a queue). Separate control-plane `actions` from data-plane `dataActions`.
2. **Choose the narrowest scope.** Assign at the smallest scope that meets the requirement: resource before resource group, resource group before subscription, and subscription before management group.
3. **Find a built-in role.** Use the Azure MCP documentation tool to find the built-in role whose `actions`/`dataActions` cover the requirement with the least excess. Prefer data-plane roles (for example, `Storage Blob Data Reader`) over broad management roles (`Contributor`).
4. **Use a custom role only if needed.** When no built-in role fits, use the Azure MCP `extension_cli_generate` tool to draft a definition listing only the required `actions`/`dataActions` and explicit `assignableScopes`.
5. **Generate the assignment.** Use the Azure MCP `extension_cli_generate` tool for the `az role assignment create` command and translate it to Terraform as the kit deliverable.
6. **Prefer a managed identity.** For service-to-service authentication, assign the role to a managed identity. Never distribute secrets, keys, or connection strings.

## Least-privilege decision table

| Situation | Choice |
|---|---|
| A built-in role exactly matches the actions | The built-in role at the narrowest scope |
| A built-in role is close but slightly broad | Prefer the built-in role unless the extra permissions are sensitive. Document the difference |
| No built-in role covers the actions | A custom role definition containing only the required actions |
| An Azure service needs to call another Azure service | A managed identity with a role assignment, never a secret |
| The identity only reads data | A data-plane `... Data Reader` role, not `Reader` or `Contributor` |

> [!WARNING]
> Never assign `Owner` or `Contributor` at subscription or management-group scope to a workload identity. These roles include `Microsoft.Authorization/*`, which allows the identity to grant itself more access.

## Bicep and ARM out of scope

A Bicep or ARM role assignment snippet (through the Azure MCP `bicepschema` and `get_bestpractices` tools) is optional and **out of scope** for this kit's deliverables. Produce Terraform. Use Bicep only for exploration or comparison.

## Output Template

Deliver the recommendation with a ready-to-commit Terraform snippet. Role assignments and definitions do not accept `tags`, so the kit's tagging rule does not apply to these resources.

```hcl
resource "azurerm_role_assignment" "app_blob_reader" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

When no built-in role fits, deliver a custom role definition along with the assignment:

```hcl
resource "azurerm_role_definition" "read_one_container" {
  name        = "SIFAP Read Single Blob Container"
  scope       = azurerm_storage_account.data.id
  description = "Least-privilege read-only access to a single blob container."

  permissions {
    actions      = ["Microsoft.Storage/storageAccounts/blobServices/containers/read"]
    data_actions = ["Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read"]
    not_actions  = []
  }

  assignable_scopes = [azurerm_storage_account.data.id]
}
```

Summarize the choice in text:

```text
Recommended role: Storage Blob Data Reader (built-in)
Scope: storage account azurerm_storage_account.data (the narrowest that works)
Principal: user-assigned managed identity app
Reason: covers the data-plane blob read action without excess; no custom role is needed.
```

## Quality Gate

- [ ] The recommended role is the narrowest built-in role covering all required actions.
- [ ] The assignment scope is the smallest that meets the requirement.
- [ ] A custom role is proposed only when no built-in role fits and lists only the required actions, with explicit `assignable_scopes`.
- [ ] The assignment is expressed as Terraform `azurerm_role_assignment` (Bicep/ARM out of scope).
- [ ] Service-to-service authentication uses a managed identity, never a secret or connection string.
- [ ] No `Owner`/`Contributor` at subscription or management-group scope for a workload identity.

## License

The material included in this skill is provided under the [MIT License](LICENSE.txt).
