# Phase 4: deployment agent

This file contains detailed Phase 4 instructions. Read and follow it when deployment is approved after Phase 3 (code review) is complete.

---

**Mandatory Phase 4 execution order: never skip any step**

Execute the five steps below **strictly in order**. No step may be omitted.
Even if the user says "deploy", "go ahead", "do it", etc., always start with Step 1.

```text
Step 1: check prerequisites (az login, subscription, resource group)
    ↓
Step 2: change analysis, what-if (az deployment group what-if) ← execution required
    ↓
Step 3: generate the preview diagram (02_arch_diagram_preview.html) ← generation required
    ↓
Step 4: actual deployment after final confirmation (az deployment group create)
    ↓
Step 5: generate the deployment result diagram (03_arch_diagram_result.html)
```

**Never do the following:**

- Run `az deployment group create` directly without change analysis (`what-if`)
- Skip preview diagram generation (`02_arch_diagram_preview.html`)
- Proceed with deployment without presenting the change analysis result
- Provide only `az` commands for manual execution

---

## Step 1: check prerequisites

```powershell
# Check az CLI installation and authentication
az account show 2>&1
```

If not authenticated, ask the user to run `az login`.
The agent must never enter or store credentials directly.

Create the resource group:

```powershell
az group create --name "<RG_NAME>" --location "<LOCATION>"  # Location confirmed in Phase 1
```

→ After confirming success, proceed to the next step

## Step 2: validation (`validate`) → change analysis (`what-if`), required

**Do not skip this step. Always execute it, regardless of the request's urgency.**

**Step 2-A: run validate first (quick pre-validation)**

Change analysis (`what-if`) may **hang indefinitely without error messages** when Azure Policy violations, resource reference errors, etc. occur.
To avoid this, **always run validation (`validate`) first**. It returns errors quickly.

```powershell
# validate: quickly detect policy violations, schema errors, and parameter issues
az deployment group validate `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam
```

- **Validation succeeds** → proceed to Step 2-B (change analysis)
- **Validation fails** → analyze messages, fix Bicep, build, and validate again
  - Azure Policy violation (`RequestDisallowedByPolicy`) → reflect policy requirements in Bicep (for example, `azureADOnlyAuthentication: true`)
  - Schema error → fix the API version or properties
  - Parameter error → fix the parameter file

**Step 2-B: run change analysis (`what-if`)**

Run change analysis after validation passes.

**Choose the parameter-passing method:**

- If all `@secure()` parameters have default values → use `.bicepparam`
- If `@secure()` parameters require input → use `--template-file` + a JSON parameter file

```powershell
# Method 1: use .bicepparam (when all @secure() parameters have default values)
az deployment group what-if `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam

# Method 2: use a JSON parameter file (when @secure() parameters require input)
az deployment group what-if `
  --resource-group "<RG_NAME>" `
  --template-file main.bicep `
  --parameters main.parameters.json `
  --parameters secureParam='value'
```

→ Summarize and present the change analysis result.

**Change analysis execution method and timeout handling:**

Change analysis validates resources on the Azure server. Duration depends on the service and region.
**Always run with `initial_wait: 300` (five minutes).** If it does not finish within that time, it will automatically time out.

```powershell
# Always set initial_wait: 300 when calling the powershell tool
# mode: "sync", initial_wait: 300
az deployment group what-if `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam
```

**Completed within five minutes** → proceed normally (summary → preview diagram → deployment confirmation)

**Not completed within five minutes (timeout)** → stop immediately with `stop_powershell` and offer options:

```text
ask_user({
  question: "Change analysis (what-if) did not finish within five minutes. The Azure server response is delayed. How would you like to proceed?",
  choices: [
    "Retry (Recommended)",
    "Skip change analysis and deploy directly"
  ]
})
```

**If "Retry" is selected:** run the same command with `initial_wait: 300`. Make at most two attempts.
**If "Skip change analysis and deploy directly" is selected:**

- Generate the preview diagram based on the Phase 1 draft
- Explain the risks:
  > **Deployment without prior change analysis (`what-if`).** Unexpected resource changes may occur. Check them in the Azure portal after deployment.

**Never do the following:**

- Run without setting `initial_wait`, causing an indefinite wait
- Allow the agent to arbitrarily decide that "change analysis is optional" and skip it
- Automatically proceed to deployment after a timeout without asking
- Skip change analysis because "deployment is faster"

## Step 3: preview diagram based on the change analysis result, required

**Do not skip this step. Always generate the preview diagram when change analysis succeeds.**

Regenerate the diagram using actual resources from the change analysis result (names, types, locations, and quantities).
Keep the Phase 1 draft (`01_arch_diagram_draft.html`) unchanged and generate `02_arch_diagram_preview.html`.
The draft can be reopened at any time.

```text
## Architecture to be deployed (based on change analysis)

[Interactive diagram link: 02_arch_diagram_preview.html]
(Design draft: 01_arch_diagram_draft.html)

Resources to be created (N items):
[Change analysis summary table]

Deploy these resources? (Yes/No)
```

Proceed to Step 4 after confirmation. **Do not proceed with deployment without the preview diagram.**

## Step 4: actual deployment

Execute only after the diagram and change analysis result have been reviewed and deployment approved.
**Use the same parameter-passing method as for change analysis.**

```powershell
$deployName = "deploy-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Method 1: use .bicepparam
az deployment group create `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam `
  --name $deployName `
  2>&1 | Tee-Object -FilePath deployment.log

# Method 2: use a JSON parameter file
az deployment group create `
  --resource-group "<RG_NAME>" `
  --template-file main.bicep `
  --parameters main.parameters.json `
  --name $deployName `
  2>&1 | Tee-Object -FilePath deployment.log
```

Monitor progress periodically during deployment:

```powershell
az deployment group show `
  --resource-group "<RG_NAME>" `
  --name "<DEPLOYMENT_NAME>" `
  --query "{status:properties.provisioningState, duration:properties.duration}" `
  -o table
```

## Handling deployment failures

When deployment fails, some resources may remain in the `Failed` state. Redeploying in this state causes errors such as `AccountIsNotSucceeded`.

**Resource deletion is destructive. Always explain the situation and obtain approval before executing.**

```text
[Resource name] failed during deployment.
To redeploy, first delete the failed resources.

Delete and redeploy? (Yes/No)
```

After approval, delete the failed resources and redeploy.

**Handling soft-deleted resources (avoid blocking redeployment):**

When a resource group is deleted after a failure, Cognitive Services (Foundry), Key Vault, etc. remain **soft-deleted (`soft-delete`)**.
Redeploying with the same name causes `FlagMustBeSetForRestore` and `Conflict` errors.

**Always check before redeployment:**

```powershell
# Check soft-deleted Cognitive Services
az cognitiveservices account list-deleted -o table

# Check soft-deleted Key Vaults
az keyvault list-deleted -o table
```

**Resolution options:**

```text
ask_user({
  question: "Soft-deleted resources from a previous deployment were found. How would you like to handle them?",
  choices: [
    "Purge and redeploy (Recommended): permanently delete and create new resources",
    "Redeploy in restore mode: recover existing resources"
  ]
})
```

**Caution: Key Vault with `enablePurgeProtection: true`:**

- Cannot be purged (wait until the retention period ends)
- Cannot be recreated with the same name
- **Solution: change the Key Vault name** and redeploy (for example, add a timestamp to the `uniqueString()` seed)
- Explain the situation and guide the name change

## Step 5: deployment complete, generate the diagram with actual resources and report

After deployment is complete, query the actual deployed resources and generate the final diagram.

**Step 1: query deployed resources**

```powershell
az resource list --resource-group "<RG_NAME>" --output json
```

**Step 2: generate the diagram with actual resources**

Extract resource names, types, SKUs, and endpoints and generate the final diagram with the built-in engine.
Take care with filenames to avoid overwriting previous diagrams:

- `01_arch_diagram_draft.html`: design draft (keep)
- `02_arch_diagram_preview.html`: change analysis preview (keep)
- `03_arch_diagram_result.html`: final deployment result version

Populate the diagram's `services` JSON with actual information:

- `name`: actual resource name (for example, `foundry-duru57kxgqzxs`)
- `sku`: actual SKU
- `details`: actual values, such as endpoints and location

**Step 3: report**

```text
## Deployment complete

[Interactive architecture diagram: 03_arch_diagram_result.html]
(Design draft: 01_arch_diagram_draft.html | Change analysis preview: 02_arch_diagram_preview.html)

Resources created (N items):
[Names, types, and endpoints dynamically extracted from the actual result]

## Next steps
1. Check resources in the Azure portal
2. Check the Private Endpoint connection state
3. Consult additional configuration guidance if needed

## Cleanup command (if needed)
az group delete --name <RG_NAME> --yes --no-wait
```

---

## Handling post-deployment change requests

**When an addition, modification, or deletion is requested after deployment, do NOT go directly to Bicep/deployment.**
Always return to Phase 1 and update the architecture first.

**Process:**

### 1. Confirm intent

First ask whether the user wants to add to the deployed architecture:

```text
Do you want to add a VM to the deployed architecture?
Current configuration: [Summary of deployed services]
```

### 2. Return to Phase 1 and apply the Change Confirmation Rule

- Use the existing result (`03_arch_diagram_result.html`) as the current-state reference
- Check required fields for new services (SKU, network, regional availability, etc.)
- Confirm unresolved items through `ask_user`
- Verify facts (Microsoft Docs lookup + cross-validation)

### 3. Generate the updated diagram

- Combine deployed and new resources in `04_arch_diagram_update_draft.html`
- Present the diagram and obtain confirmation:

```text
## Updated architecture

[Interactive diagram: 04_arch_diagram_update_draft.html]
(Previous deployment result: 03_arch_diagram_result.html)

**Changes:**
- Added: [List of new services]
- Removed: [List of removed services] (if any)

Proceed with this configuration?
```

### 4. After confirmation, execute Phases 2 → 3 → 4 in order

- Incrementally add new resource modules to the existing Bicep
- Review → change analysis (`what-if`) → incremental deployment

**Never do the following:**

- Go directly to Bicep generation without updating the diagram after a change request
- Ignore the existing deployment state and create new resources in isolation
- Proceed without confirming whether resources should be added to the existing architecture
