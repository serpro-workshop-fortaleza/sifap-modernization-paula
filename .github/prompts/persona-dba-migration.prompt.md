---
name: "migration"
description: "Produce a versioned, reversible Flyway migration for PostgreSQL 16, with online-safe steps, batched backfill, and a rollback script."
argument-hint: "req=REQ-NNN change=<natural-language-change>"
agent: "dba"
tools: ["read", "search", "edit", "execute"]
---
# /migration

## Objective

Produce a Flyway migration for **PostgreSQL 16** for a schema change that is (a) idempotent, (b) reversible, (c) safe to run while the application serves traffic, and (d) traced to a `REQ-ID` in `specs/<NNN>-<feature>/spec.md`. The deliverable contains a versioned forward migration, a batched backfill when needed, and a matching rollback script. All must be tested on a staging snapshot.

> [!WARNING]
> Destructive changes (dropping or renaming a column, changing a type, or adding `NOT NULL`) never ship in a single deployment. Expand, migrate, then contract.

## When to Invoke

During Stages 3 or 4, when a task in `plan.md` requires a schema change or when mapping an Adabas DDM to its first PostgreSQL table. Run after recording the change in the plan. Never use this prompt to invent a schema.

## Preconditions

- The change is present in `specs/<NNN>-<feature>/plan.md`. Otherwise, it goes through an architecture review first
- `specs/<NNN>-<feature>/spec.md` contains the `REQ-ID` and EARS statement served by the change
- A `db/migration/` folder exists in the backend module or will be created by this migration
- A staging snapshot of the target database is available for testing

## Inputs the Team Must Provide

- The requested change in natural language
- The linked `REQ-ID` and its EARS statement
- The data scale: row counts of affected tables and peak queries per second (QPS)
- The deployment window: zero downtime required or a maintenance window allowed
- The legacy reference, if any: the Adabas DDM in `01-archaeology/legacy-sifap/adabas-ddms/` that originates this mapping
- Ask the user for any missing information

## What I Will Do

- Confirm that the change is in `plan.md`, then choose a Flyway version `Vyyyymmddhhmm__short_description.sql`
- Design an online-safe sequence: nullable column, batched backfill, and constraints last
- Faithfully map Adabas formats (Natural packed decimal `P9.2` / DDM `P 9,2` → `NUMERIC(9,2)`, `MU` → child table or JSONB, `PE` → child table, superdescriptor or composite descriptor → composite index)
- Write a separate idempotent backfill for large tables and apply constraints only after it completes
- Write the matching `*.undo.sql` rollback and document replication, `VACUUM`, and plan-cache side effects
- Test the forward migration and rollback on a staging snapshot and paste the output

## What I Will NOT Do

- Design a schema that is not in `plan.md`. Unplanned changes go back to architecture review
- Add `NOT NULL DEFAULT`, drop, or rename a column on a large, hot table in a single statement, because that rewrites or locks the table
- Deliver a forward migration without its matching rollback
- Create an index without `CONCURRENTLY` or backfill an entire table in one transaction
- Store PII (CPF or benefit amounts) in a new column without flagging it and adding a column `COMMENT`
- Write business logic in the database (stored procedures). Logic belongs in Java
- Assume the meaning or contents of an Adabas field. I map only the format identified by the team in the DDM

## Output Format

```markdown
### Migration metadata
Version `V202603171430__add_reviewed_at.sql` · REQ-031 · online-safe: yes · ~2 min for 4 million rows.

### Forward: V202603171430__add_reviewed_at.sql
-- REQ-031: While a payment is under review, the system shall record the review timestamp.
-- Online-safe: nullable addition + CONCURRENTLY index; no table rewrite.
ALTER TABLE payment ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;
CREATE INDEX CONCURRENTLY idx_payment_reviewed_at ON payment (reviewed_at);
COMMENT ON COLUMN payment.reviewed_at IS 'Review timestamp; not PII.';

### Backfill (separate and idempotent): batches of 5,000
-- Run outside the migration; commit between batches until no rows remain.

### Rollback: V202603171430__add_reviewed_at.undo.sql
DROP INDEX CONCURRENTLY IF EXISTS idx_payment_reviewed_at;
ALTER TABLE payment DROP COLUMN IF EXISTS reviewed_at;

### Application coordination
Deploy the writer that populates reviewed_at after this migration. Readers accept NULL until the backfill completes.

### Risk register
Locking: none (CONCURRENTLY). Replication: index creation increases lag; monitor it. Plan cache: invalidated when adding the column.
```

## Definition of Done

- [ ] Forward and rollback scripts are in `db/migration/`
- [ ] The forward script is idempotent (`IF NOT EXISTS`, `IF EXISTS`)
- [ ] No `ACCESS EXCLUSIVE` lock occurs on a hot table without an explicit maintenance-window note
- [ ] Backfills of more than 100,000 rows run in batches of 1,000 to 10,000, with a commit between batches
- [ ] The linked `REQ-ID` and EARS statement appear in a comment at the top of the file
- [ ] Output from `flyway migrate` and `flyway undo` on a staging snapshot is included
- [ ] The application coordination plan is explicitly stated

## Prompt Body

You are `@dba`. The team needs to turn a schema change into a safe, reversible migration. Read [`safe-migration`](../skills/safe-migration/SKILL.md) before starting. This skill defines the expand/migrate/contract pattern and the preflight checklist.

**Step 1: confirm that the change is planned.**
Check that the change appears in `plan.md`. Otherwise, stop and route it to architecture review. The migration follows the plan, never the reverse. Record the `REQ-ID` and EARS statement.

**Step 2: choose the version and map the types.**
Name the file `Vyyyymmddhhmm__short_description.sql`. When mapping an Adabas DDM, convert formats faithfully: Natural packed decimal `P9.2` / DDM `P 9,2` → `NUMERIC(9,2)` (monetary values use `NUMERIC`, never `FLOAT`); `MU` → a child table or JSONB; `PE` → a child table; a superdescriptor or composite descriptor → a composite index. In the Natural CE 9.3.3 lab image, Natural format specifications use a period as the decimal separator. Therefore, `P9.2` means nine integer digits plus two fractional digits. Comma formats, such as `P9,2`, fail with `NAT0165` in source declarations. See [`natural-adabas`](../instructions/natural-adabas.instructions.md).

**Step 3: design the migration for online execution.**
Prefer nonblocking additive steps: add a nullable column, backfill it, and add constraints last. Create indexes with `CREATE INDEX CONCURRENTLY`, without `IF NOT EXISTS`, which requires a separate guard. Avoid `ALTER TABLE` operations that require an `ACCESS EXCLUSIVE` lock on a hot table. If one is unavoidable, schedule a maintenance window and record that requirement.

**Step 4: plan the backfill.**
For nontrivial data, write a separate idempotent backfill that processes 1,000 to 10,000 rows per batch, with a `commit` between batches. Never backfill inside the migration when the table has more than 100,000 rows.

**Step 5: apply constraints after the backfill.**
Add `NOT NULL`, `CHECK`, foreign keys, and unique indexes only after the data is consistent.

**Step 6: write the rollback.**
Pair every forward migration with a `Vyyyymmddhhmm__short_description.undo.sql` file that restores the previous schema, even from an intermediate state.

**Step 7: document side effects and test.**
Record replication slot drift, `VACUUM` implications, plan-cache invalidation, and any application code that must ship together. Restore the staging snapshot, run `flyway migrate`, verify, run `flyway undo`, verify again, and paste the output.

Never put business logic in the database. Mask CPF and benefit amounts. Flag every new PII column for the DevOps Engineer and Technical Lead.

## Example Invocation

```text
/migration req=REQ-031 change="add a nullable review timestamp to the payment table"
```
