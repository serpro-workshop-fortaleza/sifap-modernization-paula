# Project structure and `azure.yaml`

## Recommended repository structure

Use this as a default, not as a reason to reorganize a repository that is already coherent:

```text
.
|-- .azure/                         # Generated local AZD environment state; ignored
|-- .devcontainer/                  # Optional reproducible development environment
|-- .github/
|   |-- workflows/
|       |-- azure-dev.yml           # Optional GitHub Actions pipeline
|-- infra/
|   |-- main.bicep                  # Bicep orchestration entry point
|   |-- main.parameters.json        # AZD environment-to-Bicep parameter mapping
|   |-- modules/
|       |-- core/                   # Shared platform resources
|       |-- app/                    # Application-specific resources
|-- scripts/
|   |-- azd/                        # Hook and deployment helper scripts
|-- src/
|   |-- api/                        # Independently deployable service
|   |-- web/                        # Independently deployable service
|-- tests/
|-- .gitignore
|-- azure.yaml
|-- README.md
```

For Terraform, use a conventional structure in `infra`:

```text
infra/
|-- main.tf
|-- providers.tf
|-- variables.tf
|-- outputs.tf
|-- provider.conf.json              # AZD remote backend configuration, when used
|-- modules/
```

### Structure rules

- Put `azure.yaml` at the project root.
- Keep application source code independent of deployment assets.
- Keep the IaC entry point thin and move resource details into modules.
- Organize modules by responsibility or lifecycle, not an arbitrary file per resource.
- Keep hook scripts outside `infra` unless a script belongs exclusively to an infrastructure layer.
- Avoid versioning environment-specific source trees such as `infra/dev`, `infra/test`, and `infra/prod`. Use parameters.
- Keep tests according to normal language conventions. Do not move them just to fit this example.
- Include `.devcontainer` only when it is maintained and tested.

## Basic `azure.yaml` structure

Add the schema directive for editor validation:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
name: sample-app

infra:
  provider: bicep
  path: ./infra
  module: main

services:
  api:
    project: ./src/api
    language: ts
    host: appservice
  web:
    project: ./src/web
    dist: dist
    language: ts
    host: staticwebapp
```

The explicit `infra` block is useful when clarity matters, although Bicep, `infra`, and `main` are the defaults.

## Manifest design checklist

### Top-level configuration

- `name` uses lowercase letters, starts and ends with an alphanumeric character, and contains only alphanumeric characters and hyphens.
- `metadata.template` identifies the source template and version when the repository is distributed as a template.
- `infra.provider`, `infra.path`, and `infra.module` match the actual repository.
- `requiredVersions` is used when the project depends on a minimum AZD or extension version.
- `workflows` overrides defaults only when deployment order truly requires it.
- `state.remote` is configured at project scope when teams share AZD environments.

### Services

- A service represents deployable application code, not a database, Key Vault, or other shared resource.
- Service names are short, meaningful, and stable.
- `project` points to the service root and uses a relative path.
- `language`, `host`, `dist`, container, and remote build settings match how the service is built.
- An Azure Container Apps service uses either `project` or `image`, never both.
- `resourceName` is set only when default AZD discovery through the `azd-service-name` tag is unavailable or intentionally bypassed.
- Dependencies use supported `uses` relationships instead of implicit assumptions.
- Environment variables use substitutions or IaC outputs instead of hardcoded environment values.

### Resources and infrastructure

- Shared Azure resources remain in IaC.
- Service modules and AZD service names stay aligned to make resource discovery predictable.
- Custom resource group names include environment identity and comply with Azure naming constraints.
- Infrastructure layers are reserved for independently provisioned units, different scopes, or hook-mediated dependencies.
- Cross-layer dependencies are explicit with `dependsOn` when AZD cannot infer them.

### Pipelines and hooks

- `pipeline.variables` contains non-secret settings.
- `pipeline.secrets` is used only when the pipeline needs to store the resolved value rather than a Key Vault reference.
- Root hooks handle project-wide work; service hooks handle one service.
- Hook scripts use explicit shells and portable paths.
- Hooks do not duplicate application tests or declarative IaC behavior.

## README requirements for a reusable AZD project

Document:

1. Architecture and services deployed to Azure.
2. Local prerequisites, including AZD and provider-specific tools.
3. Authentication requirements.
4. How to create or select an environment.
5. Required non-secret variables and how to set them.
6. How to supply secrets without exposing their values.
7. How to run, test, provision, deploy, monitor, and troubleshoot.
8. Resources expected to incur costs.
9. How to clean up safely.
10. Beta or preview dependencies, including Terraform or pipeline features where applicable.

Do not put real subscription IDs, tenant IDs, secret names that reveal sensitive systems, or production endpoints in reusable documentation.
