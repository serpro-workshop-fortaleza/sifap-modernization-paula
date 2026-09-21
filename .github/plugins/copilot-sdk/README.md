# copilot-sdk

Build agent-based applications with the GitHub Copilot SDK.

## What this plugin includes

| Component | Type | Location |
|-----------|------|----------|
| `copilot-sdk` | Skill | [`.github/skills/copilot-sdk/`](../../skills/copilot-sdk/) |

## How it is enabled

Copilot discovers the content in `.github/skills/` natively in this
repository, so this skill works here without installing a plugin. The
plugin layer packages it as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
