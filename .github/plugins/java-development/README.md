# java-development

Spring Boot scaffolding, Javadoc, JUnit 5, and Spring Boot best practices skills.

## What this plugin includes

Java 21 + Spring Boot 3.3 is the kit's backend platform.

| Component | Type | Location |
|-----------|------|----------|
| `create-spring-boot-java-project` | Skill | [`.github/skills/create-spring-boot-java-project/`](../../skills/create-spring-boot-java-project/) |
| `java-docs` | Skill | [`.github/skills/java-docs/`](../../skills/java-docs/) |
| `java-junit` | Skill | [`.github/skills/java-junit/`](../../skills/java-junit/) |
| `java-springboot` | Skill | [`.github/skills/java-springboot/`](../../skills/java-springboot/) |

All four original references resolve, so nothing was removed.

## How it is enabled

Copilot discovers the content in `.github/skills/` natively in this
repository, so these skills work here without installing a plugin. The
plugin layer packages them as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
