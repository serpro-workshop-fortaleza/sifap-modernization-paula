# software-engineering-team

User experience and interface design (UX/UI) agent from the
software engineering team collection.

## What this plugin includes

| Component | Type | Location |
|-----------|------|----------|
| `se-ux-ui-designer` | Agent | [`.github/agents/se-ux-ui-designer.agent.md`](../../agents/se-ux-ui-designer.agent.md) |

## Related kit content

The immersion provides its own persona and stage agents in
[`.github/agents/`](../../agents/) (for example, `software-architect`,
`product-owner`, `tech-writer`, `qa-engineer`). They cover the roles served
by the original `se-*` agents, so those original agents are not
referenced here as replacements.

## Original references not included

- `se-gitops-ci-specialist`, `se-product-manager-advisor`,
  `se-responsible-ai-code`, `se-security-reviewer`,
    `se-system-architecture-reviewer`, `se-technical-writer` (agents) - not
    present in this kit.

## How it is enabled

Copilot discovers the content in `.github/agents/` natively in this
repository, so this agent works here without installing a plugin. The
plugin layer packages it as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
