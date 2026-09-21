# Organization, security, and administration

## Contents

- [Projects](#projects)
- [Extension management](#extension-management)
- [Service endpoints](#service-endpoints)
- [Teams](#teams)
- [Users](#users)
- [Security groups](#security-groups)
- [Security permissions](#security-permissions)
- [Wikis](#wikis)
- [Administration](#administration)
- [DevOps extensions](#devops-extensions)

---

## Projects

### List projects

```bash
az devops project list --organization https://dev.azure.com/{org}
az devops project list --top 10 --output table
```

### Create project

```bash
az devops project create \
  --name myNewProject \
  --organization https://dev.azure.com/{org} \
  --description "My new DevOps project" \
  --source-control git \
  --visibility private
```

### Show project details

```bash
az devops project show --project {project-name} --org https://dev.azure.com/{org}
```

### Delete project

```bash
az devops project delete --id {project-id} --org https://dev.azure.com/{org} --yes
```

## Extension management

### List extensions

```bash
# List available extensions
az extension list-available --output table

# List installed extensions
az extension list --output table
```

### Manage the Azure DevOps extension

```bash
# Install the Azure DevOps extension
az extension add --name azure-devops

# Update the Azure DevOps extension
az extension update --name azure-devops

# Remove extension
az extension remove --name azure-devops

# Install from a local path
az extension add --source ~/extensions/azure-devops.whl
```

## Service endpoints

### List service endpoints

```bash
az devops service-endpoint list --project {project}
az devops service-endpoint list --project {project} --output table
```

### Show service endpoint

```bash
az devops service-endpoint show --id {endpoint-id} --project {project}
```

### Create service endpoint

```bash
# Use a configuration file
az devops service-endpoint create --service-endpoint-configuration endpoint.json --project {project}
```

### Delete service endpoint

```bash
az devops service-endpoint delete --id {endpoint-id} --project {project} --yes
```

## Teams

### List teams

```bash
az devops team list --project {project}
```

### Show team

```bash
az devops team show --team {team-name} --project {project}
```

### Create team

```bash
az devops team create \
  --name {team-name} \
  --description "Team description" \
  --project {project}
```

### Update team

```bash
az devops team update \
  --team {team-name} \
  --project {project} \
  --name "{new-team-name}" \
  --description "Updated description"
```

### Delete team

```bash
az devops team delete --team {team-name} --project {project} --yes
```

### Show team members

```bash
az devops team list-member --team {team-name} --project {project}
```

## Users

### List users

```bash
az devops user list --org https://dev.azure.com/{org}
az devops user list --top 10 --output table
```

### Show user

```bash
az devops user show --user {user-id-or-email} --org https://dev.azure.com/{org}
```

### Add user

```bash
az devops user add \
  --email user@example.com \
  --license-type express \
  --org https://dev.azure.com/{org}
```

### Update user

```bash
az devops user update \
  --user {user-id-or-email} \
  --license-type advanced \
  --org https://dev.azure.com/{org}
```

### Remove user

```bash
az devops user remove --user {user-id-or-email} --org https://dev.azure.com/{org} --yes
```

## Security groups

### List groups

```bash
# List all project groups
az devops security group list --project {project}

# List all organization groups
az devops security group list --scope organization

# List with filtering
az devops security group list --project {project} --subject-types vstsgroup
```

### Show group details

```bash
az devops security group show --group-id {group-id}
```

### Create group

```bash
az devops security group create \
  --name {group-name} \
  --description "Group description" \
  --project {project}
```

### Update group

```bash
az devops security group update \
  --group-id {group-id} \
  --name "{new-group-name}" \
  --description "Updated description"
```

### Delete group

```bash
az devops security group delete --group-id {group-id} --yes
```

### Group memberships

```bash
# List memberships
az devops security group membership list --id {group-id}

# Add member
az devops security group membership add \
  --group-id {group-id} \
  --member-id {member-id}

# Remove member
az devops security group membership remove \
  --group-id {group-id} \
  --member-id {member-id} --yes
```

## Security permissions

### List namespaces

```bash
az devops security permission namespace list
```

### Show namespace details

```bash
# Show available permissions in a namespace
az devops security permission namespace show --namespace "GitRepositories"
```

### List permissions

```bash
# List permissions for a user/group and namespace
az devops security permission list \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project}

# List for a specific token (repository)
az devops security permission list \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}"
```

### Show permissions

```bash
az devops security permission show \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}"
```

### Update permissions

```bash
# Grant permission
az devops security permission update \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask "Pull,Contribute"

# Deny permission
az devops security permission update \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask 0
```

### Reset permissions

```bash
# Reset specific permission bits
az devops security permission reset \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask "Pull,Contribute"

# Reset all permissions
az devops security permission reset-all \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" --yes
```

## Wikis

### List wikis

```bash
# List all project wikis
az devops wiki list --project {project}

# List all organization wikis
az devops wiki list
```

### Show wiki

```bash
az devops wiki show --wiki {wiki-name} --project {project}
az devops wiki show --wiki {wiki-name} --project {project} --open
```

### Create wiki

```bash
# Create project wiki
az devops wiki create \
  --name {wiki-name} \
  --project {project} \
  --type projectWiki

# Create code wiki from repository
az devops wiki create \
  --name {wiki-name} \
  --project {project} \
  --type codeWiki \
  --repository {repo-name} \
  --mapped-path /wiki
```

### Delete wiki

```bash
az devops wiki delete --wiki {wiki-id} --project {project} --yes
```

### Wiki pages

```bash
# List pages
az devops wiki page list --wiki {wiki-name} --project {project}

# Show page
az devops wiki page show \
  --wiki {wiki-name} \
  --path "/page-name" \
  --project {project}

# Create page
az devops wiki page create \
  --wiki {wiki-name} \
  --path "/new-page" \
  --content "# New page\n\nPage content here..." \
  --project {project}

# Update page
az devops wiki page update \
  --wiki {wiki-name} \
  --path "/existing-page" \
  --content "# Updated page\n\nNew content..." \
  --project {project}

# Delete page
az devops wiki page delete \
  --wiki {wiki-name} \
  --path "/old-page" \
  --project {project} --yes
```

## Administration

### Banner management

```bash
# List banners
az devops admin banner list

# Show banner details
az devops admin banner show --id {banner-id}

# Add new banner
az devops admin banner add \
  --message "Scheduled system maintenance" \
  --level info  # info, warning, error

# Update banner
az devops admin banner update \
  --id {banner-id} \
  --message "Updated message" \
  --level warning \
  --expiration-date "2025-12-31T23:59:59Z"

# Remove banner
az devops admin banner remove --id {banner-id}
```

## DevOps extensions

Manage extensions installed in an Azure DevOps organization (different from CLI extensions).

```bash
# List installed extensions
az devops extension list --org https://dev.azure.com/{org}

# Search for extensions in the Marketplace
az devops extension search --search-query "docker"

# Show extension details
az devops extension show --ext-id {extension-id} --org https://dev.azure.com/{org}

# Install extension
az devops extension install \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org} \
  --publisher {publisher-id}

# Enable extension
az devops extension enable \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org}

# Disable extension
az devops extension disable \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org}

# Uninstall extension
az devops extension uninstall \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org} --yes
```
