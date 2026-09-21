---
name: "azure-developer-cli"
description: "Use when designing, creating, reviewing, migrating, or troubleshooting Azure Developer CLI (azd) projects according to current Microsoft guidance. Covers azd, azure.yaml, AZD templates, Terraform (or Bicep) in infra, AZD environments and secrets, hooks, deployment workflows, and azd-managed CI/CD. Triggers include \"azd\", \"azure.yaml\", \"azd environment\", \"azd pipeline\", and \"azd up\"."
---
# Azure Developer CLI best practices

Use this skill to produce maintainable, secure, environment-aware `azd` projects. Prefer repository conventions when they are already coherent and make the smallest complete change that improves the project. This skill teaches how to structure and operate an `azd` project, but does not decide the workload architecture.

> [!NOTE]
> This skill assumes the **`azd` CLI** is installed and authenticated. This kit standardizes IaC on **Terraform (`azurerm ~> 3.x`)**. Therefore, treat Terraform as the provider in `infra/` and read the Bicep guidance below only as reference.

## When to Invoke

- "Set up a new azd project for our backend and frontend services."
- "Review our azure.yaml and infra structure for issues."
- "Migrate this azd template from Bicep to Terraform."
- "Why does `azd provision` fail in our staging environment?"

## Start with repository discovery

Before editing:

1. Locate `azure.yaml`, the configured `infra.path`, source projects, deployment scripts, `.gitignore`, and pipeline definitions.
2. Read `azure.yaml` before inferring services or the IaC provider.
3. Identify whether the task is creation, migration, review, deployment, or troubleshooting.
4. Identify the active environment only when an environment-specific operation is needed.
5. Read the relevant reference:
   - Repository structure or `azure.yaml`: [references/project-structure.md](references/project-structure.md)
   - Bicep, Terraform, parameters, outputs, or environments: [references/iac-and-environments.md](references/iac-and-environments.md)
   - Secrets, hooks, CI/CD, deployment, or troubleshooting: [references/security-cicd-operations.md](references/security-cicd-operations.md)
   - Product details that may have changed: [references/official-docs.md](references/official-docs.md)

Do not assume the default `infra` path, the default Bicep provider, or a single service when `azure.yaml` indicates otherwise.

## Apply safety guardrails

- Never commit `.azure`, environment `.env` files, credentials, deployment outputs containing secrets, local Terraform state, or generated deployment artifacts.
- Never put literal secrets in `azure.yaml`, IaC parameter files, hooks, version control, command arguments that will be logged, or IaC outputs.
- Prefer managed identities and RBAC. Use Key Vault references and `azd env set-secret` when a secret is unavoidable.
- Before any command that can create, modify, or delete Azure resources, confirm the environment, subscription, tenant, region, and expected scope.
- Treat an explicit request to deploy, provision, destroy, or configure a pipeline as approval for the named action. Otherwise, ask before running `azd up`, `azd provision`, `azd deploy`, `azd down`, or `azd pipeline config`.
- Do not replace Bicep with Terraform, Terraform with Bicep, or an established hosting service unless the user requests that architectural change.
- Preserve resources and state owned outside the current `azd` project.

## Use these defaults

| Concern | Preferred default |
| --- | --- |
| Project manifest | One `azure.yaml` at the repository root |
| Application code | `src/<service-name>` for each independently deployable service |
| Infrastructure | `infra` with a thin entry point and reusable modules |
| IaC provider | Terraform in this kit; otherwise Bicep unless the repository or user chooses Terraform |
| Deployment environments | Separate named environments for development, test, staging, and production |
| Local AZD state | `.azure/<environment-name>`, excluded from version control |
| Shared environment state | Remote AZD environments backed by Azure Blob Storage |
| Secrets | Managed identity/RBAC first; then Key Vault references |
| Automation scripts | Short, idempotent scripts in `scripts/azd` |
| CI authentication | Workload identity federation/OIDC where supported |
| Routine development | `azd up` for simple workflows; separate phases for controlled workflows |

## Implementation workflow

### 1. Model the application

- Define one entry in `services` for each independently deployable component.
- Keep service keys stable because they participate in resource discovery and deployment.
- Map each service to its actual `project`, `language`, and `host` values.
- Keep shared infrastructure in IaC instead of inventing a dummy deployable service.
- Declare dependencies with supported `azure.yaml` fields instead of relying on file order.

### 2. Model the infrastructure

- Keep `main.bicep` or `main.tf` as the orchestration entry point.
- Split reusable or independently understandable infrastructure into modules.
- Parameterize environment-specific values. Do not fork the IaC tree per environment.
- Output only stable, non-secret values required by deployment or application configuration.
- Use deterministic names and consistent tags that include the project and environment.
- Add role assignments to identities instead of distributing service keys.
- Use infrastructure layers only when separate scopes or lifecycle dependencies justify them.

### 3. Model the environments

- Use predictable names, such as `<project>-dev` for shared environments and `<alias>-dev` for personal environments.
- Use `azd env set`, `azd env unset`, and `azd env set-secret` instead of editing `.env` directly.
- Use `-e` or `--environment` in scripts and automation to make the target explicit.
- Use `azd env refresh` to synchronize deployment outputs after another actor changes an environment.
- Configure remote AZD state when a team shares environment state.

### 4. Add hooks only for lifecycle gaps

- Prefer declarative IaC and native service configuration over hooks.
- Use root hooks for project-wide behavior and service hooks for service-specific behavior.
- Keep non-trivial hook logic in versioned scripts in `scripts/azd`.
- Set `shell` explicitly. Provide `windows` and `posix` variants when needed.
- Make hooks idempotent, non-interactive in CI, and fail on errors unless failure is intentionally non-blocking.
- Test a hook independently with `azd hooks run <hook-name>`.

### 5. Build CI/CD intentionally

- Keep the pipeline definition with the template and review changes generated by `azd pipeline config`.
- Use short-lived federated credentials when supported by the provider.
- Run tests and IaC validation before provisioning.
- Use explicit environments and `--no-prompt` in automation.
- Add protected production environments and approval gates.
- For Terraform, configure protected remote state before the pipeline and account for current AZD authentication limitations.

## Validate before completion

Run only the checks applicable to the repository:

```text
Application: existing formatter, lint, type checking, build, and tests
Bicep:      az bicep build --file infra/main.bicep
Terraform:  terraform fmt -check -recursive
            terraform init -backend=false
            terraform validate
AZD hooks: azd hooks run <hook-name>
Packaging: azd package
```

For a Bicep what-if or a Terraform plan, choose the correct deployment scope and environment. These checks may authenticate to Azure or read remote state. Therefore, follow the safety guardrails.

Verify that:

- `azure.yaml` paths exist and service settings match the source projects.
- The IaC entry point and provider agree with `azure.yaml`.
- Required deployment outputs match variables consumed by services, hooks, and pipelines.
- `.gitignore` excludes `.azure`, secrets, local state, and generated artifacts.
- No secrets appear in tracked content or command output.
- Documentation explains prerequisites, environment creation, deployment, verification, and cleanup.

## Report the outcome

Report:

- Changed files and behaviors.
- The IaC provider and environment assumptions.
- Checks performed.
- Any cloud-mutating command intentionally not run.
- Any beta or preview feature the solution depends on.

Do not claim deployment success unless the target environment was actually deployed and verified.

## Output Template

Report the change in a short status block:

```text
azd project review: sifap-modern
Changed: azure.yaml (web service added), infra/main.tf (storage module added)
IaC provider: Terraform (azurerm ~> 3.x); environment: sifap-dev
Checks run: terraform fmt -check, terraform validate, azd package
Not run: azd provision (would change Azure); requires explicit approval
Preview features: none
```

## Quality Gate

- [ ] Service paths in `azure.yaml` exist and settings match the source projects.
- [ ] The IaC entry point and provider agree with `azure.yaml` (Terraform in this kit).
- [ ] Required deployment outputs match variables consumed by services, hooks, and pipelines.
- [ ] `.gitignore` excludes `.azure`, secrets, local state, and generated artifacts.
- [ ] No secrets appear in tracked content or command output; secrets use managed identity or Key Vault references.
- [ ] Applicable checks pass (`terraform fmt -check`, `terraform validate`, the project's formatter, lint, and tests).
- [ ] No cloud-mutating command was run without explicit approval, and success is claimed only after actual verification.
