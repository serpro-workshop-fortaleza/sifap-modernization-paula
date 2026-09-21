# Pipeline variables, variable groups, and agents

## Contents

- [Pipeline variables](#pipeline-variables)
- [Variable groups](#variable-groups)
- [Pipeline folders](#pipeline-folders)
- [Agent pools](#agent-pools)
- [Agent queues](#agent-queues)
- [Agents](#agents)

---

## Pipeline variables

### List variables

```bash
az pipelines variable list --pipeline-id {pipeline-id}
```

### Create variable

```bash
# Non-secret variable
az pipelines variable create \
  --name {var-name} \
  --value {var-value} \
  --pipeline-id {pipeline-id}

# Secret variable
az pipelines variable create \
  --name {var-name} \
  --secret true \
  --pipeline-id {pipeline-id}

# Secret with interactive prompt
az pipelines variable create \
  --name {var-name} \
  --secret true \
  --prompt true \
  --pipeline-id {pipeline-id}
```

### Update variable

```bash
az pipelines variable update \
  --name {var-name} \
  --value {new-value} \
  --pipeline-id {pipeline-id}

# Update secret variable
az pipelines variable update \
  --name {var-name} \
  --secret true \
  --value "{new-secret-value}" \
  --pipeline-id {pipeline-id}
```

### Delete variable

```bash
az pipelines variable delete --name {var-name} --pipeline-id {pipeline-id} --yes
```

## Variable groups

### List variable groups

```bash
az pipelines variable-group list
az pipelines variable-group list --output table
```

### Show variable group

```bash
az pipelines variable-group show --id {group-id}
```

### Create variable group

```bash
az pipelines variable-group create \
  --name {group-name} \
  --variables key1=value1 key2=value2 \
  --authorize true
```

### Update variable group

```bash
az pipelines variable-group update \
  --id {group-id} \
  --name {new-name} \
  --description "Updated description"
```

### Delete variable group

```bash
az pipelines variable-group delete --id {group-id} --yes
```

### Variable group variables

```bash
# List variables
az pipelines variable-group variable list --group-id {group-id}

# Create non-secret variable
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name {var-name} \
  --value {var-value}

# Create secret variable (prompts for the value if not supplied)
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name {var-name} \
  --secret true

# Create secret with an environment variable
export AZURE_DEVOPS_EXT_PIPELINE_VAR_MySecret=secretvalue
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name MySecret \
  --secret true

# Update variable
az pipelines variable-group variable update \
  --group-id {group-id} \
  --name {var-name} \
  --value {new-value} \
  --secret false

# Delete variable
az pipelines variable-group variable delete \
  --group-id {group-id} \
  --name {var-name}
```

## Pipeline folders

### List folders

```bash
az pipelines folder list
```

### Create folder

```bash
az pipelines folder create --path 'folder/subfolder' --description "My folder"
```

### Delete folder

```bash
az pipelines folder delete --path 'folder/subfolder'
```

### Update folder

```bash
az pipelines folder update --path 'old-folder' --new-path 'new-folder'
```

## Agent pools

### List agent pools

```bash
az pipelines pool list
az pipelines pool list --pool-type automation
az pipelines pool list --pool-type deployment
```

### Show agent pool

```bash
az pipelines pool show --pool-id {pool-id}
```

## Agent queues

### List agent queues

```bash
az pipelines queue list
az pipelines queue list --pool-name {pool-name}
```

### Show agent queue

```bash
az pipelines queue show --id {queue-id}
```

## Agents

### List pool agents

```bash
az pipelines agent list --pool-id {pool-id}
```

### Show agent details

```bash
az pipelines agent show --agent-id {agent-id} --pool-id {pool-id}
```
