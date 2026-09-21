# Error handling guide

This reference documents common errors during preflight validation and how to handle them.

## Core principle

**Continue on failure.** Record all issues in the final report instead of stopping at the first error. This provides a complete picture of what needs to be fixed.

---

## Authentication errors

### Not authenticated (Azure CLI)

**Detection:**

```text
ERROR: Please run 'az login' to setup account.
ERROR: AADSTS700082: The refresh token has expired
```

**Exit codes:** non-zero

**Handling:**

1. Record the error in the report
2. Include remediation steps
3. Skip the remaining Azure CLI commands
4. Continue with other validation steps if possible

**Report entry:**

```markdown
#### Azure CLI authentication required

- **Severity:** Error
- **Source:** az CLI
- **Message:** Not authenticated with the Azure CLI
- **Remediation:** Run `az login` to authenticate, then rerun preflight validation
- **Documentation:** https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli
```

### Not authenticated (azd)

**Detection:**

```text
ERROR: not logged in, run `azd auth login` to login
```

**Handling:**

1. Record the error in the report
2. Skip azd commands
3. Suggest `azd auth login`

**Report entry:**

```markdown
#### Azure Developer CLI authentication required

- **Severity:** Error
- **Source:** azd
- **Message:** Not authenticated with the Azure Developer CLI
- **Remediation:** Run `azd auth login` to authenticate, then rerun preflight validation
```

### Expired token

**Detection:**

```text
AADSTS700024: Client assertion is not within its valid time range
AADSTS50173: The provided grant has expired
```

**Handling:**

1. Record the error
2. Suggest reauthentication
3. Skip Azure operations

---

## Permission errors

### Insufficient RBAC permissions

**Detection:**

```text
AuthorizationFailed: The client '...' with object id '...' does not have authorization
to perform action '...' over scope '...'
```

**Handling:**

1. **First attempt:** retry with `--validation-level ProviderNoRbac`
2. Record the permission limitation in the report
3. If ProviderNoRbac also fails, report the specific missing permission

**Report entry:**

```markdown
#### Validation with limited permissions

- **Severity:** Warning
- **Source:** what-if
- **Message:** Full RBAC validation failed; using read-only validation
- **Detail:** Missing permission: `Microsoft.Resources/deployments/write` at scope `/subscriptions/xxx`
- **Recommendation:** Request the Contributor role on the target resource group or check deployment permissions with the administrators
```

### Resource group not found

**Detection:**

```text
ResourceGroupNotFound: Resource group 'xxx' could not be found.
```

**Handling:**

1. Record in the report
2. Suggest creating the resource group
3. Skip what-if for this scope

**Report entry:**

````markdown
#### Resource group does not exist

- **Severity:** Error
- **Source:** what-if
- **Message:** Resource group 'my-rg' does not exist
- **Remediation:** Create the resource group before deployment:
  ```bash
  az group create --name my-rg --location eastus
  ```

````

### Subscription access denied

**Detection:**

```text

SubscriptionNotFound: The subscription 'xxx' could not be found.
InvalidSubscriptionId: Subscription '...' is not valid

```

**Handling:**

1. Record in the report
2. Suggest checking the subscription ID
3. List available subscriptions

---

## Bicep syntax errors

### Build errors

**Detection:**

```text

/path/main.bicep(22,51) : Error BCP064: Found unexpected tokens
/path/main.bicep(10,5) : Error BCP018: Expected the "=" character at this location

```

**Handling:**

1. Parse the error output for line/column numbers
2. Include all errors in the report (do not stop at the first)
3. Continue to what-if (it may provide additional context)

**Report entry:**

```markdown
#### Bicep syntax error

- **Severity:** Error
- **Source:** bicep build
- **Location:** `main.bicep:22:51`
- **Code:** BCP064
- **Message:** Unexpected tokens found in the interpolated expression
- **Remediation:** Check the string interpolation syntax on line 22
- **Documentation:** https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/diagnostics/bcp064
```

### Module not found

**Detection:**

```text
Error BCP091: An error occurred reading file. Could not find file '...'
Error BCP190: The module is not valid
```

**Handling:**

1. Record the missing module
2. Check whether `bicep restore` is needed
3. Check the module path

### Parameter file issues

**Detection:**

```text
Error BCP032: The value must be a compile-time constant
Error BCP035: The specified object is missing required properties
```

**Handling:**

1. Record the parameter issues
2. Identify which parameters have issues
3. Suggest fixes

---

## Tool not installed

### Azure CLI not found

**Detection:**

```text
'az' is not recognized as an internal or external command
az: command not found
```

**Handling:**

1. Record in the report
2. Provide installation instructions. If available, use the Azure MCP tool `extension_cli_install` to obtain them. Otherwise, find instructions at https://learn.microsoft.com/en-us/cli/azure/install-azure-cli.
3. Skip az commands

**Report entry:**

```markdown
#### Azure CLI not installed

- **Severity:** Warning
- **Source:** environment
- **Message:** The Azure CLI (az) is not installed or is not on PATH
- **Remediation:** Install the Azure CLI <ADD INSTALLATION INSTRUCTIONS HERE>
- **Impact:** What-if validation using az commands was skipped
```

### Bicep CLI not found

**Detection:**

```text
'bicep' is not recognized as an internal or external command
bicep: command not found
```

**Handling:**

1. Record in the report
2. The Azure CLI may have Bicep built in; try `az bicep build`
3. Provide the installation link

**Report entry:**

```markdown
#### Bicep CLI not installed

- **Severity:** Warning
- **Source:** environment
- **Message:** The Bicep CLI is not installed
- **Remediation:** Install the Bicep CLI: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/install
- **Impact:** Syntax validation was skipped; Azure will validate during what-if
```

### Azure Developer CLI not found

**Detection:**

```text
'azd' is not recognized as an internal or external command
azd: command not found
```

**Handling:**

1. If `azure.yaml` exists, this tool is required
2. Fall back to az CLI commands if possible
3. Record in the report

---

## What-if-specific errors

### Nested template limits

**Detection:**

```text
The deployment exceeded the nested template limit of 500
```

**Handling:**

1. Record as a warning (not an error)
2. Explain that affected resources appear as "Ignore"
3. Suggest a manual review

### Unsupported template link

**Detection:**

```text
templateLink references in nested deployments won't be visible in what-if
```

**Handling:**

1. Record as a warning
2. Explain the limitation
3. Resources will be checked during the actual deployment

### Unevaluated expressions

**Detection:** properties showing function names such as `[utcNow()]` instead of values

**Handling:**

1. Record as informational
2. Explain that they are evaluated during deployment
3. This is not an error

---

## Network errors

### Timeout

**Detection:**

```text
Connection timed out
Request timed out
```

**Handling:**

1. Suggest retrying
2. Check network connectivity
3. This may indicate Azure service issues

### SSL/TLS errors

**Detection:**

```text
SSL: CERTIFICATE_VERIFY_FAILED
unable to get local issuer certificate
```

**Handling:**

1. Record in the report
2. This may indicate a corporate proxy or firewall
3. Suggest checking SSL settings

---

## Fallback strategy

When primary validation fails, try the alternatives in order:

```text
Provider (full RBAC validation)
    ↓ fails with a permission error
ProviderNoRbac (validation without checking write permission)
    ↓ fails
Template (static syntax only)
    ↓ fails
Report all failures and skip what-if analysis
```

**Always continue to report generation**, even if all validation steps fail.

---

## Aggregating errors in the report

When multiple errors occur, aggregate them logically:

1. **Group by source** (bicep, what-if, and permissions)
2. **Sort by severity** (errors before warnings)
3. **Deduplicate** similar errors
4. **Provide a summary count** at the beginning

Example:

```markdown
## Issues

Found **3 errors** and **2 warnings**

### Errors (3)

1. [Bicep syntax error - main.bicep:22:51](#error-1)
2. [Bicep syntax error - main.bicep:45:10](#error-2)
3. [Resource group not found](#error-3)

### Warnings (2)

1. [Validation with limited permissions](#warning-1)
2. [Nested template limit reached](#warning-2)
```

---

## Exit code reference

| Tool | Exit code | Meaning |
|------|-----------|---------|
| az | 0 | Success |
| az | 1 | General error |
| az | 2 | Command not found |
| az | 3 | Missing required argument |
| azd | 0 | Success |
| azd | 1 | Error |
| bicep | 0 | Build succeeded |
| bicep | 1 | Build failed (errors) |
| bicep | 2 | Build succeeded with warnings |
