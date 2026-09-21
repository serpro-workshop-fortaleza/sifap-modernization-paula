# frontend-web-dev

React web frontend agent and Playwright test generation skill.

## What this plugin includes

| Component | Type | Location |
|-----------|------|----------|
| `expert-react-frontend-engineer` | Agent | [`.github/agents/expert-react-frontend-engineer.agent.md`](../../agents/expert-react-frontend-engineer.agent.md) |
| `playwright-generate-test` | Skill | [`.github/skills/playwright-generate-test/`](../../skills/playwright-generate-test/) |

## Original references not included

- `playwright-explore-website` (skill) - not present in this kit.
- `electron-angular-native` (agent) - not present in this kit.

## How it is enabled

Copilot discovers the content in `.github/skills/` and `.github/agents/` natively
in this repository, so these components work here without
installing a plugin. The plugin layer packages them as a named collection
in the local `datacorp-mm-team-kit` marketplace
([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
