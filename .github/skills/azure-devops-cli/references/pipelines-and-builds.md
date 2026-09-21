# Pipelines, builds, and releases

## Contents

- [Pipelines](#pipelines)
- [Pipeline runs](#pipeline-runs)
- [Builds](#builds)
- [Build definitions](#build-definitions)
- [Releases](#releases)
- [Release definitions](#release-definitions)
- [Universal packages (artifacts)](#universal-packages-artifacts)

---

## Pipelines

### List pipelines

```bash
az pipelines list --output table
az pipelines list --query "[?name=='myPipeline']"
az pipelines list --folder-path 'folder/subfolder'
```

### Create pipeline

```bash
# From local repository context (automatically detects settings)
az pipelines create --name 'ContosoBuild' --description 'Contoso project pipeline'

# With a specific branch and YAML path
az pipelines create \
  --name {pipeline-name} \
  --repository {repo} \
  --branch main \
  --yaml-path azure-pipelines.yml \
  --description "My CI/CD pipeline"

# For a GitHub repository
az pipelines create \
  --name 'GitHubPipeline' \
  --repository https://github.com/Org/Repo \
  --branch main \
  --repository-type github

# Skip the first run
az pipelines create --name 'MyPipeline' --skip-run true
```

### Show pipeline

```bash
az pipelines show --id {pipeline-id}
az pipelines show --name {pipeline-name}
```

### Update pipeline

```bash
az pipelines update --id {pipeline-id} --name "New name" --description "Updated description"
```

### Delete pipeline

```bash
az pipelines delete --id {pipeline-id} --yes
```

### Run pipeline

```bash
# Run by name
az pipelines run --name {pipeline-name} --branch main

# Run by ID
az pipelines run --id {pipeline-id} --branch refs/heads/main

# With parameters
az pipelines run --name {pipeline-name} --parameters version=1.0.0 environment=prod

# With variables
az pipelines run --name {pipeline-name} --variables buildId=123 configuration=release

# Open results in the browser
az pipelines run --name {pipeline-name} --open
```

## Pipeline runs

### List runs

```bash
az pipelines runs list --pipeline {pipeline-id}
az pipelines runs list --name {pipeline-name} --top 10
az pipelines runs list --branch main --status completed
```

### Show run details

```bash
az pipelines runs show --run-id {run-id}
az pipelines runs show --run-id {run-id} --open
```

### Pipeline artifacts

```bash
# List artifacts for a run
az pipelines runs artifact list --run-id {run-id}

# Download artifact
az pipelines runs artifact download \
  --artifact-name '{artifact-name}' \
  --path {local-path} \
  --run-id {run-id}

# Upload artifact
az pipelines runs artifact upload \
  --artifact-name '{artifact-name}' \
  --path {local-path} \
  --run-id {run-id}
```

### Pipeline run tags

```bash
# Add run tag
az pipelines runs tag add --run-id {run-id} --tags production v1.0

# List run tags
az pipelines runs tag list --run-id {run-id} --output table
```

## Builds

### List builds

```bash
az pipelines build list
az pipelines build list --definition {build-definition-id}
az pipelines build list --status completed --result succeeded
```

### Queue build

```bash
az pipelines build queue --definition {build-definition-id} --branch main
az pipelines build queue --definition {build-definition-id} --parameters version=1.0.0
```

### Show build details

```bash
az pipelines build show --id {build-id}
```

### Cancel build

```bash
az pipelines build cancel --id {build-id}
```

### Build tags

```bash
# Add build tag
az pipelines build tag add --build-id {build-id} --tags prod release

# Delete build tag
az pipelines build tag delete --build-id {build-id} --tag prod
```

## Build definitions

### List build definitions

```bash
az pipelines build definition list
az pipelines build definition list --name {definition-name}
```

### Show build definition

```bash
az pipelines build definition show --id {definition-id}
```

## Releases

### List releases

```bash
az pipelines release list
az pipelines release list --definition {release-definition-id}
```

### Create release

```bash
az pipelines release create --definition {release-definition-id}
az pipelines release create --definition {release-definition-id} --description "Release v1.0"
```

### Show release

```bash
az pipelines release show --id {release-id}
```

## Release definitions

### List release definitions

```bash
az pipelines release definition list
```

### Show release definition

```bash
az pipelines release definition show --id {definition-id}
```

## Universal packages (artifacts)

### Publish package

```bash
az artifacts universal publish \
  --feed {feed-name} \
  --name {package-name} \
  --version {version} \
  --path {package-path} \
  --project {project}
```

### Download package

```bash
az artifacts universal download \
  --feed {feed-name} \
  --name {package-name} \
  --version {version} \
  --path {download-path} \
  --project {project}
```
