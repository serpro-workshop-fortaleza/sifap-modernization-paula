# Repositories and pull requests

## Contents

- [Repositories](#repositories)
- [Repository import](#repository-import)
- [Pull requests](#pull-requests)
- [Git references](#git-references)
- [Repository policies](#repository-policies)

---

## Repositories

### List repositories

```bash
az repos list --org https://dev.azure.com/{org} --project {project}
az repos list --output table
```

### Show repository details

```bash
az repos show --repository {repo-name} --project {project}
```

### Create repository

```bash
az repos create --name {repo-name} --project {project}
```

### Delete repository

```bash
az repos delete --id {repo-id} --project {project} --yes
```

### Update repository

```bash
az repos update --id {repo-id} --name {new-name} --project {project}
```

## Repository import

### Import Git repository

```bash
# Import from a public Git repository
az repos import create \
  --git-source-url https://github.com/user/repo \
  --repository {repo-name}

# Import with authentication
az repos import create \
  --git-source-url https://github.com/user/private-repo \
  --repository {repo-name} \
  --user {username} \
  --password {password-or-pat}
```

## Pull requests

### Create pull request

```bash
# Basic pull request creation
az repos pr create \
  --repository {repo} \
  --source-branch {source-branch} \
  --target-branch {target-branch} \
  --title "Pull request title" \
  --description "Pull request description" \
  --open

# Pull request with work items
az repos pr create \
  --repository {repo} \
  --source-branch {source-branch} \
  --work-items 63 64

# Draft pull request with reviewers
az repos pr create \
  --repository {repo} \
  --source-branch feature/new-feature \
  --target-branch main \
  --title "Feature: new operation" \
  --draft true \
  --reviewers user1@example.com user2@example.com \
  --required-reviewers lead@example.com \
  --labels "enhancement" "backlog"
```

### List pull requests

```bash
# All pull requests
az repos pr list --repository {repo}

# Filter by status
az repos pr list --repository {repo} --status active

# Filter by creator
az repos pr list --repository {repo} --creator {email}

# Table output
az repos pr list --repository {repo} --output table
```

### Show pull request details

```bash
az repos pr show --id {pr-id}
az repos pr show --id {pr-id} --open  # Open in the browser
```

### Update pull request (complete/abandon/draft)

```bash
# Complete pull request
az repos pr update --id {pr-id} --status completed

# Abandon pull request
az repos pr update --id {pr-id} --status abandoned

# Set as draft
az repos pr update --id {pr-id} --draft true

# Publish draft pull request
az repos pr update --id {pr-id} --draft false

# Auto-complete when policies pass
az repos pr update --id {pr-id} --auto-complete true

# Set title and description
az repos pr update --id {pr-id} --title "New title" --description "New description"
```

### Check out pull request locally

```bash
# Check out pull request branch
az repos pr checkout --id {pr-id}

# Check out with a specific remote
az repos pr checkout --id {pr-id} --remote-name upstream
```

### Vote on pull request

```bash
az repos pr set-vote --id {pr-id} --vote approve
az repos pr set-vote --id {pr-id} --vote approve-with-suggestions
az repos pr set-vote --id {pr-id} --vote reject
az repos pr set-vote --id {pr-id} --vote wait-for-author
az repos pr set-vote --id {pr-id} --vote reset
```

### Pull request reviewers

```bash
# Add reviewers
az repos pr reviewer add --id {pr-id} --reviewers user1@example.com user2@example.com

# List reviewers
az repos pr reviewer list --id {pr-id}

# Remove reviewers
az repos pr reviewer remove --id {pr-id} --reviewers user1@example.com
```

### Pull request work items

```bash
# Add work items to pull request
az repos pr work-item add --id {pr-id} --work-items {id1} {id2}

# List pull request work items
az repos pr work-item list --id {pr-id}

# Remove work items from pull request
az repos pr work-item remove --id {pr-id} --work-items {id1}
```

### Pull request policies

```bash
# List policies for a pull request
az repos pr policy list --id {pr-id}

# Queue policy evaluation for a pull request
az repos pr policy queue --id {pr-id} --evaluation-id {evaluation-id}
```

## Git references

### List references (branches)

```bash
az repos ref list --repository {repo}
az repos ref list --repository {repo} --query "[?name=='refs/heads/main']"
```

### Create reference (branch)

```bash
az repos ref create --name refs/heads/new-branch --object-type commit --object {commit-sha}
```

### Delete reference (branch)

```bash
az repos ref delete --name refs/heads/old-branch --repository {repo} --project {project}
```

### Lock/unlock branch

```bash
az repos ref lock --name refs/heads/main --repository {repo} --project {project}
az repos ref unlock --name refs/heads/main --repository {repo} --project {project}
```

## Repository policies

### List all policies

```bash
az repos policy list --repository {repo-id} --branch main
```

### Create/update/delete policy

```bash
# Create from a configuration file
az repos policy create --config policy.json

# Update
az repos policy update --id {policy-id} --config updated-policy.json

# Delete
az repos policy delete --id {policy-id} --yes
```

### Approval count policy

```bash
az repos policy approver-count create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --minimum-approver-count 2 \
  --creator-vote-counts true
```

### Build policy

```bash
az repos policy build create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --build-definition-id {definition-id} \
  --queue-on-source-update-only true \
  --valid-duration 720
```

### Work item linking policy

```bash
az repos policy work-item-linking create \
  --blocking true \
  --branch main \
  --enabled true \
  --repository-id {repo-id}
```

### Required review policy

```bash
az repos policy required-reviewer create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --required-reviewers user@example.com
```

### Merge strategy policy

```bash
az repos policy merge-strategy create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --allow-squash true \
  --allow-rebase true \
  --allow-no-fast-forward true
```

### Case enforcement policy

```bash
az repos policy case-enforcement create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id}
```

### Required comment policy

```bash
az repos policy comment-required create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id}
```

### File size policy

```bash
az repos policy file-size create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --maximum-file-size 10485760  # 10 MB in bytes
```
