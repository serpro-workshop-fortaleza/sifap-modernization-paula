---
name: "iac-module"
description: "Create or refactor a Terraform module for SIFAP 2.0 Azure infrastructure with standardized tags, typed variables, outputs, and validation."
argument-hint: "name=<module> service=<azurerm_resource> reqs=REQ-NNN"
agent: "devops-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /iac-module

## Objective

Produce or update **a single Terraform module** in `infra/modules/` for SIFAP 2.0, limited to one Azure service area (networking, compute, database, monitoring, or security). The module applies standard SIFAP tags to all taggable resources, keeps secrets out of code, uses Managed Identity for service-to-service authentication, and passes `terraform fmt` and `terraform validate`, as well as `tflint` and `checkov`, before committing. This matches the infrastructure gate in `.github/workflows/ci.yml`.

## When to Invoke

Use when a bounded context needs a new Azure service or when an existing module needs hardening or extension. Module changes ship in their own pull request, separate from feature code.

## Preconditions

- `.specify/memory/constitution.md` states the nonnegotiable rules (Managed Identity, Key Vault, and network access)
- The Azure service and linked `REQ-ID` are known
- The target module path (`infra/modules/<name>/`) is new or already exists for an update

## Inputs the Team Must Provide

- The module name and Azure service, for example, `database` for `azurerm_postgresql_flexible_server`
- The linked `REQ-ID` in `specs/<NNN>-<feature>/spec.md`, usually nonfunctional or operational
- Target environments (`dev`, `stage`, `prod`) and any environment-specific overrides
- Whether the change creates a new module or modifies an existing one

Ask the user for any missing item.

## What I Will Do

- Read [`../skills/iac-review/SKILL.md`](../skills/iac-review/SKILL.md) and the constitution, and follow existing module patterns
- Scaffold the module with five files and typed, documented variables
- Apply the standard SIFAP tag set to all taggable resources
- Keep secrets in `azurerm_key_vault_secret`, never in `locals`, `variables`, or `outputs`
- Use Managed Identity and private networking by default
- Add `examples/basic/` and validate locally with `fmt`, `validate`, `tflint`, and `checkov`

## What I Will NOT Do

- Invent a SKU price, region availability, or a SIFAP-specific value. Unknown inputs will be parameterized and confirmed by the team
- Create the CI/CD pipeline (`/pipeline`), write application code (`@builder`), or change requirements (`@requirements-engineer`)
- Put a secret in a variable, default value, output, or state file when avoidable
- Set `public_network_access_enabled = true` without an exception documented in `.specify/memory/constitution.md`
- Put a `provider` block in the module or apply tags to only some resources

## Output Format

A module with five files (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`), plus `examples/basic/`. The main files follow the repository's actual `azurerm` pattern:

```hcl
# infra/modules/database/versions.tf
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
    random = { source = "hashicorp/random", version = "~> 3.6" }
  }
}

# infra/modules/database/main.tf
locals {
  tags = merge(var.tags, {
    project     = "sifap"
    environment = var.environment
    owner       = var.owner
    cost-center = var.cost_center
    module      = "database"
    managed-by  = "terraform"
  })
}

resource "random_password" "admin" {
  length  = 32
  special = true
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                          = "${var.project}-${var.environment}-psql-${var.location_short}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = "16"
  administrator_login           = var.administrator_login
  administrator_password        = random_password.admin.result
  public_network_access_enabled = false # private endpoint only; no recorded exception
  tags                          = local.tags
}

# The secret stays in Key Vault, never in variables, outputs, or logs.
resource "azurerm_key_vault_secret" "admin_password" {
  name         = "${var.environment}-psql-admin-password"
  value        = random_password.admin.result
  key_vault_id = var.key_vault_id
  tags         = local.tags
}

# infra/modules/database/outputs.tf
output "server_fqdn" {
  description = "PostgreSQL FQDN for consumers; contains no secrets."
  value       = azurerm_postgresql_flexible_server.this.fqdn
}
```

Accompany the module with a validation report (output from `fmt`, `validate`, `tflint`, and `checkov`) and a one-line note about monthly cost per environment, linked to Azure pricing.

## Definition of Done

- [ ] `terraform fmt -check`, `terraform validate`, `tflint`, and `checkov` pass
- [ ] All taggable resources contain `project`, `environment`, and `owner`, plus the standard extra tags
- [ ] No secrets appear in variables, outputs, or defaults
- [ ] Public network access stays disabled unless an exception in the constitution is referenced
- [ ] Managed Identity is used and no service principal credentials appear in code
- [ ] A consumer in `examples/basic/` compiles and passes validation
- [ ] `README.md` documents inputs, outputs, an example, and the linked `REQ-ID`

## Prompt Body

You are `@devops-engineer`. The team needs a focused, reviewable module that respects the repository's Terraform rules.

**Step 1: read the constitution and skill.**
Open `.specify/memory/constitution.md` for the nonnegotiable rules and [`../skills/iac-review/SKILL.md`](../skills/iac-review/SKILL.md) for the review checklist. Review existing modules to identify patterns to follow.

**Step 2: pin the provider.**
Use `azurerm ~> 3.x`, the repository standard, pinned through `required_providers`, and consult [Azure Verified Modules](https://aka.ms/avm) when applicable.

**Step 3: scaffold the module.**
Create `main.tf` (resources only, no `provider` block), `variables.tf` (all inputs typed and documented, with `validation` blocks where ranges matter), `outputs.tf` (IDs, names, and FQDNs, never secrets), `versions.tf`, and `README.md`.

**Step 4: apply standard tags.**
Merge `var.tags` with `project`, `environment`, `owner`, `cost-center`, `module`, and `managed-by`, and attach the map to all taggable resources.

**Step 5: enforce secret, identity, and network discipline.**
Secrets flow through `azurerm_key_vault_secret` data sources or generated values stored in Key Vault, never through variables, defaults, or outputs. Use system-assigned or user-assigned managed identities for service-to-service authentication. Keep `public_network_access_enabled = false` unless the constitution grants an exception.

**Step 6: add an example and validate.**
Write `examples/basic/main.tf` to consume the module. Then run `terraform fmt -check -recursive`, `terraform init -backend=false`, `terraform validate`, `tflint --recursive`, and `checkov -d . --soft-fail false`. All commands must pass.

`terraform fmt` and `terraform validate` must pass before committing, as required by `.github/workflows/ci.yml`. All taggable resources contain the required tags. No secret may reach a variable, output, or default value. Never enable public network access without a documented exception or invent a value the team needs to confirm.

## Example Invocation

```text
/iac-module name=database service=azurerm_postgresql_flexible_server reqs=REQ-NNN
```
