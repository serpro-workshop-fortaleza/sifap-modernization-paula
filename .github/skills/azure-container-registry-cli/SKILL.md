---
name: "azure-container-registry-cli"
description: "Use when working with Azure Container Registry, running az acr commands, or pushing, importing, building, or cleaning up container images in Azure. Covers registries, cloud builds, ACR Tasks, authentication, tokens, geo-replication, and networking. Triggers include \"az acr\", \"push image to ACR\", \"build image in Azure\", \"ACR authentication\", and \"container registry\"."
---
# Azure Container Registry CLI

Manage Azure Container Registry (ACR) resources with the Azure CLI's `az acr` command group. `az acr` ships with the Azure CLI core and requires no extension. The `acrtransfer` extension is needed only for export/import pipelines.

> [!NOTE]
> This skill depends on the **`az` CLI** being installed and authenticated. In this kit, provision the registry in Terraform (`azurerm_container_registry`, with the required `project`, `environment`, and `owner` tags) in `infra/`. Use `az acr` for operational tasks such as building, importing, tagging, and diagnosing images, not as the infrastructure system of record.

## When to Invoke

- "Push our Spring Boot image to Azure Container Registry."
- "Build a container image in Azure without a local Docker daemon."
- "How can AKS pull images from this registry without using the admin user?"
- "Clean up old tags to reduce ACR storage costs."

## Prerequisites

Install the Azure CLI, sign in, and select a subscription:

```bash
brew install azure-cli                                     # macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash     # Linux
winget install Microsoft.AzureCLI                          # Windows
az login
az account set --subscription {subscription-id}
```

## Quick start

```bash
az acr create --resource-group {rg} --name {registry} --sku Standard          # SKU: Basic | Standard | Premium
az acr login --name {registry}                                                # authenticates Docker/Podman
az acr build --registry {registry} --image app:v1 .                           # cloud build, no local Docker
az acr import --name {registry} --source mcr.microsoft.com/hello-world:latest  # server-side copy
az acr repository list --name {registry} --output table
az acr repository show-tags --name {registry} --repository app --orderby time_desc
az acr check-health --name {registry} --yes                                   # diagnoses connectivity
```

## Core principles

- **Prefer `az acr build`/ACR Tasks** over local `docker build` + `docker push`: builds run in Azure, work without a local daemon, and integrate with triggers.
- **Prefer `az acr import`** to move images between registries: the operation is server-side, faster, and requires no local storage.
- **Never enable the admin user in production.** Use Microsoft Entra identities (`AcrPull`/`AcrPush` RBAC roles or `Container Registry Repository Reader`/`Writer` on ABAC-enabled registries), repository-scoped tokens, or managed identities.
- **Premium-only features**: geo-replication, private endpoints, retention policies, connected registries, and agent pools. Repository-scoped tokens work on all tiers. Zone redundancy is automatic in supported regions.

## CLI structure

```text
az acr
├── create / delete / list / show / update   Registry lifecycle
├── login                  Docker credential helper (or --expose-token)
├── check-health / check-name / show-usage    Diagnostics and quota
├── build                  Cloud image build (quick task)
├── run                    Run a command or multi-step task once
├── task                   ACR Tasks (triggers, timers, logs, and runs)
├── agentpool              Dedicated task agent pools (Premium)
├── import                 Server-side image copy into the registry
├── repository             List/show/delete/untag repositories and tags; lock images
├── manifest               Manifest metadata, deletion, and OCI references
├── credential             Admin user credentials (avoid in production)
├── token / scope-map      Repository-scoped tokens (Premium)
├── replication            Geo-replication (Premium)
├── network-rule           IP network rules
├── private-endpoint-connection   Private Link approvals
├── config                 content-trust, retention, soft delete...
├── cache / credential-set Artifact cache rules (pull-through cache)
├── webhook                HTTP notifications for push/delete events
├── connected-registry     On-premises/IoT connected registries
└── export-pipeline / import-pipeline / pipeline-run   acrtransfer extension
```

## Reference files

Read the reference file relevant to the task. Each file contains complete command syntax and domain examples.

| File | When to read | Covers |
|---|---|---|
| [references/auth-and-security.md](references/auth-and-security.md) | Authentication failures, permissions, or image pull access for CI/CD or AKS | `az acr login` (including `--expose-token`), Entra RBAC roles, service principals, managed identities, `--attach-acr` for AKS, repository-scoped tokens and scope maps, admin user, and content trust |
| [references/build-and-tasks.md](references/build-and-tasks.md) | Image builds in Azure, automation, and CI triggers | `az acr build`, `az acr run`, multi-step task YAML, `az acr task` (git/base image/timer triggers, logs, and runs), and agent pools |
| [references/images-and-artifacts.md](references/images-and-artifacts.md) | Repository management, tags, cleanup, and storage cost | `az acr import`, repository and manifest commands, untag versus delete, cleanup (`acr purge`), image locking, retention policy, soft delete, artifact cache, and `show-usage` |
| [references/networking-and-geo.md](references/networking-and-geo.md) | Multiple regions, private access, and edge scenarios | Geo-replication, zone redundancy, private endpoints, network rules, dedicated data endpoints, connected registries, and registry transfer pipelines |

## Output Template

Provide an executable command plan that makes the identity model explicit:

```bash
az acr create --resource-group rg-sifap --name sifapregistry --sku Standard
az acr build --registry sifapregistry --image sifap-backend:$(git rev-parse --short HEAD) .
az acr repository show-tags --name sifapregistry --repository sifap-backend --output table
az role assignment create \
  --assignee <aks-kubelet-identity-object-id> \
  --role AcrPull \
  --scope $(az acr show --name sifapregistry --query id --output tsv)
```

Summarize what was done and the security posture:

```text
Registry: sifapregistry (Standard) in rg-sifap
Image: sifap-backend:<git-sha> built in Azure (no local Docker)
Access: AcrPull granted to the AKS kubelet managed identity; admin user disabled
```

## Quality Gate

- [ ] The registry SKU matches the need (Premium only when geo-replication, private endpoints, or scoped tokens are required).
- [ ] Whenever feasible, images are built with `az acr build`/ACR Tasks, not local `docker build` + `docker push`.
- [ ] The admin user is disabled; access uses an Entra identity (`AcrPull`/`AcrPush`), a managed identity, or a repository-scoped token.
- [ ] `az acr check-health --name {registry}` reports no errors.
- [ ] Image moves between registries use `az acr import` (server-side), not local pull and push operations.
- [ ] The registry resource is defined in Terraform in `infra/` with the required `project`, `environment`, and `owner` tags.
