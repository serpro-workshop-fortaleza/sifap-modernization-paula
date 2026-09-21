---
name: "safe-migration"
description: "Use when planning a live schema change, a zero-downtime migration, or rollback of a deployment that changed a table. Triggers include \"migration\", \"ALTER TABLE\", \"zero downtime\", \"expand and contract\", and \"backfill\"."
---
# Safe schema migration

## When to Invoke

- "Plan the migration to add column X."
- "Can we rename this column without downtime?"
- "How do we safely remove this table?"

## Expand, migrate, and contract pattern

Every schema change affecting live traffic goes through **three deployments**, never just one.

1. **Expand**: add the new structure alongside the old one (new nullable column, new table, or new index). No reads or writes use it yet.
2. **Migrate**: dual-write to the old and new structures, backfill historical rows, and switch reads to the new structure through a feature flag.
3. **Contract**: remove the old structure only after the new one has been authoritative for at least one release cycle.

## Rules of thumb

- **Additive changes are always safe**: a new nullable column, new index (CONCURRENTLY / ONLINE), or new table.
- **Destructive changes never happen in a single deployment**: dropping or renaming a column, changing a type, dropping a table, or adding NOT NULL.
- **Backfills run in batches**, with LIMIT, pauses between batches, and idempotency. Never run `UPDATE whole_table SET …` all at once.
- **Index creation**: `CREATE INDEX CONCURRENTLY` (Postgres), `ONLINE=ON` (MySQL 8 / SQL Server). Monitor lock escalation.
- **Renames**: do NOT rename directly. Add a new column -> dual-write -> backfill -> switch reads -> remove the old column.

## Pre-deployment checklist

- [ ] The migration has documented **forward** and **rollback** plans.
- [ ] Duration was estimated on a **production copy** (never estimate in the development environment).
- [ ] Locking impact was assessed (`pg_locks`, `SHOW ENGINE INNODB STATUS`, `sys.dm_tran_locks`).
- [ ] Backfill batch size was set according to the replica lag budget.
- [ ] Monitoring exists for replica lag, long transactions, and deadlocks.
- [ ] A feature flag or dual-read path was installed before the migration step.

## Warning signs: do not deploy

- A single `ALTER TABLE` that fully locks a large table.
- A migration coupled to application deployment that cannot be rolled back independently.
- An irreversible step without a backup.
- A backfill that rewrites all rows in a single transaction.

## Output Template

```markdown
## Migration plan - <change>

| Field | Value |
|---|---|
| Change type | additive / destructive |
| Pattern stage | Expand / Migrate / Contract |
| Migration file | backend/src/main/resources/db/migration/V<N>__<desc>.sql |
| Forward plan | <DDL / backfill> |
| Rollback plan | <how to roll back independently of application deployment> |
| Locking impact | <estimate obtained on a production copy> |

### Backfill
- Batch size <rows>, pause <ms>, idempotent yes/no
```

## Quality Gate

- [ ] Destructive changes are split across expand, migrate, and contract deployments.
- [ ] Forward and rollback plans exist independently of application deployment.
- [ ] Indexes are created with `CREATE INDEX CONCURRENTLY`; no full-table lock is deployed.
- [ ] Backfills run in bounded, idempotent batches within the replica lag budget.
- [ ] Duration and locking impact were estimated on a production-sized copy.

## References

- [Braintree - PostgreSQL at Scale: Safe Migrations](https://medium.com/paypal-tech/postgresql-at-scale-database-schema-changes-without-downtime-20d3749ed680)
- [GitHub - gh-ost online schema migration](https://github.com/github/gh-ost)
- [Martin Fowler - Evolutionary Database Design](https://martinfowler.com/articles/evodb.html)
