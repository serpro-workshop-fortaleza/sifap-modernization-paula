---
name: "azure-pricing"
description: "Use when someone asks about the cost of an Azure service, wants to compare SKU or regional prices, needs pricing data for an estimate, or asks about Copilot Studio pricing and agent credit consumption. Retrieves live retail prices from the public Azure Retail Prices API (no authentication) and estimates Copilot Studio credits. Triggers include \"Azure pricing\", \"how much does it cost\", \"compare SKU prices\", \"cost estimate\", and \"Copilot Studio credits\". To turn an existing workload into cost optimization work items, use az-cost-optimize."
---
# Azure pricing

Retrieve live Azure retail prices through the public Azure Retail Prices API. No authentication is required, only outbound HTTPS access to `prices.azure.com`.

> [!NOTE]
> This skill requires outbound web access (the built-in `web_fetch` tool or equivalent) to reach `prices.azure.com`. If web access is unavailable, disclose this and fall back to the cached rates in the reference files.

## When to Invoke

- "How much does a Standard_D4s_v5 VM cost in East US?"
- "Compare Blob Storage prices across regions."
- "Provide a monthly estimate for this architecture."
- "How many Copilot Credits will our agent consume per month?"

## API endpoint

```text
GET https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview
```

Append `$filter` as a query parameter using OData filter syntax. Always use `api-version=2023-01-01-preview` to include savings plan data.

## Procedure

If any aspect of the request is unclear, ask questions to identify the correct filter fields and values before calling the API.

1. **Identify the filter fields** in the request (service name, region, SKU, and price type).
2. **Convert the region** to a lowercase `armRegionName` without spaces (`East US` becomes `eastus`; `West Europe` becomes `westeurope`). See the complete list in [references/REGIONS.md](references/REGIONS.md).
3. **Build the filter string** using the fields below and fetch the URL.
4. **Process the `Items` array** in the JSON response. Each item contains the price and metadata.
5. **Follow pagination** through `NextPageLink` only if you need more than 1,000 results, which is rarely necessary.
6. **Calculate estimates** using the formulas in [references/COST-ESTIMATOR.md](references/COST-ESTIMATOR.md) to produce monthly and annual amounts.
7. **Present the results** in a summary table with service, SKU, region, unit price, and monthly and annual estimates.

## Filterable fields

| Field | Type | Example |
|---|---|---|
| `serviceName` | string (exact, case-sensitive) | `'Functions'`, `'Virtual Machines'`, `'Storage'` |
| `serviceFamily` | string (exact, case-sensitive) | `'Compute'`, `'Storage'`, `'Databases'`, `'AI + Machine Learning'` |
| `armRegionName` | string (exact, lowercase) | `'eastus'`, `'westeurope'`, `'southeastasia'` |
| `armSkuName` | string (exact) | `'Standard_D4s_v5'`, `'Standard_LRS'` |
| `skuName` | string (supports `contains`) | `'D4s v5'` |
| `priceType` | string | `'Consumption'`, `'Reservation'`, `'DevTestConsumption'` |
| `meterName` | string (supports `contains`) | `'Spot'` |

Use `eq` for equality, `and` to combine conditions, and `contains(field, 'value')` for partial matches.

## Filter examples

| Purpose | `$filter` value |
|---|---|
| Functions consumption prices in East US | `serviceName eq 'Functions' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |
| D4s v5 VMs in West Europe (consumption) | `armSkuName eq 'Standard_D4s_v5' and armRegionName eq 'westeurope' and priceType eq 'Consumption'` |
| All Storage prices in a region | `serviceName eq 'Storage' and armRegionName eq 'eastus'` |
| Spot price for a specific SKU | `armSkuName eq 'Standard_D4s_v5' and contains(meterName, 'Spot') and armRegionName eq 'eastus'` |
| One-year reservation price | `serviceName eq 'Virtual Machines' and priceType eq 'Reservation' and armRegionName eq 'eastus'` |
| Azure AI / OpenAI (Foundry Models) | `serviceName eq 'Foundry Models' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |
| Azure Cosmos DB | `serviceName eq 'Azure Cosmos DB' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |

## Complete query URL example

```text
https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&$filter=serviceName eq 'Functions' and armRegionName eq 'eastus' and priceType eq 'Consumption'
```

When building the URL, encode spaces as `%20` and quotes as `%27`.

## Key response fields

```json
{
  "Items": [
    {
      "retailPrice": 0.000016,
      "unitPrice": 0.000016,
      "currencyCode": "USD",
      "unitOfMeasure": "1 Execution",
      "serviceName": "Functions",
      "skuName": "Premium",
      "armRegionName": "eastus",
      "meterName": "vCPU Duration",
      "productName": "Functions",
      "priceType": "Consumption",
      "isPrimaryMeterRegion": true,
      "savingsPlan": [
        { "unitPrice": 0.000012, "term": "1 Year" },
        { "unitPrice": 0.000010, "term": "3 Years" }
      ]
    }
  ],
  "NextPageLink": null,
  "Count": 1
}
```

Use only items where `isPrimaryMeterRegion` is `true`, unless the user requests non-primary meters.

## Supported serviceFamily values

`Analytics`, `Compute`, `Containers`, `Data`, `Databases`, `Developer Tools`, `Integration`, `Internet of Things`, `Management and Governance`, `Networking`, `Security`, `Storage`, `Web`, `AI + Machine Learning`.

## Tips

- `serviceName` values are case-sensitive. When in doubt, filter by `serviceFamily` first to discover valid `serviceName` values.
- If results are empty, broaden the filter. Remove `priceType` or region restrictions first.
- Prices are in USD unless `currencyCode` is set in the request.
- For savings plan prices, look for the `savingsPlan` array in each item. It is only present with `2023-01-01-preview`.
- See common service names and their correct capitalization in [references/SERVICE-NAMES.md](references/SERVICE-NAMES.md).

## Troubleshooting

| Issue | Solution |
|---|---|
| Empty results | Broaden the filter. Remove `priceType` or `armRegionName` first |
| Incorrect service name | Use the `serviceFamily` filter to discover valid `serviceName` values |
| Missing savings plan data | Confirm that the URL contains `api-version=2023-01-01-preview` |
| URL errors | Check encoding: spaces as `%20` and quotes as `%27` |
| Too many results | Add more filter fields (region, SKU, priceType) to narrow the query |

## Copilot Studio agent usage estimation

Use this section when someone asks about Copilot Studio pricing, Copilot Credits, or agent usage costs.

### Key facts

- **1 Copilot Credit = 0.01 USD.**
- Credits are pooled across the tenant.
- Agents serving employees licensed for M365 Copilot receive classic answers, generative answers, and tenant graph grounding at no cost.
- Overage enforcement is triggered at 125% of prepaid capacity.

### Estimation steps

1. **Collect inputs**: agent type (employee/customer), user count, interactions per month, knowledge percentage, tenant graph percentage, and tool usage per session.
2. **Fetch current billing rates** with the web fetch tool so the estimate uses Microsoft's current prices.
3. **Process the retrieved content** to extract the current billing rate table (credits per capability type).
4. **Calculate the estimate** using `total_sessions = users * interactions_per_month` and the category rates below.
5. **Present the results** in a table broken down by category, with total credits and estimated cost in USD.

| Category | Calculation |
|---|---|
| Knowledge credits | Apply tenant graph grounding, generative answer, and classic answer rates. |
| Agent tool credits | Apply the agent action rate per tool call. |
| Agent flow credits | Apply the flow rate per 100 actions. |
| Prompt modification credits | Apply basic, standard, and premium rates per 10 responses. |

### Source URLs to fetch

| URL | Content |
|---|---|
| `https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management` | Rate table, billing examples, and overage rules |
| `https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing` | Licensing options, M365 Copilot inclusions, prepaid versus pay-as-you-go |

Fetch at least the first URL (billing rates) before calculating. See [references/COPILOT-STUDIO-RATES.md](references/COPILOT-STUDIO-RATES.md) for a cached snapshot of rates, formulas, and examples to use as a fallback when web fetching is unavailable.

## Output Template

Present retail prices in a table that states the source and assumptions:

```markdown
## Azure pricing: Standard_D4s_v5, eastus

| Service | SKU | Region | Unit price | Unit | Monthly estimate |
|---|---|---|---|---|---|
| Virtual Machines | Standard_D4s_v5 | eastus | $0.192 | 1 hour | ~$140 (730 h) |
| Virtual Machines | Standard_D4s_v5 (1-year savings plan) | eastus | $0.113 | 1 hour | ~$82 (730 h) |

Source: Azure Retail Prices API, api-version 2023-01-01-preview, retrieved on 2026-08-17. Prices in USD. Assumes 730 h/month and isPrimaryMeterRegion only.
```

## Quality Gate

- [ ] The region is converted to a valid lowercase `armRegionName`.
- [ ] The filter uses exact `serviceName`/`serviceFamily` values with the correct capitalization.
- [ ] Only items with `isPrimaryMeterRegion == true` are used, unless non-primary meters are requested.
- [ ] `api-version=2023-01-01-preview` is used to make savings plan data available when relevant.
- [ ] Monthly/annual estimates state their assumptions (hours, quantity) and cite the API and retrieval date.
- [ ] The currency is stated (USD unless otherwise specified).
- [ ] Copilot Studio estimates use freshly retrieved rates or explicitly disclose the use of cached rates.
