---
description: "Use when creating or reviewing infrastructure as code, Terraform, Bicep, Azure resource definitions, and environment configuration."
applyTo: "infra/**,**/*.tf,**/*.bicep,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml"
---

# Infrastructure conventions - Terraform and Compose

This file activates when you edit files in `infra/`, any `*.tf` or `*.bicep`, or a `compose`/`docker-compose` YAML file. It teaches Azure provisioning with Terraform (`azurerm ~> 3.x`, the primary tool) and safe local Compose parity. Prefer Terraform; use Bicep only when a module truly requires it. The team creates `infra/` in Stages 3/4; there is no inherited stack to copy.

## Provider and versions

Pin the provider and minimum Terraform version. Keep one `provider "azurerm"` block per configuration.

```hcl
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

## Module layout

Use one module per Azure service area to keep blast radius and ownership clear.

```text
infra/
├── networking/   # VNet, subnets, NSGs
├── compute/      # App Service / Container Apps
├── database/     # PostgreSQL Flexible Server
└── monitoring/   # Log Analytics, alerts
```

## Required tags on all resources

Every resource has `project`, `environment`, and `owner` (add `cost-center` when the team tracks it). Define them once in `locals` and apply them.

```hcl
locals {
  common_tags = {
    project     = var.project
    environment = var.environment
    owner       = var.owner
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg-${var.location_short}"
  location = var.location
  tags     = local.common_tags
}
```

## Secrets

> [!WARNING]
> Secrets belong only in `azurerm_key_vault_secret`, never in `locals`, `variables` defaults, `.tfvars`, or versioned state. Mark secret inputs with `sensitive = true` and inject them through the pipeline's OIDC session.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = var.db_password
  key_vault_id = azurerm_key_vault.main.id
  tags         = local.common_tags
}
```

## Managed Identity

Service-to-service authentication uses Managed Identity (`azurerm_user_assigned_identity` or system-assigned identity), not connection strings with embedded passwords. Assign the identity and grant Key Vault access through a role assignment.

## Naming convention

Resource names follow `{project}-{env}-{resource}-{region}`.

| Resource | Example |
|---|---|
| Resource group | `sifap-prod-rg-brs` |
| PostgreSQL server | `sifap-prod-psql-brs` |

## Formatting and validation gate

CI runs `terraform fmt -check -recursive` and, in each module, `terraform init -backend=false` followed by `terraform validate` (see [`ci.yml`](../workflows/ci.yml)). Before pushing, run `terraform fmt -recursive` and `terraform -chdir=<module> validate` locally. The [`iac-review`](../skills/iac-review/SKILL.md) skill owns drift detection and in-depth module review.

## Docker Compose parity

Compose is for local development only. Pin images by digest, keep secrets in a Git-ignored `.env`, and never commit real credentials.

```yaml
services:
  db:
    image: postgres:16@sha256:<digest> # pin the digest
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD} # from .env, never hardcoded
```

## Conventions

| Rule | Rationale |
|---|---|
| `azurerm ~> 3.x`, pinned `required_version` | Reproducible plans across machines |
| One module per service area | Clear ownership and small blast radius |
| `project` + `environment` + `owner` tags on all resources | Cost tracking, auditing, and cleanup |
| Secrets only in `azurerm_key_vault_secret` | No credentials in code or state |
| Managed Identity for service authentication | No stored passwords between services |
| Clean `fmt` + `validate` per module | Matches the CI infrastructure gate |

## Do / Don't

| Do | Don't |
|---|---|
| Apply `local.common_tags` to every resource | Ship an untagged resource |
| Mark secret variables with `sensitive = true` | Put a secret in a `variable` default or `.tfvars` |
| Pin Compose images by digest | Use `postgres:latest` |
| Authenticate through Managed Identity | Embed a password in a connection string |

## PR Checklist

- [ ] The provider is `azurerm ~> 3.x`, with pinned `required_version`
- [ ] Every resource has `project`, `environment`, and `owner` tags
- [ ] No secret appears outside `azurerm_key_vault_secret`; secret variables are `sensitive`
- [ ] Service-to-service authentication uses Managed Identity
- [ ] `terraform fmt -check -recursive` and per-module `validate` pass locally
- [ ] Compose files pin image digests and read secrets from a Git-ignored `.env`
