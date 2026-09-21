# azure-cloud-development

Azure cloud development skills: cost optimization, pricing, and resource health.

## What this plugin includes

The manifest references skills at the repository level in
`.github/skills/`. They are maintained once there and shared throughout the kit.

| Component | Type | Location |
|-----------|------|----------|
| `az-cost-optimize` | Skill | [`.github/skills/az-cost-optimize/`](../../skills/az-cost-optimize/) |
| `azure-pricing` | Skill | [`.github/skills/azure-pricing/`](../../skills/azure-pricing/) |
| `azure-resource-health-diagnose` | Skill | [`.github/skills/azure-resource-health-diagnose/`](../../skills/azure-resource-health-diagnose/) |

## Original references not included

The original `azure-cloud-development` plugin also listed the items below. They
are not present in this kit's consolidated `.github/skills/` and `.github/agents/`,
so the manifest omits them:

- `import-infrastructure-as-code` (skill)
- `azure-logic-apps-expert`, `azure-principal-architect`, `azure-saas-architect`,
  `azure-verified-modules-bicep`, `azure-verified-modules-terraform`,
    `terraform-azure-implement`, `terraform-azure-planning` (agents)

## How it is enabled

Copilot discovers the content in `.github/skills/` natively in this
repository, so these skills work here without installing a plugin. The
plugin layer packages them as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
