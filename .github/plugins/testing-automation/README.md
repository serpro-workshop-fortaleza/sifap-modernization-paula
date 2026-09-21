# testing-automation

JUnit 5 and Playwright test generation skills.

## What this plugin includes

| Component | Type | Location |
|-----------|------|----------|
| `java-junit` | Skill | [`.github/skills/java-junit/`](../../skills/java-junit/) |
| `playwright-generate-test` | Skill | [`.github/skills/playwright-generate-test/`](../../skills/playwright-generate-test/) |

## Related kit content

The immersion maintains testing skills such as
[`tdd-workflow`](../../skills/tdd-workflow/),
[`test-strategy`](../../skills/test-strategy/) and
[`spring-boot-testing`](../../skills/spring-boot-testing/), which cover the
roles of the original `tdd-*` agents.

## Original references not included

- `ai-prompt-engineering-safety-review`, `csharp-nunit`,
  `playwright-explore-website` (skills) - not present in this kit.
- `playwright-tester`, `tdd-red`, `tdd-green`, `tdd-refactor` (agents) - not
  present in this kit.

## How it is enabled

Copilot discovers the content in `.github/skills/` natively in this
repository, so these skills work here without installing a plugin. The
plugin layer packages them as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
