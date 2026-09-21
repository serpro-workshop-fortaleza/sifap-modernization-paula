# Networking and geo-replication

## Contents

- [Geo-replication](#geo-replication)
- [Zone redundancy](#zone-redundancy)
- [Private endpoints (Private Link)](#private-endpoints-private-link)
- [Public network rules](#public-network-rules)
- [Dedicated data endpoints](#dedicated-data-endpoints)
- [Connected registry](#connected-registry)
- [Registry transfer pipelines](#registry-transfer-pipelines)

Geo-replication, private endpoints, public IP network rules, dedicated data endpoints, connected registries, and transfer pipelines require the **Premium** SKU. Zone redundancy is automatic on all tiers.

---

## Geo-replication

One registry, one login server, and images served from the nearest region:

```bash
az acr replication create --registry {registry} --location westeurope
az acr replication list --registry {registry} --output table
az acr replication show --registry {registry} --name westeurope
az acr replication delete --registry {registry} --name westeurope

# Regional endpoint status (useful for debugging HTTP notifications/replication)
az acr replication update --registry {registry} --name westeurope --region-endpoint-enabled true
```

Pushes are replicated automatically. Clients continue pulling images from `{registry}.azurecr.io`, and Traffic Manager routes to the nearest replica.

## Zone redundancy

Zone redundancy is **automatically enabled for all registries, on all tiers (Basic/Standard/Premium), in regions supporting availability zones**. No option, SKU, or action is needed, and it cannot be disabled. Geo-replicas in supported regions are also zone-redundant by default.

Do not rely on the `zoneRedundancy` property or the legacy `--zone-redundancy` option: the property is a deprecated artifact that may show `Disabled` even when the registry is fully zone-redundant. Registries in regions without availability zone support are the only exception. Migrate them (through `az acr import` or a transfer pipeline) to a supported region.

## Private endpoints (Private Link)

```bash
# 1. Disable network policies on the subnet if needed and create the endpoint
az network private-endpoint create --resource-group {rg} --name {registry}-pe \
  --vnet-name {vnet} --subnet {subnet} \
  --private-connection-resource-id $(az acr show --name {registry} --query id --output tsv) \
  --group-ids registry \
  --connection-name {registry}-pe-conn

# 2. Private DNS to resolve {registry}.azurecr.io to a private IP
az network private-dns zone create --resource-group {rg} --name privatelink.azurecr.io
az network private-dns link vnet create --resource-group {rg} \
  --zone-name privatelink.azurecr.io --name {registry}-dns-link --virtual-network {vnet} --registration-enabled false
az network private-endpoint dns-zone-group create --resource-group {rg} \
  --endpoint-name {registry}-pe --name default \
  --private-dns-zone privatelink.azurecr.io --zone-name registry

# 3. Optionally disable public access entirely
az acr update --name {registry} --public-network-enabled false

# Manage connection approvals
az acr private-endpoint-connection list --registry-name {registry} --output table
az acr private-endpoint-connection approve --registry-name {registry} --name {connection}
```

Notes:

- Each private endpoint creates records for the registry **and** its data endpoints (`{registry}.{region}.data.azurecr.io`). Geo-replicated registries need one data record per region.
- With public access disabled, default ACR Tasks agents cannot reach the registry. Use a dedicated agent pool attached to a VNet subnet or enable trusted services **and** the network bypass policy for tasks (see below).

## Public network rules

Restrict public access to specific IPs instead of making access fully private (or before doing so):

```bash
# Deny by default, then allow specific ranges
az acr update --name {registry} --default-action Deny
az acr network-rule add --name {registry} --ip-address 203.0.113.0/24
az acr network-rule list --name {registry}
az acr network-rule remove --name {registry} --ip-address 203.0.113.0/24

# Allow trusted Azure services (for example, Defender, ACI, and image import) through the firewall
az acr update --name {registry} --allow-trusted-services true
```

> [!WARNING]
> **Since June 1, 2025, `--allow-trusted-services` alone is NOT sufficient for ACR Tasks using a system-assigned managed identity**. Without the network bypass policy for tasks, runs receive 403 errors on network-restricted registries. Enable it explicitly:

```bash
az resource update \
  --namespace Microsoft.ContainerRegistry --resource-type registries \
  --name {registry} --resource-group {rg} \
  --api-version 2025-06-01-preview \
  --set properties.networkRuleBypassAllowedForTasks=true
```

Alternatives that avoid bypass entirely: run tasks on a VNet-attached agent pool or run `acr purge` locally with the [acr-cli binary](https://github.com/azure/acr-cli). Tasks using a user-assigned identity are not affected.

## Dedicated data endpoints

Provide stable, registry-specific FQDNs for layer downloads (`{registry}.{region}.data.azurecr.io`) instead of shared storage endpoints. This simplifies client-side firewall rules:

```bash
az acr update --name {registry} --data-endpoint-enabled true
az acr show-endpoints --name {registry}
```

## Connected registry

On-premises/IoT edge mirror of a cloud registry:

```bash
# The parent registry must have a dedicated data endpoint
az acr update --name {registry} --data-endpoint-enabled true

az acr connected-registry create --registry {registry} --name {connected-name} \
  --repository "app" "hello-world" \
  --mode ReadOnly            # or ReadWrite

az acr connected-registry list --registry {registry} --output table
az acr connected-registry get-settings --registry {registry} --name {connected-name} \
  --parent-protocol https --generate-password 1
az acr connected-registry deactivate --registry {registry} --name {connected-name}
```

## Registry transfer pipelines

Move images between disconnected clouds/tenants through storage blobs (`acrtransfer` extension):

```bash
az extension add --name acrtransfer

# Export from the source registry to a storage container (SAS token in Key Vault)
az acr export-pipeline create --resource-group {rg} --registry {src-registry} \
  --name export-pipe \
  --secret-uri https://{vault}.vault.azure.net/secrets/{sas-secret} \
  --storage-container-uri https://{account}.blob.core.windows.net/{container}

# Import at the destination
az acr import-pipeline create --resource-group {rg} --registry {dst-registry} \
  --name import-pipe \
  --secret-uri https://{vault}.vault.azure.net/secrets/{sas-secret} \
  --storage-container-uri https://{account}.blob.core.windows.net/{container}

# Run an export
az acr pipeline-run create --resource-group {rg} --registry {src-registry} \
  --pipeline export-pipe --name run1 --pipeline-type export \
  --artifacts app:v1 app:v2 --storage-blob transfer-blob-1
```

For simple copies within the same cloud, prefer `az acr import` (see `images-and-artifacts.md`).
