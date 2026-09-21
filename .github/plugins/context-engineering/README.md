# context-engineering

Context mapping to maximize GitHub Copilot effectiveness.

## What this plugin includes

| Component | Type | Location |
|-----------|------|----------|
| `context-map` | Skill | [`.github/skills/context-map/`](../../skills/context-map/) |

## Related kit content

The immersion also maintains
[`.github/skills/context-audit/`](../../skills/context-audit/) and
[`.github/skills/refactor-safely/`](../../skills/refactor-safely/), which are the
kit's own equivalents of the original `what-context-needed` and
`refactor-plan`.

## Original references not included

- `refactor-plan`, `what-context-needed` (skills) - the kit uses
  `refactor-safely` and `context-audit` instead.
- `context-architect` (agent) - not present in this kit.

## How it is enabled

Copilot discovers the content in `.github/skills/` natively in this
repository, so this skill works here without installing a plugin. The
plugin layer packages it as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
