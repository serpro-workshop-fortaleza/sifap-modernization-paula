# Images and artifacts

## Contents

- [Import images (server-side copy)](#import-images-server-side-copy)
- [Repositories and tags](#repositories-and-tags)
- [Manifests](#manifests)
- [Untag versus delete](#untag-versus-delete)
- [Purge old images (acr purge)](#purge-old-images-acr-purge)
- [Lock images](#lock-images)
- [Retention policy and soft delete](#retention-policy-and-soft-delete)
- [Artifact cache (pull-through cache)](#artifact-cache-pull-through-cache)
- [Storage usage](#storage-usage)

---

## Import images (server-side copy)

Prefer this option over downloading and uploading with `docker pull` + `docker push`: it uses no local storage and keeps multi-architecture manifests intact:

```bash
# From a public registry
az acr import --name {registry} --source mcr.microsoft.com/hello-world:latest
az acr import --name {registry} --source docker.io/library/nginx:1.27 --image nginx:1.27

# From another ACR in the same tenant (by resource ID, no credentials required)
az acr import --name {registry} \
  --source app:v1 \
  --registry /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ContainerRegistry/registries/{src-registry}

# From a private registry with credentials
az acr import --name {registry} --source private.example.com/app:v1 \
  --username {user} --password {password}

# Overwrite an existing tag
az acr import --name {registry} --source docker.io/library/nginx:1.27 --image nginx:1.27 --force
```

## Repositories and tags

```bash
az acr repository list --name {registry} --output table

# Tags, newest to oldest, with digest and timestamps
az acr repository show-tags --name {registry} --repository app \
  --orderby time_desc --detail --output table

az acr repository show --name {registry} --image app:v1        # tag attributes
az acr repository show --name {registry} --repository app      # repository attributes
```

## Manifests

```bash
# Metadata for all manifests in a repository (digest, tags, size, and timestamps)
az acr manifest list-metadata --registry {registry} --name app --output table

# Metadata/raw content of a manifest
az acr manifest show-metadata --registry {registry} --name app:v1
az acr manifest show --registry {registry} --name app@sha256:{digest}

# Find untagged (orphaned) manifests
az acr manifest list-metadata --registry {registry} --name app \
  --query "[?tags==null].digest" --output tsv
```

## Untag versus delete

```bash
# Remove a tag: only the tag is removed; manifest + layers remain (pull by digest)
az acr repository untag --name {registry} --image app:v1

# Delete by tag: removes the entire manifest and ALL other tags pointing to it
az acr repository delete --name {registry} --image app:v1 --yes

# Delete by digest (precise)
az acr repository delete --name {registry} --image app@sha256:{digest} --yes

# Delete an entire repository
az acr repository delete --name {registry} --repository app --yes
```

> [!WARNING]
> Deleting by tag removes the underlying manifest. Other tags for the same image also disappear. To remove only a tag name, untag first.

## Purge old images (acr purge)

`acr purge` runs as an ACR Task (`mcr.microsoft.com/acr/acr-cli` container):

```bash
# ALWAYS do a dry run first
az acr run --registry {registry} \
  --cmd "acr purge --filter 'app:.*' --ago 30d --untagged --dry-run" /dev/null

# Delete tags older than 30 days matching the regex, plus untagged manifests
az acr run --registry {registry} \
  --cmd "acr purge --filter 'app:.*' --ago 30d --untagged" /dev/null

# Keep the five newest tags regardless of age
az acr run --registry {registry} \
  --cmd "acr purge --filter 'app:.*' --ago 0d --keep 5 --untagged" /dev/null

# Schedule as a nightly task
az acr task create --registry {registry} --name purge-old-images \
  --cmd "acr purge --filter 'app:.*' --ago 30d --untagged" \
  --context /dev/null --schedule "0 3 * * *"
```

`--filter` takes `repository:tag-regex` and can be repeated for multiple repositories.

> [!WARNING]
> `--untagged` ignores `--ago`: it deletes **all** untagged manifests, including those just created (images being pushed and reference artifacts). Omit `--untagged` if recent untagged manifests must remain. The age limit applies only to tagged images matching `--filter`.

## Lock images

Prevent critical tags from being overwritten or deleted (for example, released versions):

```bash
# Read-only: cannot be overwritten or deleted
az acr repository update --name {registry} --image app:v1 --write-enabled false

# Cannot be deleted, but can still be overwritten
az acr repository update --name {registry} --image app:v1 --delete-enabled false

# Unlock
az acr repository update --name {registry} --image app:v1 --write-enabled true --delete-enabled true
```

## Retention policy and soft delete

These are two separate policies that **cannot be enabled at the same time**. Retention policy requires **Premium**. Soft delete (preview) is available on **all tiers**, but does not support geo-replicated registries or registries with artifact cache.

```bash
# Retention policy (Premium): deletes untagged manifests after N days (0 = immediately)
az acr config retention update --registry {registry} \
  --status enabled --days 7 --type UntaggedManifests
az acr config retention show --registry {registry}

# Soft delete (preview, all tiers): recovers artifacts within 1-90 days
az acr config soft-delete update --registry {registry} --status enabled --days 7
az acr repository list-deleted --name {registry}
az acr manifest restore --registry {registry} --name app:v1
```

## Artifact cache (pull-through cache)

Cache upstream images (Docker Hub, MCR, GHCR, quay.io, and ECR Public) in the registry. This avoids rate limits and centralizes provenance:

```bash
# Optional: credentials for the authenticated upstream (secrets are in Key Vault)
az acr credential-set create --registry {registry} --name dockerhub-creds \
  --login-server docker.io \
  --username-id https://{vault}.vault.azure.net/secrets/dh-user \
  --password-id https://{vault}.vault.azure.net/secrets/dh-pass

# Cache rule: docker.io/library/* -> {registry}.azurecr.io/dockerhub/*
az acr cache create --registry {registry} --name dockerhub-cache \
  --source-repo "docker.io/library/*" --target-repo "dockerhub/*" \
  --cred-set dockerhub-creds

az acr cache list --registry {registry} --output table
```

Then `docker pull {registry}.azurecr.io/dockerhub/nginx:1.27` fetches the image through the cache.

## Storage usage

```bash
# Consumed storage versus SKU quota (Basic 10 GB/Standard 100 GB/Premium 500 GB included)
az acr show-usage --name {registry} --output table
```

Layers are deduplicated and shared across repositories. `show-usage` reports actual billable storage.
