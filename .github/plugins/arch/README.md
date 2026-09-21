# arch

Architecture and modernization toolkit.

## What this plugin includes

This is a **catalog-only** entry. The original `arch` plugin referenced
a `doc-and-modernize` skill that is not part of this kit, so no
components are bundled here. The manifest (`plugin.json`) contains only metadata.

## Related kit content

The immersion maintains its own modernization skill,
[`.github/skills/code-modernization/`](../../skills/code-modernization/), which
Copilot discovers natively in this repository.

## Original references not included

- `doc-and-modernize` (skill) - not present in this kit.

## How it is enabled

Plugins are declared in
[`.github/copilot/settings.json`](../../copilot/settings.json) through the
local `datacorp-mm-team-kit` marketplace
([`marketplace.json`](../marketplace.json)). This entry has no components,
so it is listed in the catalog but is not enabled. See
the [plugin index](../README.md) for the mechanism and its limitations.
