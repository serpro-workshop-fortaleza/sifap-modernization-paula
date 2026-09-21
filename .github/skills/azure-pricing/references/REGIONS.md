# Azure region name reference

The Azure Retail Prices API requires lowercase `armRegionName` values without spaces. Use this table to map common region names to API values.

## Region mapping

| Display name | armRegionName |
|-------------|---------------|
| East US | `eastus` |
| East US 2 | `eastus2` |
| Central US | `centralus` |
| North Central US | `northcentralus` |
| South Central US | `southcentralus` |
| West Central US | `westcentralus` |
| West US | `westus` |
| West US 2 | `westus2` |
| West US 3 | `westus3` |
| Canada Central | `canadacentral` |
| Canada East | `canadaeast` |
| Brazil South | `brazilsouth` |
| North Europe | `northeurope` |
| West Europe | `westeurope` |
| UK South | `uksouth` |
| UK West | `ukwest` |
| France Central | `francecentral` |
| France South | `francesouth` |
| Germany West Central | `germanywestcentral` |
| Germany North | `germanynorth` |
| Switzerland North | `switzerlandnorth` |
| Switzerland West | `switzerlandwest` |
| Norway East | `norwayeast` |
| Norway West | `norwaywest` |
| Sweden Central | `swedencentral` |
| Italy North | `italynorth` |
| Poland Central | `polandcentral` |
| Spain Central | `spaincentral` |
| East Asia | `eastasia` |
| Southeast Asia | `southeastasia` |
| Japan East | `japaneast` |
| Japan West | `japanwest` |
| Australia East | `australiaeast` |
| Australia Southeast | `australiasoutheast` |
| Australia Central | `australiacentral` |
| Korea Central | `koreacentral` |
| Korea South | `koreasouth` |
| Central India | `centralindia` |
| South India | `southindia` |
| West India | `westindia` |
| UAE North | `uaenorth` |
| UAE Central | `uaecentral` |
| South Africa North | `southafricanorth` |
| South Africa West | `southafricawest` |
| Qatar Central | `qatarcentral` |

## Conversion rules

1. Remove all spaces.
2. Convert to lowercase.

Examples:

- "East US" → `eastus`
- "West Europe" → `westeurope`
- "Southeast Asia" → `southeastasia`
- "South Central US" → `southcentralus`

## Common aliases

Users may refer to regions informally. Map these names to the correct `armRegionName`:

| User says | Map to |
|-----------|---------|
| "US East", "Virginia" | `eastus` |
| "US West", "California" | `westus` |
| "Europe", "EU" | `westeurope` (default) |
| "UK", "London" | `uksouth` |
| "Asia", "Singapore" | `southeastasia` |
| "Japan", "Tokyo" | `japaneast` |
| "Australia", "Sydney" | `australiaeast` |
| "India", "Mumbai" | `centralindia` |
| "Korea", "Seoul" | `koreacentral` |
| "Brazil", "São Paulo" | `brazilsouth` |
| "Canada", "Toronto" | `canadacentral` |
| "Germany", "Frankfurt" | `germanywestcentral` |
| "France", "Paris" | `francecentral` |
| "Sweden", "Stockholm" | `swedencentral` |
