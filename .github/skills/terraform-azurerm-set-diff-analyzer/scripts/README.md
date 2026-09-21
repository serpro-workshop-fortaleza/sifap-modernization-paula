# Terraform AzureRM Set diff analyzer script

Python script that analyzes Terraform plan JSON and identifies "false-positive diffs" in AzureRM Set-type attributes.

## Overview

The AzureRM provider's Set-type attributes, such as `backend_address_pool` and `security_rule`, do not guarantee order. When adding or removing elements, all of them may appear as "changed". This script distinguishes these "false-positive diffs" from real changes.

### Use cases

- As an **Agent Skill** (recommended)
- As a **CLI tool** for manual execution
- For automated analysis in **CI/CD workflows**

## Prerequisites

- Python 3.8 or later
- No additional packages required (uses only the standard library)

## Usage

### Basic usage

```bash
# Read from a file
python analyze_plan.py plan.json

# Read from stdin
terraform show -json plan.tfplan | python analyze_plan.py
```

### Options

| Option | Short form | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format (markdown/json/summary) | markdown |
| `--exit-code` | `-e` | Returns an exit code based on changes | false |
| `--quiet` | `-q` | Suppresses warnings | false |
| `--verbose` | `-v` | Shows detailed warnings | false |
| `--ignore-case` | - | Compares values without case sensitivity | false |
| `--attributes` | - | Path to a custom attribute definitions file | (built-in) |
| `--include` | - | Filters resources to analyze (repeatable) | (all) |
| `--exclude` | - | Filters resources to exclude (repeatable) | (none) |

### Exit codes (with `--exit-code`)

| Code | Meaning |
|------|---------|
| 0 | No changes or order-only changes |
| 1 | Actual changes in Set attributes |
| 2 | Resource replacement (delete + create) |
| 3 | Error |

## Output formats

### Markdown (default)

Readable format for pull request comments and reports.

```bash
python analyze_plan.py plan.json --format markdown
```

### JSON

Structured data for programmatic processing.

```bash
python analyze_plan.py plan.json --format json
```

Example output:

```json
{
  "summary": {
    "order_only_count": 3,
    "actual_set_changes_count": 1,
    "replace_count": 0
  },
  "has_real_changes": true,
  "resources": [...],
  "warnings": []
}
```

### Summary

One-line summary for CI/CD logs.

```bash
python analyze_plan.py plan.json --format summary
```

Example output:

```text
🟢 3 order-only | 🟡 1 Set change
```

## Usage in CI/CD workflows

### GitHub Actions

```yaml
name: Terraform plan analysis

on:
  pull_request:
    paths:
      - '**.tf'

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform init and plan
        run: |
          terraform init
          terraform plan -out=plan.tfplan
          terraform show -json plan.tfplan > plan.json

      - name: Analyze Set diff
        run: |
          python path/to/analyze_plan.py plan.json --format markdown > analysis.md

      - name: Comment on pull request
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: analysis.md
```

### GitHub Actions (exit-code gate)

```yaml
      - name: Analyze and enforce gate
        run: |
          python path/to/analyze_plan.py plan.json --exit-code --format summary
        # Fails with exit code 2 (resource replacement)
        continue-on-error: false
```

### Azure Pipelines

```yaml
- task: TerraformCLI@0
  inputs:
    command: 'plan'
    commandOptions: '-out=plan.tfplan'

- script: |
    terraform show -json plan.tfplan > plan.json
    python scripts/analyze_plan.py plan.json --format markdown > $(Build.ArtifactStagingDirectory)/analysis.md
  displayName: 'Analyze plan'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)/analysis.md'
    artifactName: 'plan-analysis'
```

### Filtering examples

Analyze only specific resources:

```bash
python analyze_plan.py plan.json --include application_gateway --include load_balancer
```

Exclude specific resources:

```bash
python analyze_plan.py plan.json --exclude virtual_network
```

## Interpreting results

| Category | Meaning | Recommended action |
|----------|---------|-------------------|
| 🟢 Order only | False-positive diff, no real change | Can be safely ignored |
| 🟡 Actual change | Set element added, removed, or modified | Review the content; usually an in-place update |
| 🔴 Resource replacement | delete + create | Check downtime impact |

## Custom attribute definitions

By default, it uses `references/azurerm_set_attributes.json`, but you can provide a custom definition file:

```bash
python analyze_plan.py plan.json --attributes /path/to/custom_attributes.json
```

See `references/azurerm_set_attributes.md` for the definition file format.

## Limitations

- Only AzureRM resources (`azurerm_*`) are supported
- Some resources or attributes may not be supported
- Comparisons may be incomplete for attributes containing `after_unknown` (values determined after applying the plan)
- Comparisons may be incomplete for sensitive attributes (they are masked)

## Related documentation

- [SKILL.md](../SKILL.md): usage as an Agent Skill
- [azurerm_set_attributes.md](../references/azurerm_set_attributes.md): attribute definitions reference
