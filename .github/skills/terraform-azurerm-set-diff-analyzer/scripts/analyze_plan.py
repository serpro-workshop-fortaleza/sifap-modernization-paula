#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terraform plan analyzer for AzureRM Set-type attributes

Analyzes Terraform plan JSON output to distinguish:
- Order-only changes (false positives) in Set-type attributes
- Actual additions, deletions, and modifications

Usage:
    terraform show -json plan.tfplan | python analyze_plan.py
    python analyze_plan.py plan.json
    python analyze_plan.py plan.json --format json --exit-code

For use in CI/CD pipelines, see README.md in this directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Exit codes for the --exit-code option
EXIT_NO_CHANGES = 0
EXIT_ORDER_ONLY = 0  # Order-only changes are not actual changes
EXIT_SET_CHANGES = 1  # Actual changes in Set attributes
EXIT_RESOURCE_REPLACE = 2  # Resource replacement (more severe)
EXIT_ERROR = 3

# Default path to the external attributes JSON file (relative to this script)
DEFAULT_ATTRIBUTES_PATH = (
    Path(__file__).parent.parent / "references" / "azurerm_set_attributes.json"
)


# Global configuration
class Config:
    """Global analyzer configuration."""

    ignore_case: bool = False
    quiet: bool = False
    verbose: bool = False
    warnings: List[str] = []


CONFIG = Config()


def warn(message: str) -> None:
    """Adds a warning message."""
    CONFIG.warnings.append(message)
    if CONFIG.verbose:
        print(f"Warning: {message}", file=sys.stderr)


def load_set_attributes(path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Loads Set-type attributes from an external JSON file."""
    attributes_path = path or DEFAULT_ATTRIBUTES_PATH

    try:
        with open(attributes_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("resources", {})
    except FileNotFoundError:
        warn(f"Attributes file not found: {attributes_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in attributes file: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


# Global variable storing loaded attributes (initialized in main)
AZURERM_SET_ATTRIBUTES: Dict[str, Any] = {}


def get_attr_config(attr_def: Any) -> tuple:
    """
    Parses the attribute definition and returns (key_attr, nested_attrs).

    The attribute definition can be:
    - str: simple key attribute (for example, "name")
    - None/null: no key attribute
    - dict: nested structure with "_key" and nested attributes
    """
    if attr_def is None:
        return (None, {})
    if isinstance(attr_def, str):
        return (attr_def, {})
    if isinstance(attr_def, dict):
        key_attr = attr_def.get("_key")
        nested_attrs = {k: v for k, v in attr_def.items() if k != "_key"}
        return (key_attr, nested_attrs)
    return (None, {})


@dataclass
class SetAttributeChange:
    """Represents a change in a Set-type attribute."""

    attribute_name: str
    path: str = (
        ""  # Full path of nested attributes (for example, "rewrite_rule_set.rewrite_rule")
    )
    order_only_count: int = 0
    added: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)
    modified: List[tuple] = field(default_factory=list)
    nested_changes: List["SetAttributeChange"] = field(default_factory=list)
    # For primitive sets (arrays of strings or numbers)
    is_primitive: bool = False
    primitive_added: List[Any] = field(default_factory=list)
    primitive_removed: List[Any] = field(default_factory=list)


@dataclass
class ResourceChange:
    """Represents changes in a single resource."""

    address: str
    resource_type: str
    actions: List[str] = field(default_factory=list)
    set_changes: List[SetAttributeChange] = field(default_factory=list)
    other_changes: List[str] = field(default_factory=list)
    is_replace: bool = False
    is_create: bool = False
    is_delete: bool = False


@dataclass
class AnalysisResult:
    """Overall analysis result."""

    resources: List[ResourceChange] = field(default_factory=list)
    order_only_count: int = 0
    actual_set_changes_count: int = 0
    replace_count: int = 0
    create_count: int = 0
    delete_count: int = 0
    other_changes_count: int = 0
    warnings: List[str] = field(default_factory=list)


def get_element_key(element: Dict[str, Any], key_attr: Optional[str]) -> str:
    """Extracts the key value from a Set element."""
    if key_attr and key_attr in element:
        val = element[key_attr]
        if CONFIG.ignore_case and isinstance(val, str):
            return val.lower()
        return str(val)
    # Falls back to the hash of sorted items for elements without a key attribute
    return str(hash(json.dumps(element, sort_keys=True)))


def normalize_value(val: Any) -> Any:
    """Normalizes values for comparison (treats empty strings and None as equivalent)."""
    if val == "" or val is None:
        return None
    if isinstance(val, list) and len(val) == 0:
        return None
    # Normalizes numeric types (int versus float)
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


def normalize_for_comparison(val: Any) -> Any:
    """Normalizes the value for comparison, including the case-insensitive option."""
    val = normalize_value(val)
    if CONFIG.ignore_case and isinstance(val, str):
        return val.lower()
    return val


def values_equivalent(before_val: Any, after_val: Any) -> bool:
    """Checks whether two values are effectively equivalent."""
    return normalize_for_comparison(before_val) == normalize_for_comparison(after_val)


def compare_elements(
    before: Dict[str, Any], after: Dict[str, Any], nested_attrs: Dict[str, Any] = None
) -> tuple:
    """
    Compares two elements and returns (simple_diffs, nested_set_attrs).

    simple_diffs: differences in non-Set attributes
    nested_set_attrs: list of (attr_name, before_val, after_val, attr_def) for nested Sets
    """
    nested_attrs = nested_attrs or {}
    simple_diffs = {}
    nested_set_attrs = []

    all_keys = set(before.keys()) | set(after.keys())

    for key in all_keys:
        before_val = before.get(key)
        after_val = after.get(key)

        # Checks whether this is a nested Set attribute
        if key in nested_attrs:
            if before_val != after_val:
                nested_set_attrs.append((key, before_val, after_val, nested_attrs[key]))
        elif not values_equivalent(before_val, after_val):
            simple_diffs[key] = {"before": before_val, "after": after_val}

    return (simple_diffs, nested_set_attrs)


def analyze_primitive_set(
    before_list: Optional[List[Any]],
    after_list: Optional[List[Any]],
    attr_name: str,
    path: str = "",
) -> SetAttributeChange:
    """Analyzes changes in a primitive Set (array of strings or numbers)."""
    full_path = f"{path}.{attr_name}" if path else attr_name
    change = SetAttributeChange(
        attribute_name=attr_name, path=full_path, is_primitive=True
    )

    before_set = set(before_list) if before_list else set()
    after_set = set(after_list) if after_list else set()

    # Applies case-insensitive comparison if configured
    if CONFIG.ignore_case:
        before_normalized = {v.lower() if isinstance(v, str) else v for v in before_set}
        after_normalized = {v.lower() if isinstance(v, str) else v for v in after_set}
    else:
        before_normalized = before_set
        after_normalized = after_set

    removed = before_normalized - after_normalized
    added = after_normalized - before_normalized

    if removed:
        change.primitive_removed = list(removed)
    if added:
        change.primitive_added = list(added)

    # Elements present in both (order-only change)
    common = before_normalized & after_normalized
    if common and not removed and not added:
        change.order_only_count = len(common)

    return change


def analyze_set_attribute(
    before_list: Optional[List[Dict[str, Any]]],
    after_list: Optional[List[Dict[str, Any]]],
    key_attr: Optional[str],
    attr_name: str,
    nested_attrs: Dict[str, Any] = None,
    path: str = "",
    after_unknown: Optional[Dict[str, Any]] = None,
) -> SetAttributeChange:
    """Analyzes changes in a Set-type attribute, including nested Sets."""
    full_path = f"{path}.{attr_name}" if path else attr_name
    change = SetAttributeChange(attribute_name=attr_name, path=full_path)
    nested_attrs = nested_attrs or {}

    before_list = before_list or []
    after_list = after_list or []

    # Handles non-list values (single element)
    if not isinstance(before_list, list):
        before_list = [before_list] if before_list else []
    if not isinstance(after_list, list):
        after_list = [after_list] if after_list else []

    # Checks whether this is a primitive set (non-dict elements)
    has_primitive_before = any(
        not isinstance(e, dict) for e in before_list if e is not None
    )
    has_primitive_after = any(
        not isinstance(e, dict) for e in after_list if e is not None
    )

    if has_primitive_before or has_primitive_after:
        # Handles primitive sets
        return analyze_primitive_set(before_list, after_list, attr_name, path)

    # Creates maps indexed by the key attribute
    before_map: Dict[str, Dict[str, Any]] = {}
    after_map: Dict[str, Dict[str, Any]] = {}

    # Detects duplicate keys
    for e in before_list:
        if isinstance(e, dict):
            key = get_element_key(e, key_attr)
            if key in before_map:
                warn(f"Duplicate key '{key}' in the before state of {full_path}")
            before_map[key] = e

    for e in after_list:
        if isinstance(e, dict):
            key = get_element_key(e, key_attr)
            if key in after_map:
                warn(f"Duplicate key '{key}' in the after state of {full_path}")
            after_map[key] = e

    before_keys = set(before_map.keys())
    after_keys = set(after_map.keys())

    # Finds removed elements
    for key in before_keys - after_keys:
        display_key = key if key_attr else "(element)"
        change.removed.append(display_key)

    # Finds added elements
    for key in after_keys - before_keys:
        display_key = key if key_attr else "(element)"
        change.added.append(display_key)

    # Compares common elements
    for key in before_keys & after_keys:
        before_elem = before_map[key]
        after_elem = after_map[key]

        if before_elem == after_elem:
            # Exact match: order-only change
            change.order_only_count += 1
        else:
            # Content changed: checks for significant differences
            simple_diffs, nested_set_list = compare_elements(
                before_elem, after_elem, nested_attrs
            )

            # Processes nested Set attributes recursively
            for nested_name, nested_before, nested_after, nested_def in nested_set_list:
                nested_key, sub_nested = get_attr_config(nested_def)
                nested_change = analyze_set_attribute(
                    nested_before,
                    nested_after,
                    nested_key,
                    nested_name,
                    sub_nested,
                    full_path,
                )
                if (
                    nested_change.order_only_count > 0
                    or nested_change.added
                    or nested_change.removed
                    or nested_change.modified
                    or nested_change.nested_changes
                    or nested_change.primitive_added
                    or nested_change.primitive_removed
                ):
                    change.nested_changes.append(nested_change)

            if simple_diffs:
                # There are actual differences in non-nested attributes
                display_key = key if key_attr else "(element)"
                change.modified.append((display_key, simple_diffs))
            elif not nested_set_list:
                # Only null versus empty differences: treats as an order-only change
                change.order_only_count += 1

    return change


def analyze_resource_change(
    resource_change: Dict[str, Any],
    include_filter: Optional[List[str]] = None,
    exclude_filter: Optional[List[str]] = None,
) -> Optional[ResourceChange]:
    """Analyzes the change to a single resource in the Terraform plan."""
    resource_type = resource_change.get("type", "")
    address = resource_change.get("address", "")
    change = resource_change.get("change", {})
    actions = change.get("actions", [])

    # Skips when there is no change or the resource is not an AzureRM resource
    if actions == ["no-op"] or not resource_type.startswith("azurerm_"):
        return None

    # Applies filters
    if include_filter:
        if not any(f in resource_type for f in include_filter):
            return None
    if exclude_filter:
        if any(f in resource_type for f in exclude_filter):
            return None

    before = change.get("before") or {}
    after = change.get("after") or {}
    after_unknown = change.get("after_unknown") or {}
    before_sensitive = change.get("before_sensitive") or {}
    after_sensitive = change.get("after_sensitive") or {}

    # Determines the action type
    is_create = actions == ["create"]
    is_delete = actions == ["delete"]
    is_replace = "delete" in actions and "create" in actions

    result = ResourceChange(
        address=address,
        resource_type=resource_type,
        actions=actions,
        is_replace=is_replace,
        is_create=is_create,
        is_delete=is_delete,
    )

    # Skips detailed Set analysis on creation/deletion (all elements are new/removed)
    if is_create or is_delete:
        return result

    # Gets the Set attributes for this resource type
    set_attrs = AZURERM_SET_ATTRIBUTES.get(resource_type, {})

    # Analyzes Set-type attributes
    analyzed_attrs: Set[str] = set()
    for attr_name, attr_def in set_attrs.items():
        before_val = before.get(attr_name)
        after_val = after.get(attr_name)

        # Warns about sensitive attributes
        if attr_name in before_sensitive or attr_name in after_sensitive:
            if before_sensitive.get(attr_name) or after_sensitive.get(attr_name):
                warn(
                    f"Attribute '{attr_name}' in {address} contains sensitive values (comparison may be incomplete)"
                )

        # Skips if the attribute is absent or unchanged
        if before_val is None and after_val is None:
            continue
        if before_val == after_val:
            continue

        # Analyzes only if it is a list (Set in Terraform) or has changed
        if not isinstance(before_val, list) and not isinstance(after_val, list):
            continue

        # Parses the attribute definition to get the key and nested attributes
        key_attr, nested_attrs = get_attr_config(attr_def)

        # Gets after_unknown for this attribute
        attr_after_unknown = after_unknown.get(attr_name)

        set_change = analyze_set_attribute(
            before_val,
            after_val,
            key_attr,
            attr_name,
            nested_attrs,
            after_unknown=attr_after_unknown,
        )

        # Includes only when there are actual findings
        if (
            set_change.order_only_count > 0
            or set_change.added
            or set_change.removed
            or set_change.modified
            or set_change.nested_changes
            or set_change.primitive_added
            or set_change.primitive_removed
        ):
            result.set_changes.append(set_change)
            analyzed_attrs.add(attr_name)

    # Finds other (non-Set) changes
    all_keys = set(before.keys()) | set(after.keys())
    for key in all_keys:
        if key in analyzed_attrs:
            continue
        if key.startswith("_"):  # Skips internal attributes
            continue
        before_val = before.get(key)
        after_val = after.get(key)
        if before_val != after_val:
            result.other_changes.append(key)

    return result


def collect_all_changes(set_change: SetAttributeChange, prefix: str = "") -> tuple:
    """
    Recursively collects order-only and actual changes in the nested structure.
    Returns (order_only_list, actual_change_list)
    """
    order_only = []
    actual = []

    display_name = (
        f"{prefix}{set_change.attribute_name}" if prefix else set_change.attribute_name
    )

    has_actual_change = (
        set_change.added
        or set_change.removed
        or set_change.modified
        or set_change.primitive_added
        or set_change.primitive_removed
    )

    if set_change.order_only_count > 0 and not has_actual_change:
        order_only.append((display_name, set_change))
    elif has_actual_change:
        actual.append((display_name, set_change))

    # Processes nested changes
    for nested in set_change.nested_changes:
        nested_order, nested_actual = collect_all_changes(nested, f"{display_name}.")
        order_only.extend(nested_order)
        actual.extend(nested_actual)

    return (order_only, actual)


def format_set_change(change: SetAttributeChange, indent: int = 0) -> List[str]:
    """Formats a single SetAttributeChange for output."""
    lines = []
    prefix = "  " * indent

    # Handles primitive sets
    if change.is_primitive:
        if change.primitive_added:
            lines.append(f"{prefix}**Added:**")
            for item in change.primitive_added:
                lines.append(f"{prefix}  - {item}")
        if change.primitive_removed:
            lines.append(f"{prefix}**Removed:**")
            for item in change.primitive_removed:
                lines.append(f"{prefix}  - {item}")
        if change.order_only_count > 0:
            lines.append(f"{prefix}**Order only:** {change.order_only_count} elements")
        return lines

    if change.added:
        lines.append(f"{prefix}**Added:**")
        for item in change.added:
            lines.append(f"{prefix}  - {item}")

    if change.removed:
        lines.append(f"{prefix}**Removed:**")
        for item in change.removed:
            lines.append(f"{prefix}  - {item}")

    if change.modified:
        lines.append(f"{prefix}**Modified:**")
        for item_key, diffs in change.modified:
            lines.append(f"{prefix}  - {item_key}:")
            for diff_key, diff_val in diffs.items():
                before_str = json.dumps(diff_val["before"], ensure_ascii=False)
                after_str = json.dumps(diff_val["after"], ensure_ascii=False)
                lines.append(f"{prefix}    - {diff_key}: {before_str} → {after_str}")

    if change.order_only_count > 0:
        lines.append(f"{prefix}**Order only:** {change.order_only_count} elements")

    # Formats nested changes
    for nested in change.nested_changes:
        if (
            nested.added
            or nested.removed
            or nested.modified
            or nested.nested_changes
            or nested.primitive_added
            or nested.primitive_removed
        ):
            lines.append(f"{prefix}**Nested attribute `{nested.attribute_name}`:**")
            lines.extend(format_set_change(nested, indent + 1))

    return lines


def format_markdown_output(result: AnalysisResult) -> str:
    """Formats analysis results as Markdown."""
    lines = ["# Terraform Plan Analysis Results", ""]
    lines.append(
        'Analyzes changes in AzureRM Set-type attributes and identifies order-only "false-positive diffs".'
    )
    lines.append("")

    # Categorizes changes (including nested changes)
    order_only_changes: List[tuple] = []
    actual_set_changes: List[tuple] = []
    replace_resources: List[ResourceChange] = []
    create_resources: List[ResourceChange] = []
    delete_resources: List[ResourceChange] = []
    other_changes: List[tuple] = []

    for res in result.resources:
        if res.is_replace:
            replace_resources.append(res)
        elif res.is_create:
            create_resources.append(res)
        elif res.is_delete:
            delete_resources.append(res)

        for set_change in res.set_changes:
            order_only, actual = collect_all_changes(set_change)
            for name, change in order_only:
                order_only_changes.append((res.address, name, change))
            for name, change in actual:
                actual_set_changes.append((res.address, name, change))

        if res.other_changes:
            other_changes.append((res.address, res.other_changes))

    # Section: order-only changes (false positives)
    lines.append("## 🟢 Order-Only Changes (No Impact)")
    lines.append("")
    if order_only_changes:
        lines.append(
            "The following changes only reorder Set-type attributes internally, with no actual resource changes."
        )
        lines.append("")
        for address, name, change in order_only_changes:
            lines.append(
                f"- `{address}`: **{name}** ({change.order_only_count} elements)"
            )
    else:
        lines.append("None")
    lines.append("")

    # Section: actual Set changes
    lines.append("## 🟡 Actual Changes in Set Attributes")
    lines.append("")
    if actual_set_changes:
        for address, name, change in actual_set_changes:
            lines.append(f"### `{address}` - {name}")
            lines.append("")
            lines.extend(format_set_change(change))
            lines.append("")
    else:
        lines.append("None")
    lines.append("")

    # Section: resource replacements
    lines.append("## 🔴 Resource Replacement (Caution)")
    lines.append("")
    if replace_resources:
        lines.append(
            "The following resources will be deleted and recreated. This may cause downtime."
        )
        lines.append("")
        for res in replace_resources:
            lines.append(f"- `{res.address}`")
    else:
        lines.append("None")
    lines.append("")

    # Section: warnings
    if result.warnings:
        lines.append("## ⚠️ Warnings")
        lines.append("")
        for warning in result.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)


def format_json_output(result: AnalysisResult) -> str:
    """Formats analysis results as JSON."""

    def set_change_to_dict(change: SetAttributeChange) -> dict:
        d = {
            "attribute_name": change.attribute_name,
            "path": change.path,
            "order_only_count": change.order_only_count,
            "is_primitive": change.is_primitive,
        }
        if change.added:
            d["added"] = change.added
        if change.removed:
            d["removed"] = change.removed
        if change.modified:
            d["modified"] = [{"key": k, "diffs": v} for k, v in change.modified]
        if change.primitive_added:
            d["primitive_added"] = change.primitive_added
        if change.primitive_removed:
            d["primitive_removed"] = change.primitive_removed
        if change.nested_changes:
            d["nested_changes"] = [set_change_to_dict(n) for n in change.nested_changes]
        return d

    def resource_to_dict(res: ResourceChange) -> dict:
        return {
            "address": res.address,
            "resource_type": res.resource_type,
            "actions": res.actions,
            "is_replace": res.is_replace,
            "is_create": res.is_create,
            "is_delete": res.is_delete,
            "set_changes": [set_change_to_dict(c) for c in res.set_changes],
            "other_changes": res.other_changes,
        }

    output = {
        "summary": {
            "order_only_count": result.order_only_count,
            "actual_set_changes_count": result.actual_set_changes_count,
            "replace_count": result.replace_count,
            "create_count": result.create_count,
            "delete_count": result.delete_count,
            "other_changes_count": result.other_changes_count,
        },
        "has_real_changes": (
            result.actual_set_changes_count > 0
            or result.replace_count > 0
            or result.create_count > 0
            or result.delete_count > 0
            or result.other_changes_count > 0
        ),
        "resources": [resource_to_dict(r) for r in result.resources],
        "warnings": result.warnings,
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_summary_output(result: AnalysisResult) -> str:
    """Formats analysis results as a one-line summary."""
    parts = []

    if result.order_only_count > 0:
        parts.append(f"🟢 {result.order_only_count} order-only")
    if result.actual_set_changes_count > 0:
        parts.append(f"🟡 {result.actual_set_changes_count} Set changes")
    if result.replace_count > 0:
        parts.append(f"🔴 {result.replace_count} replacements")

    if not parts:
        return "✅ No changes detected"

    return " | ".join(parts)


def analyze_plan(
    plan_json: Dict[str, Any],
    include_filter: Optional[List[str]] = None,
    exclude_filter: Optional[List[str]] = None,
) -> AnalysisResult:
    """Analyzes Terraform plan JSON and returns the results."""
    result = AnalysisResult()

    resource_changes = plan_json.get("resource_changes", [])

    for rc in resource_changes:
        res = analyze_resource_change(rc, include_filter, exclude_filter)
        if res:
            result.resources.append(res)

            # Counts statistics
            if res.is_replace:
                result.replace_count += 1
            elif res.is_create:
                result.create_count += 1
            elif res.is_delete:
                result.delete_count += 1

            if res.other_changes:
                result.other_changes_count += len(res.other_changes)

            for set_change in res.set_changes:
                order_only, actual = collect_all_changes(set_change)
                result.order_only_count += len(order_only)
                result.actual_set_changes_count += len(actual)

    # Adds warnings from the global configuration
    result.warnings = CONFIG.warnings.copy()

    return result


def determine_exit_code(result: AnalysisResult) -> int:
    """Determines the exit code based on analysis results."""
    if result.replace_count > 0:
        return EXIT_RESOURCE_REPLACE
    if (
        result.actual_set_changes_count > 0
        or result.create_count > 0
        or result.delete_count > 0
    ):
        return EXIT_SET_CHANGES
    return EXIT_NO_CHANGES


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyzes Terraform plan JSON for changes in AzureRM Set-type attributes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic usage
  python analyze_plan.py plan.json

    # From stdin
  terraform show -json plan.tfplan | python analyze_plan.py

    # CI/CD with exit code
  python analyze_plan.py plan.json --exit-code

    # JSON output for programmatic processing
  python analyze_plan.py plan.json --format json

    # Summary for CI logs
  python analyze_plan.py plan.json --format summary

Exit codes (with --exit-code):
    0 - No changes or order-only changes
    1 - Actual changes in Set attributes
    2 - Resource replacement detected
    3 - Error
""",
    )

    parser.add_argument(
        "plan_file",
        nargs="?",
        help="Path to the Terraform plan JSON file (reads from stdin if omitted)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json", "summary"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--exit-code",
        "-e",
        action="store_true",
        help="Returns an exit code based on change severity",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppresses warnings and detailed output",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Shows detailed warnings and debugging information",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Ignores case when comparing strings",
    )
    parser.add_argument(
        "--attributes", type=Path, help="Path to the custom attributes JSON file"
    )
    parser.add_argument(
        "--include",
        action="append",
        help="Analyzes only resources matching this pattern (can be repeated)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Excludes resources matching this pattern (can be repeated)",
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    global AZURERM_SET_ATTRIBUTES

    args = parse_args()

    # Sets global configuration
    CONFIG.ignore_case = args.ignore_case
    CONFIG.quiet = args.quiet
    CONFIG.verbose = args.verbose
    CONFIG.warnings = []

    # Loads Set attributes from external JSON
    AZURERM_SET_ATTRIBUTES = load_set_attributes(args.attributes)

    # Reads plan input
    if args.plan_file:
        try:
            with open(args.plan_file, "r") as f:
                plan_json = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {args.plan_file}", file=sys.stderr)
            sys.exit(EXIT_ERROR)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(EXIT_ERROR)
    else:
        try:
            plan_json = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON received from stdin: {e}", file=sys.stderr)
            sys.exit(EXIT_ERROR)

    # Checks whether the plan is empty
    resource_changes = plan_json.get("resource_changes", [])
    if not resource_changes:
        if args.format == "json":
            print(
                json.dumps(
                    {
                        "summary": {},
                        "has_real_changes": False,
                        "resources": [],
                        "warnings": [],
                    }
                )
            )
        elif args.format == "summary":
            print("✅ No changes detected")
        else:
            print("# Terraform Plan Analysis Results\n")
            print("No resource changes detected.")
        sys.exit(EXIT_NO_CHANGES)

    # Analyzes the plan
    result = analyze_plan(plan_json, args.include, args.exclude)

    # Formats output
    if args.format == "json":
        output = format_json_output(result)
    elif args.format == "summary":
        output = format_summary_output(result)
    else:
        output = format_markdown_output(result)

    print(output)

    # Determines the exit code
    if args.exit_code:
        sys.exit(determine_exit_code(result))


if __name__ == "__main__":
    main()
