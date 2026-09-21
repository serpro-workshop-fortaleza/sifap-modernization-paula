# Authentication and security

## Contents

- [Individual authentication](#individual-authentication)
- [Microsoft Entra RBAC roles](#microsoft-entra-rbac-roles)
- [Service principals](#service-principals)
- [Managed identities](#managed-identities)
- [AKS integration](#aks-integration)
- [Repository-scoped tokens](#repository-scoped-tokens)
- [Admin user](#admin-user)
- [Content trust](#content-trust-deprecated)

---

## Individual authentication

```bash
# Default authentication: configures Docker/Podman credentials with your az login identity
az acr login --name {registry}

# Without the Docker daemon: gets an Entra token and pipes it to docker login
LOGIN_SERVER=$(az acr show --name {registry} --query loginServer --output tsv)
az acr login --name {registry} --expose-token --query accessToken --output tsv | \
  docker login $LOGIN_SERVER --username 00000000-0000-0000-0000-000000000000 --password-stdin
```

Notes:

- `az acr login` tokens are valid for three hours. Rerun when they expire.
- Resolve the login server with `az acr show --name {registry} --query loginServer --output tsv` instead of hardcoding it. It is usually `{registry}.azurecr.io`, but sovereign clouds use other suffixes and registries with domain name label scope receive a hash suffix.

## Microsoft Entra RBAC roles

The applicable data-plane roles depend on the registry's **role assignment permissions mode**. Check it first:

```bash
az acr show --name {registry} --query roleAssignmentMode --output tsv
# LegacyRegistryPermissions  -> use AcrPull/AcrPush/AcrDelete
# AbacRepositoryPermissions  -> use Container Registry Repository Reader/Writer/Contributor
```

**Legacy mode (RBAC Registry Permissions):**

| Role | Permissions |
|---|---|
| `AcrPull` | Pull images |
| `AcrPush` | Pull + push images |
| `AcrDelete` | Delete images |
| `AcrImageSigner` | Sign images (content trust) |
| `Contributor`/`Owner` | Full control-plane management + push/pull |

**ABAC mode (RBAC Registry + ABAC Repository Permissions):** `AcrPull`/`AcrPush`/`AcrDelete` **are not supported**, and `Owner`/`Contributor`/`Reader` grant control-plane access only. Instead, use:

| Role | Permissions |
|---|---|
| `Container Registry Repository Reader` | Reads images, tags, and metadata (add ABAC conditions to scope to repositories) |
| `Container Registry Repository Writer` | Reads + writes/updates |
| `Container Registry Repository Contributor` | Reads + writes + deletes |
| `Container Registry Repository Catalog Lister` | Lists repositories; assign only when the identity needs to enumerate the catalog (for example, `az acr repository list`). Not required to pull/push images from known repositories |

```bash
# Get the registry resource ID
ACR_ID=$(az acr show --name {registry} --query id --output tsv)

# Grant image pull access to a user, group, service principal, or managed identity
az role assignment create --assignee {principal-id} --scope $ACR_ID --role AcrPull

# List who has access
az role assignment list --scope $ACR_ID --output table
```

## Service principals

For CI/CD systems that cannot use OIDC/managed identity:

```bash
# Create a service principal scoped to image pulls only
ACR_ID=$(az acr show --name {registry} --query id --output tsv)
az ad sp create-for-rbac --name {sp-name} --scopes $ACR_ID --role AcrPull

# Docker login with the principal: pass the secret through stdin, never as an argument
# (printf with a quoted variable preserves spaces and glob characters exactly)
printf '%s' "$SP_PASSWORD" | docker login $LOGIN_SERVER --username {appId} --password-stdin
```

Where possible, prefer federated credentials (OIDC) over service principal passwords in GitHub Actions/Azure DevOps.

## Managed identities

For Azure compute (VM, App Service, Container Apps, and Functions):

```bash
# Assign a system-managed identity and grant image pull access
az vm identity assign --name {vm} --resource-group {rg}
PRINCIPAL_ID=$(az vm show --name {vm} --resource-group {rg} --query identity.principalId --output tsv)
az role assignment create --assignee $PRINCIPAL_ID --scope $ACR_ID --role AcrPull
```

Then App Service/Container Apps pull images with options such as `--assign-identity` + `--acr-identity` from their own CLIs, without needing a registry password.

## AKS integration

```bash
# Attach during cluster creation
az aks create --name {cluster} --resource-group {rg} --attach-acr {registry}

# Attach/detach an existing cluster (grants AcrPull to the kubelet identity)
az aks update --name {cluster} --resource-group {rg} --attach-acr {registry}
az aks update --name {cluster} --resource-group {rg} --detach-acr {registry}

# Validate whether the cluster can access the registry
az aks check-acr --name {cluster} --resource-group {rg} --acr {registry}.azurecr.io
```

`--attach-acr` requires Owner or User Access Administrator on the registry. To attach across subscriptions, pass the full ACR resource ID.

> [!WARNING]
> `--attach-acr` assigns `AcrPull`, which **is not supported on ABAC-enabled registries** (`roleAssignmentMode` = `AbacRepositoryPermissions`). On these registries, manually assign ABAC roles to the kubelet identity:

```bash
ACR_ID=$(az acr show --name {registry} --query id --output tsv)
KUBELET_ID=$(az aks show --name {cluster} --resource-group {rg} \
  --query identityProfile.kubeletidentity.objectId --output tsv)
az role assignment create --assignee $KUBELET_ID --scope $ACR_ID \
  --role "Container Registry Repository Reader"
# "Container Registry Repository Catalog Lister" is NOT required to pull images;
# add it only if the identity needs to list repositories
```

## Repository-scoped tokens

Available on all service tiers. These are granular credentials that do not use Entra (for example, for external partners or IoT devices):

```bash
# 1. Create a scope map (actions: content/read, content/write, content/delete, metadata/read, metadata/write)
az acr scope-map create --name {scope-map} --registry {registry} \
  --repository app content/read metadata/read \
  --description "Pull-only access to app images"

# 2. Create a token linked to the scope map
az acr token create --name {token} --registry {registry} --scope-map {scope-map}

# 3. Generate/rotate passwords (up to two, with optional expiration)
az acr token credential generate --name {token} --registry {registry} --password1 --expiration-in-days 30

# Token authentication: pass the password through stdin, never as an argument
printf '%s' "$TOKEN_PWD" | docker login $LOGIN_SERVER --username {token} --password-stdin

# Disable or delete
az acr token update --name {token} --registry {registry} --status disabled
az acr token delete --name {token} --registry {registry} --yes
```

## Admin user

Single account with full push/pull across the registry, without per-user auditing. **Keep it disabled in production**:

```bash
az acr update --name {registry} --admin-enabled false   # recommended
az acr credential show --name {registry}                # shows username/passwords (if enabled)
az acr credential renew --name {registry} --password-name password2   # rotates
```

Legitimate uses: quick local tests and services that accept only username/password and cannot use tokens.

## Content trust (deprecated)

Docker Content Trust (DCT) is being deprecated: **since May 31, 2026, it cannot be enabled on new registries** (or registries that never enabled it) and will be fully removed on March 31, 2028. Do not configure DCT. Instead, sign images with **Notation (Notary Project)** and store signatures as OCI artifacts. See "Transition from Docker Content Trust to Notary Project" in the ACR documentation.

```bash
# Legacy DCT registries only: inspect or disable the existing configuration
az acr config content-trust show --registry {registry}
az acr config content-trust update --registry {registry} --status disabled
```

Legacy DCT signers needed `AcrImageSigner` in addition to `AcrPush`.
