# Security, hooks, CI/CD, and operations

## Identity and secret handling

Use this order of preference:

1. Managed identity with least-privilege RBAC.
2. Workload identity federation for CI/CD.
3. Key Vault reference through `azd env set-secret`.
4. Short-lived secret material only when no identity-based option exists.

Never:

- Store a plaintext secret in `.azure/<environment>/.env`.
- Commit environment files, credentials, certificates, or Terraform state.
- Put secrets in IaC outputs.
- Print environment values indiscriminately in hooks or pipelines.
- Pass a secret directly on the command line when the shell or CI system could log it.
- Grant broad subscription roles when resource group or resource scope is sufficient.

`azd env set-secret <name>` stores a Key Vault reference in the AZD environment. Resolve it only where needed:

- Map it to a Bicep `@secure()` parameter.
- Use a hook `secrets` mapping for a hook process.
- Choose between a pipeline variable containing the Key Vault reference or a pipeline secret containing the resolved value.

Prefer the reference approach when the pipeline identity can read Key Vault, because rotation will not require republishing a resolved pipeline secret.

## Hooks

Use hooks for validation, generated runtime configuration, data preparation, smoke checks, or lifecycle coordination that IaC and native AZD behavior cannot express.

### Hook rules

- Prefer external scripts over long inline commands.
- Store scripts in `scripts/azd`.
- Set `shell: sh` or `shell: pwsh` explicitly.
- Provide `windows` and `posix` implementations when syntax differs.
- Use paths relative to the hook's documented working directory.
- Make scripts idempotent and safe to rerun.
- Keep `continueOnError` false unless the operation is observability-only or truly optional.
- Use non-interactive behavior in CI.
- Do not install unpinned dependencies on every run when reproducible setup can do it once.
- Do not log secret values or all environment variables.
- Test with `azd hooks run <hook-name>` before coupling the hook to a full deployment.

Example:

```yaml
hooks:
  preprovision:
    windows:
      shell: pwsh
      run: ./scripts/azd/validate.ps1
      interactive: false
      continueOnError: false
    posix:
      shell: sh
      run: ./scripts/azd/validate.sh
      interactive: false
      continueOnError: false
```

Use root hooks for the whole project. Put service-specific hooks in that service's entry in `azure.yaml`.

## Deployment workflow

The normal AZD lifecycle is:

1. Package application artifacts.
2. Provision or update infrastructure.
3. Deploy application artifacts.

`azd up` is the convenient combined workflow and is suitable for routine development and simple deployments.

Use separate commands when:

- Infrastructure review or approval must happen before deployment.
- The application is frequently redeployed without infrastructure changes.
- Troubleshooting requires isolating packaging, provisioning, or deployment failures.
- A complex dependency requires a custom order.

```text
azd package
azd provision -e <environment>
azd deploy -e <environment>
```

Customize `workflows.up.steps` only when a real dependency requires a different order, such as provisioning before a build that needs a generated endpoint. Do not customize the workflow just to reproduce pipeline naming conventions.

## End-to-end and multi-service dependencies

- Map service dependencies before implementation.
- Let Bicep or Terraform handle one-way infrastructure dependencies.
- Use provisioning outputs for endpoints and names needed during deployment.
- Use runtime configuration, such as Azure App Configuration or a generated configuration file, when settings must change without rebuilding.
- Avoid circular build-time dependencies between frontend and backend services.
- Use hooks or a custom workflow only when outputs and runtime configuration cannot resolve the dependency.
- Test the strategy separately in development, test, and production-like environments.

## CI/CD

### Pipeline design

A robust pipeline separates:

1. Application formatting, lint, build, and tests.
2. IaC formatting and static validation.
3. What-if or plan review at the correct scope.
4. Provisioning with an explicit AZD environment.
5. Deployment.
6. Smoke or health checks.
7. Production approval and rollback/cleanup procedures.

Use:

- `--no-prompt` in automation.
- A fixed `-e` or `--environment`.
- Protected environments and required reviewers for production.
- Concurrency controls to prevent simultaneous writes to an environment.
- Least-privilege identities scoped to the target environment.
- Pinned action and tool versions with a managed update process.

### `azd pipeline config`

Current Microsoft documentation classifies `azd pipeline config` as beta. Before running it:

- Review the pipeline definition included in the template.
- Confirm the repository, organization, environment, subscription, and authentication mode.
- Expect repository, identity, variable, secret, commit, push, and pipeline side effects.
- Review the generated workflow and permission changes before production use.
- Rerun it when `pipeline.variables` or `pipeline.secrets` changes.

For GitHub Actions, AZD configures OIDC/federated credentials by default in supported scenarios. Current documentation states that AZD's Terraform pipeline does not support OIDC. Therefore, explicitly evaluate the authentication trade-off instead of silently falling back to a long-lived credential.

For Terraform, configure protected remote state before the pipeline.

## Validation and preview

Run local checks before commands that change Azure:

### Bicep

```text
az bicep build --file infra/main.bicep
```

Use an Azure deployment what-if at the scope declared by the template. Do not assume resource group scope.

### Terraform

```text
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
```

Use `terraform plan` only after confirming the backend, workspace/state key, variables, and Azure identity.

### AZD and application

- Run existing application checks.
- Run relevant hooks independently.
- Run `azd package` to verify service paths and packaging.
- Confirm that IaC outputs match variables consumed during deployment.
- Check the environment name before provisioning, deploying, or deleting.

## Troubleshooting sequence

1. Identify whether the failure occurs in packaging, provisioning, deployment, a hook, authentication, or resource discovery.
2. Rerun the smallest failing phase instead of `azd up`.
3. Check the selected environment and expected subscription, tenant, and region.
4. Check paths, provider, service names, host types, and resource discovery tags in `azure.yaml`.
5. Refresh environment outputs with `azd env refresh` when Azure state changes elsewhere.
6. For Terraform, check both AZD and Azure CLI authentication, as well as the correct remote state.
7. For hooks, run the hook directly and check the shell, working directory, and environment dependencies.
8. Use debug logs only when needed and redact sensitive values before sharing them.

## Cleanup

- Confirm the exact environment before `azd down`.
- Explain that cleanup can delete resources containing data.
- Preserve shared or externally owned resources.
- For ephemeral environments, automate cleanup and include a fallback for failed pipeline runs.
- Verify deletion instead of assuming command success.
