---
name: "postgresql-optimization"
description: "Optimize PostgreSQL 16 queries, indexes, and schemas using PostgreSQL-specific features, delegating the workflow to the postgresql-optimization skill."
argument-hint: "selection=<sql-or-query>"
agent: "dba"
tools: ["read", "search", "execute"]
---
# /postgresql-optimization

## Objective

Optimize a slow PostgreSQL query, index, or schema using PostgreSQL-specific features. Support each recommendation with measured `EXPLAIN ANALYZE` results. The complete workflow is in the [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 database (PostgreSQL 16 through JPA/Hibernate) without repeating it.

> [!IMPORTANT]
> No recommendation is delivered without before-and-after `EXPLAIN ANALYZE` results. A plan is evidence, not an opinion.

## When to Invoke

During Stages 3 or 4, when a query is slow, a report times out, or a schema needs tuning with realistic row counts.

## Preconditions

- The query or schema to optimize is available
- A staging snapshot with realistic row counts is accessible for running `EXPLAIN ANALYZE`
- Existing indexes on the tables involved can be listed
- The target is PostgreSQL 16

## Inputs the Team Must Provide

- `selection`: the query or schema to optimize
- The tables involved, their indexes, and realistic row counts
- Ask the user for any missing information

## What I Will Do

- Apply the optimization workflow in the [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) skill to the selection
- Read `EXPLAIN (ANALYZE, BUFFERS)` from start to finish and identify the dominant cost
- Recommend the correct index type (GIN/GiST/partial/covering) or a query rewrite with evidence
- Express index changes as operationally safe and rollback-safe migrations

## What I Will NOT Do

- Recommend an index without assessing its write cost or add one for every query
- Rely on `EXPLAIN` without `ANALYZE` or optimize with development-scale data
- Concatenate user input into SQL or misalign the JPA mapping
- Apply a blocking `CREATE INDEX` on a heavily accessed table. I use `CONCURRENTLY`

## Output Format

```markdown
### Bottleneck
Seq Scan on `payment` (4 million rows) for a selective status filter.

### Recommendation
CREATE INDEX CONCURRENTLY idx_payment_status ON payment (status) WHERE status <> 'CLOSED';

### EXPLAIN ANALYZE
Before: Seq Scan, 820 ms. After: Index Scan, 4 ms.
```

## Definition of Done

- [ ] The dominant bottleneck is named and supported by plan evidence
- [ ] The recommendation is supported by before-and-after `EXPLAIN ANALYZE` results
- [ ] All indexes use an operationally safe (`CONCURRENTLY`) and rollback-safe migration
- [ ] Queries remain parameterized and consistent with the JPA mapping

## Prompt Body

The [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) skill defines the diagnostic workflow, index heuristics, and PostgreSQL feature set. Read it, then apply it to the selection.

**Step 1: measure.**
Run `EXPLAIN (ANALYZE, BUFFERS)` on a staging snapshot and read the plan from start to finish.

**Step 2: apply the skill.**
Use the skill to choose the fix: index type, query rewrite, JSONB/array operator, window function, or partitioning.

**Step 3: follow the kit's rules.**
Use PostgreSQL 16, keep the JPA mapping synchronized, and deliver index changes as `CONCURRENTLY` migrations in `db/migration/`.

**Step 4: prove the result.**
Run `EXPLAIN ANALYZE` again and paste the before-and-after timings.

## Example Invocation

```text
/postgresql-optimization selection="SELECT * FROM payment WHERE status = 'OPEN'"
```
