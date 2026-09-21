# Builds and ACR Tasks

## Contents

- [Quick build (az acr build)](#quick-build-az-acr-build)
- [Run a command or multi-step task once (az acr run)](#run-a-command-or-multi-step-task-once-az-acr-run)
- [ACR Tasks (az acr task)](#acr-tasks-az-acr-task)
- [Triggers](#triggers)
- [Multi-step task YAML](#multi-step-task-yaml)
- [Agent pools](#agent-pools)

---

## Quick build (az acr build)

Builds in Azure and pushes to the registry without requiring a local Docker daemon:

```bash
# Build from the current directory and push the image
az acr build --registry {registry} --image app:v1 .

# Custom Dockerfile, build arguments, and target platform
az acr build --registry {registry} --image app:v1 \
  --file docker/Dockerfile.prod \
  --build-arg VERSION=1.2.3 \
  --platform linux/amd64 .

# Cross-platform: each build produces ONE single-architecture image for the target platform
az acr build --registry {registry} --image app:v1-arm64 --platform linux/arm64 .
# For a truly multiarch image, build once per platform with architecture-specific
# tags; then assemble and push a manifest list (docker manifest create/push
# or local docker buildx)

# Build directly from a Git repository (no local clone)
az acr build --registry {registry} --image app:v1 https://github.com/{org}/{repo}.git#{branch}:{folder}

# Build without pushing (validation only)
az acr build --registry {registry} --image app:test --no-push .
```

Notes:

- The build context is uploaded. Use `.dockerignore` to keep it small.
- Use a unique tag per build (git SHA or run ID). Avoid relying on `latest`.

## Run a command or multi-step task once (az acr run)

```bash
# Run a container command on the registry task runner (/dev/null context = no upload)
az acr run --registry {registry} --cmd '{registry}.azurecr.io/app:v1' /dev/null

# Run a multi-step task file in the current directory
az acr run --registry {registry} --file acb.yaml .
```

## ACR Tasks (az acr task)

Persistent build definitions that can be triggered:

```bash
# Create a task that builds on each commit to main
az acr task create --registry {registry} --name build-app \
  --image "app:{{.Run.ID}}" \
  --context https://github.com/{org}/{repo}.git#main \
  --file Dockerfile \
  --git-access-token {pat} \
  --commit-trigger-enabled true \
  --base-image-trigger-enabled true

# Manually trigger, list, and inspect
az acr task run --registry {registry} --name build-app
az acr task list --registry {registry} --output table
az acr task list-runs --registry {registry} --name build-app --output table
az acr task logs --registry {registry} --name build-app        # latest run
az acr task logs --registry {registry} --run-id {run-id}

# Update/disable/delete
az acr task update --registry {registry} --name build-app --image "app:{{.Run.ID}}"
az acr task update --registry {registry} --name build-app --status Disabled
az acr task delete --registry {registry} --name build-app --yes
```

Useful run variables for `--image`: `{{.Run.ID}}`, `{{.Run.Commit}}`, `{{.Run.Branch}}`, `{{.Run.Date}}`.

> [!WARNING]
> On **ABAC-enabled registries** (`roleAssignmentMode` = `AbacRepositoryPermissions`), tasks and quick builds/runs do not have default access to the source registry. Pass `--source-acr-auth-id [caller]` to `az acr build`/`az acr run` and `--source-acr-auth-id [system]` (or the resource ID of a user-assigned identity) to `az acr task create`/`update`. Then grant that identity the `Container Registry Repository ...` roles. Before referencing it, confirm that the task actually has that identity: add `--assign-identity [system]` during creation or run `az acr task identity assign` on an existing task.

## Triggers

```bash
# Timer trigger (cron in UTC), for example, nightly rebuild
az acr task timer add --registry {registry} --name build-app \
  --timer-name nightly --schedule "0 2 * * *"
az acr task timer list --registry {registry} --name build-app
az acr task timer remove --registry {registry} --name build-app --timer-name nightly
```

- **Commit trigger**: rebuilds after a push to the monitored branch (`--commit-trigger-enabled`).
- **Base image trigger**: automatically rebuilds when the base image (for example, a patched image from `mcr.microsoft.com`) is updated (`--base-image-trigger-enabled`). Essential for operating system and framework patches.
- **Timer trigger**: cron schedules; also the standard way to schedule cleanup with `acr purge` (see `images-and-artifacts.md`).

Tasks that access other registries or Azure resources can use an identity:

```bash
az acr task identity assign --registry {registry} --name build-app   # system-assigned
az acr task credential add --registry {registry} --name build-app \
  --login-server {other-registry}.azurecr.io --use-identity [system]
```

## Multi-step task YAML

`acb.yaml`: builds, tests, and pushes the image only on success:

```yaml
version: v1.1.0
steps:
  - build: -t $Registry/app:{{.Run.ID}} -f Dockerfile .
  - cmd: $Registry/app:{{.Run.ID}} run-tests
  - push:
      - $Registry/app:{{.Run.ID}}
```

```bash
# Run once
az acr run --registry {registry} --file acb.yaml .

# Or create a triggerable task from the YAML
az acr task create --registry {registry} --name build-test-push \
  --file acb.yaml \
  --context https://github.com/{org}/{repo}.git#main \
  --git-access-token {pat}
```

## Agent pools

Premium SKU. Dedicated task compute for more CPU or to use one of the two supported ways to run tasks against a network-restricted registry. The other way combines trusted services and the network bypass policy for tasks. See `networking-and-geo.md`:

```bash
az acr agentpool create --registry {registry} --name pool1 --tier S2   # S1/S2/S3/I6

# In the firewall/VNet scenario, the pool MUST be attached to a subnet that can reach
# the registry's private endpoint; without --subnet-id, it runs outside the VNet
az acr agentpool create --registry {registry} --name pool1 --tier S2 \
  --subnet-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}/subnets/{subnet}

az acr agentpool list --registry {registry} --output table

# Target the agent pool
az acr build --registry {registry} --agent-pool pool1 --image app:v1 .
az acr task create --registry {registry} --name build-app --agent-pool pool1 ...
```
