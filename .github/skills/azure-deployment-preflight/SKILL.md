---
name: "azure-deployment-preflight"
description: "Use before deploying Bicep/ARM to Azure to validate template syntax, run what-if analysis, and check permissions. Trigger when users mention Azure deployment, Bicep file validation, deployment permission checks, infrastructure change previews, running what-if, or preparing for azd provision. Triggers include \"preflight\", \"what-if\", \"validate deployment\", \"azd provision --preview\", and \"deployment permissions\"."
---
# Azure deployment preflight validation

This skill validates Bicep deployments before execution and supports both Azure CLI (`az`) and Azure Developer CLI (`azd`) workflows.

> **Kit scope:** this kit's IaC uses **Terraform (Azure provider `~> 3.x`)**. Bicep/ARM are **out of scope** for kit deliverables. Use this preflight validation only when a project actually uses Bicep/ARM. For Terraform, use `terraform validate`/`terraform plan` and the `terraform-azurerm-set-diff-analyzer` skill.

## When to Invoke

- "Validate my Bicep deployment before running it."
- "Preview the changes that `azd provision` will make."
- "Check whether I have permission to deploy this template."
- "Run what-if on my infrastructure before deployment."

Typical occasions: before deploying infrastructure to Azure; while preparing or reviewing Bicep files; to preview deployment changes; to check whether permissions are sufficient; or before running `azd up`, `azd provision`, or `az deployment`.

## Validation process

Follow these steps in order. Continue to the next step even if a previous one fails, and record all issues in the final report.

### Step 1: detect the project type

Determine the deployment workflow by checking the project indicators:

1. **Check for an azd project**: look for `azure.yaml` in the project root. If found, use the **azd workflow**; otherwise, use the **az CLI workflow**.
2. **Locate Bicep files**: find all `.bicep` files that need validation. For azd projects, check `infra/` first, then the project root. For standalone projects, use the specified file or search common locations (`infra/`, `deploy/`, and the project root).
3. **Automatically detect parameter files**: for each Bicep file, look for `<filename>.bicepparam` (Bicep parameters, preferred), `<filename>.parameters.json` (JSON parameters), or `parameters.json` or `parameters/<env>.json` in the same directory.

### Step 2: validate Bicep syntax

Run the Bicep CLI to check template syntax before attempting deployment validation:

```bash
bicep build <bicep-file> --stdout
```

**What to record:**

- Syntax errors with line/column numbers
- Warning messages
- Build success/failure status

**If the Bicep CLI is not installed:**

- Record the issue in the report
- Continue to Step 3 (Azure will validate syntax during what-if)

### Step 3: run preflight validation

Choose the appropriate validation based on the project type detected in Step 1.

#### For azd projects (azure.yaml exists)

Use `azd provision --preview` to validate the deployment:

```bash
azd provision --preview
```

If an environment is specified or multiple environments exist:

```bash
azd provision --preview --environment <env-name>
```

#### For standalone Bicep (no azure.yaml)

Determine the deployment scope from the Bicep file's `targetScope` declaration:

| Target scope | Command |
|--------------|---------|
| `resourceGroup` (default) | `az deployment group what-if` |
| `subscription` | `az deployment sub what-if` |
| `managementGroup` | `az deployment mg what-if` |
| `tenant` | `az deployment tenant what-if` |

**Run with the Provider validation level first.**

Resource group scope (most common):

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

Subscription scope:

```bash
az deployment sub what-if \
  --location <location> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

Management group scope:

```bash
az deployment mg what-if \
  --location <location> \
  --management-group-id <mg-id> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

Tenant scope (`tenant`):

```bash
az deployment tenant what-if \
  --location <location> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

**Fallback strategy:**

If `--validation-level Provider` fails with permission errors (RBAC), retry with `ProviderNoRbac`:

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  --validation-level ProviderNoRbac
```

Record the fallback in the report. The user may not have full deployment permissions.

### Step 4: record what-if results

Analyze the what-if output to categorize resource changes:

| Change type | Symbol | Meaning |
|-------------|--------|---------|
| Create | `+` | A new resource will be created |
| Delete | `-` | The resource will be deleted |
| Modify | `~` | Resource properties will change |
| NoChange | `=` | The resource will not change |
| Ignore | `*` | The resource was not analyzed (limits reached) |
| Deploy | `!` | The resource will be deployed (changes unknown) |

For modified resources, record the specific property changes.

### Step 5: generate the report

Create a Markdown report file in the **project root** named:

- `preflight-report.md`

Use the template structure in [references/REPORT-TEMPLATE.md](references/REPORT-TEMPLATE.md).

**Report sections:**

1. **Summary**: overall status, timestamp, validated files, and target scope
2. **Tools executed**: commands executed, versions, and validation levels used
3. **Issues**: all errors and warnings with severity and remediation
4. **What-if results**: resources to be created/modified/deleted or left unchanged
5. **Recommendations**: actionable next steps

## Required information

Before running validation, obtain:

| Information | Required for | How to obtain |
|-------------|--------------|---------------|
| Resource group | `az deployment group` | Ask the user or check the existing configuration in `.azure/` |
| Subscription | All deployments | Run `az account show` or ask the user |
| Location | Subscription/management group/tenant scope | Ask the user or use the configured default |
| Environment | azd projects | Run `azd env list` or ask the user |

If any required information is missing, request it before proceeding.

## Error handling

See [references/ERROR-HANDLING.md](references/ERROR-HANDLING.md) for detailed error handling guidance.

**Core principle:** continue validation even when errors occur. Record all issues in the final report.

| Error type | Action |
|------------|--------|
| Not authenticated | Record in the report and suggest `az login` or `azd auth login` |
| Permission denied | Fall back to `ProviderNoRbac` and record in the report |
| Bicep syntax error | Include all errors and continue with the other files |
| Tool not installed | Record in the report and skip that validation step |
| Resource group not found | Record in the report and suggest creating it |

## Tool requirements

This skill uses the following tools:

- **Azure CLI** (`az`): version 2.76.0+ recommended for `--validation-level`
- **Azure Developer CLI** (`azd`): for projects with `azure.yaml`
- **Bicep CLI** (`bicep`): for syntax validation
- **Azure MCP tools**: to look up documentation and best practices

Check tool availability before starting:

```bash
az --version
azd version
bicep --version
```

## Example workflow

1. User: "Validate my Bicep deployment before running it"
2. The agent detects `azure.yaml`, indicating an azd project
3. The agent finds `infra/main.bicep` and `infra/main.bicepparam`
4. The agent runs `bicep build infra/main.bicep --stdout`
5. The agent runs `azd provision --preview`
6. The agent generates `preflight-report.md` in the project root
7. The agent summarizes the findings for the user

## Output Template

The skill writes `preflight-report.md` in the project root, following [references/REPORT-TEMPLATE.md](references/REPORT-TEMPLATE.md). Below the top-level title `Preflight report`, it contains:

```markdown
## Summary

- Status: PASSED with warnings
- Timestamp: 2026-08-17T14:00:00Z
- Validated files: infra/main.bicep
- Target scope: resourceGroup (rg-sifap)

## Tools executed

| Tool | Version | Result |
|---|---|---|
| bicep build | 0.30.3 | success |
| az deployment group what-if | 2.76.0 (Provider) | success |

## Issues

| Severity | Location | Finding | Remediation |
|---|---|---|---|
| Warning | main.bicep:42 | Storage allows public blob access | Set allowBlobPublicAccess to false |

## What-if results

| Change | Count | Resources |
|---|---|---|
| Create (+) | 3 | storageAccount, appService, keyVault |
| Modify (~) | 1 | appServicePlan (B1 -> S1) |
| Delete (-) | 0 | none |

## Recommendations

- Resolve the public access warning before deployment.
- Run again with `--validation-level Provider` after RBAC permissions are granted.
```

## Quality Gate

- [ ] The project type was detected (azd versus standalone) and all `.bicep` files were located.
- [ ] Bicep syntax was validated with `bicep build`, or the missing tool was recorded in the report.
- [ ] What-if ran at the correct scope; any RBAC failure triggered a fallback to `ProviderNoRbac` and was recorded.
- [ ] All create/modify/delete changes were categorized, with details of modified properties.
- [ ] `preflight-report.md` was written in the project root with all five sections completed.
- [ ] Validation continued through all steps and recorded all issues instead of stopping at the first error.

## References

- [Validation command reference](references/VALIDATION-COMMANDS.md)
- [Report template](references/REPORT-TEMPLATE.md)
- [Error handling guide](references/ERROR-HANDLING.md)
