# chromium-control-canvas

Interactive Chromium control dashboard.

## What this plugin includes

This is a **catalog-only** entry. The original plugin provided a CLI
*extension* package (an `extensions/` component), which is not bundled in this
kit. The manifest (`plugin.json`) contains only metadata.

## Original references not included

- `chromium-control-canvas` (CLI extension) - no `extensions/` package is
  tracked in this kit.

## How it is enabled

Plugins are declared in
[`.github/copilot/settings.json`](../../copilot/settings.json) through the
local `datacorp-mm-team-kit` marketplace
([`marketplace.json`](../marketplace.json)). This entry has no components,
so it is listed in the catalog but is not enabled.
See the [plugin index](../README.md) for the mechanism and its limitations.
