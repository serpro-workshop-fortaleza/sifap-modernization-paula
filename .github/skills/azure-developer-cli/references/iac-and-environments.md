# Infrastructure as code and environments

## Choose the provider intentionally

### Bicep

Use Bicep when:

- The project uses only Azure.
- Native Azure resource coverage and immediate API support matter.
- The team wants a stateless deployment model.
- Azure Verified Modules covers common resource patterns.

Bicep is AZD's default IaC provider.

### Terraform

Use Terraform when:

- The repository already uses Terraform.
- The team has established Terraform module, state, policy, and review practices.
- Cross-provider infrastructure is a real requirement.

Current Microsoft documentation classifies AZD's Terraform support as beta. Make this constraint visible and do not migrate a project to Terraform just for familiarity.

## Bicep structure

Keep `main.bicep` as the orchestration layer:

```text
infra/
|-- main.bicep
|-- main.parameters.json
|-- modules/
|   |-- core/
|   |-- data/
|   |-- identity/
|   |-- observability/
|   |-- services/
```

### Bicep practices

- Declare the deployment `targetScope` intentionally.
- Use modules for cohesive capabilities and repeated patterns.
- Prefer Azure Verified Modules when they meet the requirement and the team accepts their versioning model.
- Pin module versions and review updates instead of letting them float automatically.
- Add descriptions and validation decorators to parameters.
- Pass parameters through modules instead of reading AZD environment variables inside each module.
- Use deterministic names that respect each resource type's length and character constraints.
- Use `uniqueString` with stable scope inputs when global uniqueness is required.
- Apply consistent project, environment, owner, and cost tags where policy permits.
- Use managed identities and narrowly scoped role assignments.
- Avoid keys and connection strings when identity-based access is available.
- Output the resource IDs, names, and endpoints required by later phases.
- Never output secret values. Deployment outputs are copied to the AZD environment.

### Parameter flow

Use `main.parameters.json` to map AZD environment values to Bicep:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "value": "${AZURE_ENV_NAME}"
    },
    "location": {
      "value": "${AZURE_LOCATION}"
    }
  }
}
```

Match these values in the entry point:

```bicep
@description('Stable name of the AZD deployment environment.')
@minLength(1)
param environmentName string

@description('Primary Azure region for this deployment.')
param location string
```

Use outputs as a contract between provisioning and later AZD phases:

```bicep
output SERVICE_API_ENDPOINT_URL string = api.outputs.endpoint
```

Choose stable output names because services, hooks, and pipelines may consume them as environment variables.

When using AZD environment secrets with Bicep:

- Mark the Bicep input with `@secure()`.
- Map the AZD secret reference through `main.parameters.json`.
- Do not output the secure value.
- Note that current AZD documentation states that `.bicepparam` files do not support environment secrets.

## Terraform structure and state

### Terraform practices

- Set `infra.provider: terraform` explicitly in `azure.yaml`.
- Keep all AZD-managed `.tf` files in the configured infrastructure path.
- Pin Terraform and provider versions and commit the dependency lock file.
- Use modules with clear inputs and outputs.
- Mark sensitive variables and outputs as `sensitive`, but remember that sensitive values may still exist in state.
- Do not commit `.tfstate`, plan files, crash logs, or provider credentials.
- Avoid splitting ownership of the same Azure resource between AZD and an unrelated Terraform root module.

### Authentication

The Azure provider for Terraform uses Azure CLI authentication by default and does not use AZD's credential cache. Prefer the documented single-authentication configuration:

```text
azd config set auth.useAzCliAuth true
az login
```

Otherwise, both `azd auth login` and `az login` are required.

### Remote state

Configure a protected remote backend before `azd pipeline config` or collaborative deployments:

- Use a dedicated storage account and private container where appropriate.
- Restrict access with RBAC and network controls.
- Enable platform protections such as versioning, soft delete, and resource locks according to organizational policy.
- Use a different state key for each project and environment.
- Treat state as sensitive data.
- Do not store backend access keys in version control.

AZD reads Terraform backend settings from `infra/provider.conf.json` when configured according to the official Terraform integration.

## Environment strategy

AZD stores local environment state in:

```text
.azure/
|-- config.json
|-- <environment-name>/
    |-- .env
    |-- config.json
```

The entire `.azure` directory must remain outside version control.

### Naming

Use names that make ownership and lifecycle clear:

- Shared: `<project>-dev`, `<project>-test`, `<project>-prod`
- Personal: `<alias>-<purpose>` or `<alias>-dev`
- Ephemeral: `<project>-pr-<number>` when automation also guarantees cleanup

Keep the name short enough to accommodate resources with restrictive naming limits.

### Management

Use AZD commands instead of editing files manually:

```text
azd env new <name>
azd env list
azd env select <name>
azd env set <key> <value>
azd env get-value <key>
azd env unset <key>
azd env refresh
```

In automation and potentially destructive operations, set the environment explicitly:

```text
azd provision -e <environment> --no-prompt
azd deploy -e <environment> --no-prompt
```

### Configuration rules

- Keep one IaC codebase and vary behavior through parameters.
- Keep non-secret defaults in reviewed configuration or IaC, not in committed `.azure` files.
- Use `azd env set` for deployment-specific non-secret settings.
- Let IaC outputs populate computed resource names and endpoints.
- Avoid environment-name conditionals scattered across modules. Prefer explicit feature or SKU parameters.
- Use `azd env refresh` after another actor changes deployment outputs.
- Do not assume the currently selected environment in scripts.

## Shared and remote environments

Configure `state.remote` when team members or automation need a shared AZD environment:

```yaml
state:
  remote:
    backend: AzureBlobStorage
    config:
      accountName: <storage-account-name>
      containerName: <project-container-name>
```

AZD remote state synchronizes `.env` and AZD's `config.json`. It is separate from Terraform remote state. A Terraform project with AZD collaboration may require both:

- AZD remote state for environment configuration.
- Terraform remote state for managed infrastructure state.

Protect both stores with least-privilege RBAC and appropriate data protection settings.
