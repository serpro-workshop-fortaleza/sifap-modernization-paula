---
description: "Use for general Terraform hygiene (file layout, variables, outputs, formatting, validation, tests, and state). The kit's authoritative Azure rules live in infrastructure.instructions.md."
applyTo: "**/*.tf"
---

# Terraform conventions - General hygiene

This file adds language-level Terraform hygiene to the kit's authoritative infrastructure rules. **[`infrastructure.instructions.md`](infrastructure.instructions.md) is authoritative** for this kit: Azure provider `azurerm ~> 3.x` (pinned `required_version`), required `project`/`environment`/`owner` tags, secrets only in `azurerm_key_vault_secret`, one module per Azure service area, Managed Identity, and the `terraform fmt` + `terraform validate` gate. In a conflict, infrastructure rules take precedence. The team creates `infra/` in Stages 3/4; there is no inherited stack to copy.

## File layout

Split each module by function to keep files navigable:

- `main.tf` - resources
- `variables.tf` - typed inputs
- `outputs.tf` - outputs
- `locals.tf` - computed values and repeated expressions
- `terraform.tf` - `terraform {}` block and provider requirements

Use `snake_case` for variable, local, output, and module names.

## Variables and outputs

- Every variable and output declares an explicit `type` and `description`.
- Provide defaults only for truly optional inputs; never default a secret.
- Mark secret inputs and secret-bearing outputs as `sensitive = true`; avoid exposing secrets whenever possible.
- Expose in `outputs` only what another module or consumer actually needs.

## Locals and data sources

- Move repeated expressions into `locals` (for example, the `common_tags` map) to keep values consistent.
- Use `data` sources to read existing resources instead of hardcoding IDs. Avoid data lookups for resources created in the same configuration; reference them directly.

## Idempotency

Write convergent configurations: a second `terraform apply` without input changes must report zero changes. Avoid `local-exec` / `null_resource` side effects that rerun on every apply.

## Formatting, validation, and tests

- Run `terraform fmt -recursive` and `terraform validate` per module before every commit (matches the CI infrastructure gate).
- Run `tflint` to catch provider-specific issues early.
- Write module tests with the native `*.tftest.hcl` framework, covering a positive and a negative case; keep them idempotent.

## State

Store state in a remote backend (Azure Storage) with locking; never commit a `*.tfstate` file. Treat state and fetched modules in `.terraform/` as read-only; make every change through HCL and the Terraform CLI.

## Conventions

| Rule | Rationale |
|---|---|
| One responsibility per file (`main`/`variables`/`outputs`/`locals`) | Navigable modules |
| `snake_case` names, typed and described variables | Consistent, self-explanatory HCL |
| `sensitive = true` on secret inputs and outputs | Secrets appear in neither plan output nor state |
| Clean per-module `fmt` + `validate` + `tflint` | Matches the CI infrastructure gate |
| Remote state, never versioned | No state conflicts or leaks |

## Do / Don't

| Do | Don't |
|---|---|
| Follow `infrastructure.instructions.md` for provider, tags, secrets, and modules | Reinvent the kit's Azure rules here |
| Pin versions (kit baseline: `azurerm ~> 3.x`) | Use floating `latest` providers |
| Keep state remote and read-only | Commit `*.tfstate` or edit it manually |
| Cover modules with `*.tftest.hcl` tests | Ship modules without tests |

## PR Checklist

- [ ] Files are split into `main`/`variables`/`outputs`/`locals`, with `snake_case` names
- [ ] Every variable and output has `type` and `description`; secrets are marked `sensitive`
- [ ] `terraform fmt -recursive`, per-module `validate`, and `tflint` pass locally
- [ ] Provider versions are pinned to the kit baseline (`azurerm ~> 3.x`)
- [ ] State remains in the remote backend; no `*.tfstate` is versioned
