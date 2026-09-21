# AzureRM Set-type attribute reference

This document provides an overview and explains how to maintain `azurerm_set_attributes.json`.

> **Last updated**: January 28, 2026

## Overview

`azurerm_set_attributes.json` is a definition file for attributes treated as Set-type by the AzureRM provider.
The `analyze_plan.py` script reads this JSON to identify "false-positive diffs" in Terraform plans.

### What are Set-type attributes?

Terraform's Set type is a collection that **does not guarantee order**.
As a result, when adding or removing elements, unchanged items may appear as "changed".
This is called a "false-positive diff".

## JSON file structure

### Basic format

```json
{
  "resources": {
    "azurerm_resource_type": {
      "attribute_name": "key_attribute"
    }
  }
}
```

- **key_attribute**: the attribute that uniquely identifies Set elements, such as `name` or `id`
- **null**: used when there is no key attribute (compares the entire element)

### Nested format

When a Set attribute contains another Set attribute:

```json
{
  "rewrite_rule_set": {
    "_key": "name",
    "rewrite_rule": {
      "_key": "name",
      "condition": "variable",
      "request_header_configuration": "header_name"
    }
  }
}
```

- **`_key`**: the key attribute of Set elements at this level
- **Other keys**: definitions of nested Set attributes

### Example: azurerm_application_gateway

```json
"azurerm_application_gateway": {
  "backend_address_pool": "name",           // Simple Set (key is name)
  "rewrite_rule_set": {                     // Nested Set
    "_key": "name",
    "rewrite_rule": {
      "_key": "name",
      "condition": "variable"
    }
  }
}
```

## Maintenance

### How to add new attributes

1. **Check the official documentation**

   Look up the resource in the [Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs). Check whether the attribute is listed as "Set of ...". Some resources, such as `azurerm_application_gateway`, have explicitly indicated Set attributes.

2. **Check the source code (most reliable)**

   Look up the resource on the [AzureRM provider's GitHub](https://github.com/hashicorp/terraform-provider-azurerm). Confirm `Type: pluginsdk.TypeSet` in the schema definition and identify attributes in the Set's `Schema` that can serve as `_key`.

3. **Add to the JSON**

   ```json
   "azurerm_new_resource": {
     "set_attribute": "key_attribute"
   }
   ```

**Test the addition:**

```bash
# Check with a real plan
python3 scripts/analyze_plan.py your_plan.json
```

### How to identify key attributes

| Common key attribute | Usage |
|---------------------|-------|
| `name` | Named blocks (most common) |
| `id` | Resource ID reference |
| `location` | Geographic location |
| `address` | Network address |
| `host_name` | Host name |
| `null` | When there is no key (compares the entire element) |

## Related tools

### analyze_plan.py

Analyzes Terraform plan JSON to identify false-positive diffs.

```bash
# Basic usage
terraform show -json plan.tfplan | python3 scripts/analyze_plan.py

# Read from a file
python3 scripts/analyze_plan.py plan.json

# Use a custom attributes file
python3 scripts/analyze_plan.py plan.json --attributes /path/to/custom.json
```

## Supported resources

Refer directly to `azurerm_set_attributes.json` for currently supported resources:

```bash
# List resources
jq '.resources | keys' azurerm_set_attributes.json
```

Key resources:

- `azurerm_application_gateway`: backend pools, listeners, rules, etc.
- `azurerm_firewall_policy_rule_collection_group`: rule collections
- `azurerm_frontdoor`: backend pools and routing
- `azurerm_network_security_group`: security rules
- `azurerm_virtual_network_gateway`: IP and VPN client configuration

## Notes

- Attribute behavior may vary by provider or API version
- New resources and attributes need to be added as they become available
- Defining all levels of deeply nested structures improves accuracy
