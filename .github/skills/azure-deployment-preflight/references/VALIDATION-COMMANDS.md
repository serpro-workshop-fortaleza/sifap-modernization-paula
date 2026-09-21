# Validation command reference

This reference documents all commands used in Azure preflight validation.

## Azure Developer CLI (azd)

### azd provision --preview

Previews infrastructure changes for azd projects without deploying them.

```bash
azd provision --preview [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--environment`, `-e` | Environment name to use |
| `--no-prompt` | Accepts defaults without prompting |
| `--debug` | Enables debug logging |
| `--cwd` | Sets the working directory |

**Examples:**

```bash
# Preview with the default environment
azd provision --preview

# Preview a specific environment
azd provision --preview --environment dev

# Preview without prompts (CI/CD)
azd provision --preview --no-prompt
```

**Output:** shows resources that will be created, modified, or deleted.

### azd auth login

Authenticates with Azure for azd operations.

```bash
azd auth login [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--check-status` | Checks authentication status without signing in |
| `--use-device-code` | Uses the device code flow |
| `--tenant-id` | Specifies the tenant |
| `--client-id` | Service principal client ID |

### azd env list

Lists available environments.

```bash
azd env list
```

---

## Azure CLI (az)

### az deployment group what-if

Previews changes for resource group deployments.

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  [options]
```

**Required parameters:**

| Parameter | Description |
|-----------|-------------|
| `--resource-group`, `-g` | Target resource group name |
| `--template-file`, `-f` | Bicep file path |

**Optional parameters:**

| Parameter | Description |
|-----------|-------------|
| `--parameters`, `-p` | Parameter file or inline values |
| `--validation-level` | `Provider` (default), `ProviderNoRbac`, or `Template` |
| `--result-format` | `FullResourcePayloads` (default) or `ResourceIdOnly` |
| `--no-pretty-print` | Outputs raw JSON for parsing |
| `--name`, `-n` | Deployment name |
| `--exclude-change-types` | Excludes specific change types from the output |

**Validation levels:**

| Level | Description | Use case |
|-------|-------------|----------|
| `Provider` | Full validation with RBAC checks | Default, most comprehensive |
| `ProviderNoRbac` | Full validation with read-only permissions | When deployment permissions are missing |
| `Template` | Static syntax validation only | Quick syntax check |

**Examples:**

```bash
# Basic what-if
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep

# With parameters and full validation
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --validation-level Provider

# Fallback without RBAC checks
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --validation-level ProviderNoRbac

# JSON output for parsing
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --no-pretty-print
```

### az deployment sub what-if

Previews changes for subscription-level deployments.

```bash
az deployment sub what-if \
  --location <location> \
  --template-file <bicep-file> \
  [options]
```

**Required parameters:**

| Parameter | Description |
|-----------|-------------|
| `--location`, `-l` | Deployment metadata location |
| `--template-file`, `-f` | Bicep file path |

**Examples:**

```bash
az deployment sub what-if \
  --location eastus \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --validation-level Provider
```

### az deployment mg what-if

Previews changes for management group deployments.

```bash
az deployment mg what-if \
  --location <location> \
  --management-group-id <mg-id> \
  --template-file <bicep-file> \
  [options]
```

**Required parameters:**

| Parameter | Description |
|-----------|-------------|
| `--location`, `-l` | Deployment metadata location |
| `--management-group-id`, `-m` | Target management group ID |
| `--template-file`, `-f` | Bicep file path |

### az deployment tenant what-if

Previews changes for tenant-level deployments (`tenant`).

```bash
az deployment tenant what-if \
  --location <location> \
  --template-file <bicep-file> \
  [options]
```

**Required parameters:**

| Parameter | Description |
|-----------|-------------|
| `--location`, `-l` | Deployment metadata location |
| `--template-file`, `-f` | Bicep file path |

### az login

Authenticates with the Azure CLI.

```bash
az login [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--tenant`, `-t` | Tenant ID or domain |
| `--use-device-code` | Uses the device code flow |
| `--service-principal` | Signs in as a service principal |

### az account show

Displays the current subscription context.

```bash
az account show
```

### az group exists

Checks whether the resource group exists.

```bash
az group exists --name <rg-name>
```

---

## Bicep CLI

### bicep build

Compiles Bicep to ARM JSON and validates syntax.

```bash
bicep build <bicep-file> [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--stdout` | Outputs to stdout instead of a file |
| `--outdir` | Output directory |
| `--outfile` | Output file path |
| `--no-restore` | Skips module restore |

**Examples:**

```bash
# Validate syntax (output to stdout, without creating a file)
bicep build main.bicep --stdout > /dev/null

# Build into a specific directory
bicep build main.bicep --outdir ./build

# Validate multiple files
for f in *.bicep; do bicep build "$f" --stdout; done
```

**Error output format:**

```text
/path/to/file.bicep(22,51) : Error BCP064: Found unexpected tokens in interpolated expression.
/path/to/file.bicep(22,51) : Error BCP004: The string at this location is not terminated.
```

Format: `<file>(<line>,<column>) : <severity> <code>: <message>`

### bicep --version

Checks the Bicep CLI version.

```bash
bicep --version
```

---

## Parameter file detection

### Bicep parameters (.bicepparam)

Modern Bicep parameter files (recommended):

```bicep
using './main.bicep'

param location = 'eastus'
param environment = 'dev'
param tags = {
  environment: 'dev'
  project: 'myapp'
}
```

**Detection pattern:** `<template-name>.bicepparam`

### JSON parameters (.parameters.json)

Traditional ARM parameter files:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": { "value": "eastus" },
    "environment": { "value": "dev" }
  }
}
```

**Detection patterns:**

- `<template-name>.parameters.json`
- `parameters.json`
- `parameters/<env>.json`

### Using parameters with commands

```bash
# Bicep parameter file
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam

# JSON parameter file
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters @parameters.json

# Inline parameter overrides
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --parameters location=westus
```

---

## Determining the deployment scope

Check the Bicep file's `targetScope` declaration:

```bicep
// Resource group (default when not specified)
targetScope = 'resourceGroup'

// Subscription
targetScope = 'subscription'

// Management group
targetScope = 'managementGroup'

// Tenant
targetScope = 'tenant'
```

**Scope-to-command mapping:**

| targetScope | Command | Required parameters |
|-------------|---------|---------------------|
| `resourceGroup` | `az deployment group what-if` | `--resource-group` |
| `subscription` | `az deployment sub what-if` | `--location` |
| `managementGroup` | `az deployment mg what-if` | `--location`, `--management-group-id` |
| `tenant` | `az deployment tenant what-if` | `--location` |

---

## Version requirements

| Tool | Minimum version | Recommended version | Key features |
|------|-----------------|---------------------|--------------|
| Azure CLI | 2.14.0 | 2.76.0+ | `--validation-level` option |
| Azure Developer CLI | 1.0.0 | Latest | `--preview` option |
| Bicep CLI | 0.4.0 | Latest | Better error messages |

**Check versions:**

```bash
az --version
azd version
bicep --version
```
