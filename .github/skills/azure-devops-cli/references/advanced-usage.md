# Advanced usage: output, queries, and parameters

## Contents

- [Output formats](#output-formats)
- [JMESPath queries](#jmespath-queries)
- [Advanced JMESPath queries](#advanced-jmespath-queries)
- [Global arguments](#global-arguments)
- [Common parameters](#common-parameters)
- [Git aliases](#git-aliases)
- [Getting help](#getting-help)

---

## Output formats

All commands support multiple output formats:

```bash
# Table format (human-readable)
az pipelines list --output table

# JSON format (default, machine-readable)
az pipelines list --output json

# JSONC (colored JSON)
az pipelines list --output jsonc

# YAML format
az pipelines list --output yaml

# YAMLC (colored YAML)
az pipelines list --output yamlc

# TSV format (tab-separated values)
az pipelines list --output tsv

# None (no output)
az pipelines list --output none
```

## JMESPath queries

Filter and transform output:

```bash
# Filter by name
az pipelines list --query "[?name=='myPipeline']"

# Get specific fields
az pipelines list --query "[].{Name:name, ID:id}"

# Chain queries
az pipelines list --query "[?name.contains('CI')].{Name:name, ID:id}" --output table

# Get the first result
az pipelines list --query "[0]"

# Get the first N results
az pipelines list --query "[0:5]"
```

## Advanced JMESPath queries

### Filtering and sorting

```bash
# Filter by multiple conditions
az pipelines list --query "[?name.contains('CI') && enabled==true]"

# Filter by status and result
az pipelines runs list --query "[?status=='completed' && result=='succeeded']"

# Sort by date (descending)
az pipelines runs list --query "sort_by([?status=='completed'], &finishTime | reverse(@))"

# Get the first N items after filtering
az pipelines runs list --query "[?result=='succeeded'] | [0:5]"
```

### Nested queries

```bash
# Extract nested properties
az pipelines show --id $PIPELINE_ID --query "{Name:name, Repo:repository.{Name:name, Type:type}, Folder:folder}"

# Query build details
az pipelines build show --id $BUILD_ID --query "{ID:id, Number:buildNumber, Status:status, Result:result, Requested:requestedFor.displayName}"
```

### Complex filtering

```bash
# Find pipelines with a specific YAML path
az pipelines list --query "[?process.type.name=='yaml' && process.yamlFilename=='azure-pipelines.yml']"

# Find pull requests for a specific reviewer
az repos pr list --query "[?contains(reviewers[?displayName=='John Doe'].displayName, 'John Doe')]"

# Find work items with a specific iteration and state
az boards work-item show --id $WI_ID --query "{Title:fields['System.Title'], State:fields['System.State'], Iteration:fields['System.IterationPath']}"
```

### Aggregation

```bash
# Count items by status
az pipelines runs list --query "groupBy([?status=='completed'], &[result]) | {Succeeded: [?key=='succeeded'][0].count, Failed: [?key=='failed'][0].count}"

# Get unique reviewers
az repos pr list --query "unique_by(reviewers[], &displayName)"

# Sum values
az pipelines runs list --query "[?result=='succeeded'] | [].{Duration:duration} | [0].Duration"
```

### Conditional transformation

```bash
# Format dates
az pipelines runs list --query "[].{ID:id, Date:createdDate, Formatted:createdDate | format_datetime(@, 'yyyy-MM-dd HH:mm')}"

# Conditional output
az pipelines list --query "[].{Name:name, Status:(enabled ? 'Enabled' : 'Disabled')}"

# Extract with defaults
az pipelines show --id $PIPELINE_ID --query "{Name:name, Folder:folder || 'Root', Description:description || 'No description'}"
```

### Complex workflows

```bash
# Find the longest-running builds
az pipelines build list --query "sort_by([?result=='succeeded'], &queueTime) | reverse(@) | [0:3].{ID:id, Number:buildNumber, Duration:duration}"

# Get pull request statistics by reviewer
az repos pr list --query "groupBy([], &reviewers[].displayName) | [].{Reviewer:@.key, Count:length(@)}"

# Find work items with multiple children
az boards work-item relation list --id $PARENT_ID --query "[?rel=='System.LinkTypes.Hierarchy-Forward'] | [].{ChildID:url | split('/', @) | [-1]}"
```

## Global arguments

Available on all commands:

| Parameter | Description |
|---|---|
| `--help` / `-h` | Show command help |
| `--output` / `-o` | Output format (json, jsonc, none, table, tsv, yaml, yamlc) |
| `--query` | JMESPath query string to filter output |
| `--verbose` | Increase log verbosity |
| `--debug` | Show all debug logs |
| `--only-show-errors` | Show only errors and suppress warnings |
| `--subscription` | Subscription name or ID |
| `--yes` / `-y` | Skip confirmation prompts |

## Common parameters

| Parameter | Description |
|---|---|
| `--org` / `--organization` | Azure DevOps organization URL (for example, `https://dev.azure.com/{org}`) |
| `--project` / `-p` | Project name or ID |
| `--detect` | Automatically detect the organization from Git configuration |
| `--yes` / `-y` | Skip confirmation prompts |
| `--open` | Open the resource in the browser |
| `--subscription` | Azure subscription (for Azure resources) |

## Git aliases

After enabling Git aliases:

```bash
# Enable Git aliases
az devops configure --use-git-aliases true

# Use Git commands for DevOps operations
git pr create --target-branch main
git pr list
git pr checkout 123
```

## Getting help

```bash
# General help
az devops --help

# Help for a specific command group
az pipelines --help
az repos pr --help

# Help for a specific command
az repos pr create --help

# Search for examples
az find "az repos pr create"
```
