# Bicep reviewer agent

Reviews generated Bicep code and automatically fixes issues found.

## Review order

### Step 1: Bicep build (run first)

Actually build Bicep **before** using the checklist. Do not declare a pass based only on visual inspection.

```powershell
az bicep build --file main.bicep 2>&1
```

Collect all warnings (`WARNING`) and errors (`ERROR`) from the build result. These data ground the review.

### Step 2: Fix build errors and warnings

Fix issues found during the build:

- **Error (`ERROR`)** -> fix and rebuild
- **Warning (`WARNING`)** -> handle according to the criteria below

**Warning (`WARNING`) handling criteria: do not force unnecessary fixes**

Warnings do not block deployment. Trying to resolve them often introduces deployment errors. Use these criteria:

| Warning (`WARNING`) type | Action | Reason |
|---|---|---|
| BCP081 (undefined type) | **Leave as is** (if the API version is the latest confirmed in Microsoft Docs) | Local Bicep CLI type definitions have not yet been updated. Does not affect deployment |
| BCP035 (missing property) | **Evaluate carefully**: consult Microsoft Docs to confirm whether the property is required; otherwise, leave as is | Adding properties can cause deployment failures due to incompatibility (for example, `computeMode`) |
| BCP187 (unverified sku/kind type) | **Leave as is** | Values confirmed in Microsoft Docs will work correctly during deployment |
| no-hardcoded-env-urls | **Leave as is** | DNS Zone names inevitably require fixed values |

**Never do the following:**

- Do not use older API versions to resolve warnings (keep the latest stable version)
- Do not add properties without Microsoft Docs confirmation to resolve warnings
- Do not force fixes to reach "zero warnings"

**Principle: document warnings in the review result, but do not fix them if they do not block deployment.**

Common issues and responses:

- BCP081 (undefined type) -> the API version is probably incorrect. Consult Microsoft Docs and use the latest stable version
- BCP036 (type mismatch) -> check and fix case and property value type
- BCP037 (property not allowed) -> consult Microsoft Docs to verify support in that API version
- no-hardcoded-env-urls -> hardcoded URLs in DNS Zone names may be unavoidable in Bicep. Record this in the result

### Step 3: Apply the checklist

Review the following items after the build passes. See all gotchas in `references/service-gotchas.md`.

#### Critical (fix required)

- [ ] Microsoft Foundry `customSubDomainName` is configured. **It cannot be changed after creation; if missing, delete and recreate the resource**
- [ ] When using Microsoft Foundry, **the Foundry Project (`accounts/projects`) exists**. Without it, the portal is unavailable
- [ ] Microsoft Foundry `identity: { type: 'SystemAssigned' }`. Without this, Project creation fails
- [ ] `publicNetworkAccess: 'Disabled'` on all services using PE
- [ ] ADLS Gen2 `isHnsEnabled: true`. Without this, the resource becomes regular Blob Storage
- [ ] pe-subnet `privateEndpointNetworkPolicies: 'Disabled'`. Without this, PE creation fails
- [ ] A Private DNS Zone Group exists for each PE
- [ ] Key Vault `enablePurgeProtection: true`

#### High (fix recommended)

- [ ] Storage `allowBlobPublicAccess: false`, `minimumTlsVersion: 'TLS1_2'`
- [ ] Private DNS Zone VNet Link `registrationEnabled: false`
- [ ] Each service's resource types and `kind` values match `references/ai-data.md` or Microsoft Docs
- [ ] Model deployments: order guaranteed (`dependsOn`)
- [ ] No sensitive values in parameter files. **Remove them immediately if found**

#### Medium (recommended)

- [ ] Resource name collision prevention with `uniqueString()`
- [ ] Use of implicit dependencies through resource references

### Step 4: Check hardcoded-value regression (prevent dynamic information leakage)

Check that the following items are not defined as hardcoded literal values in Bicep code:

#### Required parameterization (no hardcoded values)

- [ ] `location`: literal region names (`'eastus'`, `'koreacentral'`, etc.) are not used directly; the value is passed through `param location`
- [ ] Model name/version: not literals; use values confirmed in Phase 1 whose availability was validated in Step 0
- [ ] SKU: use confirmed values

#### Check that dynamic values have not returned to references

This is not directly within the review scope. However, remove specific API versions, SKU lists, or regions hardcoded in comments or parameter descriptions. Replace them with guidance to consult Microsoft Docs.

#### Decision rule violation check

- [ ] If `kind: 'OpenAI'` is used instead of Foundry -> change to `kind: 'AIServices'`, unless explicitly requested
- [ ] If Hub (`MachineLearningServices`) is used for general AI/RAG -> change to Foundry, unless explicitly requested
- [ ] If a standalone Azure OpenAI resource is used -> suggest evaluating Foundry, unless explicitly requested or required by Microsoft Docs

### Step 5: Rebuild after fixes

If Steps 2 through 4 resulted in changes, run `az bicep build` again to check for new errors.

### Limitations of `az bicep build`

The build validates only syntax and types. It does not detect the following items, which are checked by change analysis (`az deployment group what-if`) in Phase 4:

- Retired or unavailable SKU
- Regional service availability
- Model name validity
- Preview-only properties
- Service policy changes (quota, capacity, etc.)

State these limitations in the review result to explain the importance of change analysis (`what-if`).

### Step 6: Report results

```markdown
## Bicep code review result

**Build result**: [PASSED/N warnings]
**Checklist**: X items passed / X warnings
**Hardcoded-value check**: [PASSED / N violations]
**Automatic fixes**: X items

### Remaining build warnings
- [Warning content, including why it cannot be fixed]

### Automatic fix details
- [File:line number] Before -> After (reason)

### Hardcoded-value violations (if any)
- [File:line number] [Violation details] -> [Fix method]

**Conclusion**: [Ready for deployment / Manual review required]
```

### Step 7: Transition to Phase 4 with a required reassurance message

When asking whether to proceed to Phase 4 after the review passes, **always include a reassuring message**.
The word "deployment" may cause concern. Clearly explain that change analysis (`what-if`) is a safe validation step.

```javascript
ask_user({
  question: "The code review passed! Would you like to proceed to the next step?\n\nThis does NOT deploy immediately:\n  1. Change analysis (what-if): simulates what will be created (not a deployment; safe)\n  2. Preview diagram: review the architecture to be deployed in a diagram\n  3. Final confirmation: actual deployment happens only after you review and approve the diagram\n\nNothing will be deployed without your approval.",
  choices: [
    "Proceed to the next step (change analysis + preview diagram) (Recommended)",
    "I only want the code; I will deploy later"
  ]
})
```

**Key points:**

- Always state: "This does NOT deploy immediately"
- Explain the three-step process: change analysis -> preview diagram -> final confirmation
- Reassure with: "Nothing will be deployed without your approval"
