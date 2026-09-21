# database-data-management

PostgreSQL code review and optimization skills.

## What this plugin includes

| Component | Type | Location |
|-----------|------|----------|
| `postgresql-code-review` | Skill | [`.github/skills/postgresql-code-review/`](../../skills/postgresql-code-review/) |
| `postgresql-optimization` | Skill | [`.github/skills/postgresql-optimization/`](../../skills/postgresql-optimization/) |

PostgreSQL 16 is the kit's target database, so only PostgreSQL
skills are included.

## Related kit content

The immersion maintains a [`dba`](../../agents/dba.agent.md) persona agent and a
[`query-optimization`](../../skills/query-optimization/) skill. These are
the kit's own artifacts, not direct renamings of the original
`postgresql-dba` or `sql-optimization` items, so they are not referenced here as replacements.

## Original references not included

- `sql-code-review`, `sql-optimization` (skills) - not present in this kit.
- `ms-sql-dba`, `postgresql-dba` (agents) - not present in this kit.

## How it is enabled

Copilot discovers the content in `.github/skills/` natively in this
repository, so these skills work here without installing a plugin. The
plugin layer packages them as a named collection in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json)) and is declared
in [`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugin index](../README.md) for the mechanism and its limitations.
