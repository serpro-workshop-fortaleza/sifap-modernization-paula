---
name: "query-optimization"
description: "Use when investigating slow queries, designing indexes, or reviewing execution plans. Triggers include \"slow query\", \"EXPLAIN plan\", \"index\", \"query tuning\", \"N+1\", and \"table scan\"."
---
# Query optimization

## When to Invoke

- "This query is slow."
- "Why is it not using the index?"
- "Should I add an index on...?"
- "Review this EXPLAIN output."

## Diagnostic workflow

1. **Measure before optimizing**: capture a baseline (p50/p95 latency, rows examined, rows returned, and logical reads).
2. **Get the plan**: `EXPLAIN (ANALYZE, BUFFERS)` in PostgreSQL, `EXPLAIN ANALYZE FORMAT=JSON` in MySQL 8, or `SET STATISTICS IO, TIME ON` in SQL Server.
3. **Look for common causes**:

- **Seq Scan / Table Scan** on a large table with a selective predicate: missing index
- **Row estimate off by more than 10x**: outdated statistics; run `ANALYZE`
- **Nested Loop with many outer rows**: should be a hash or merge join
- **Sort spilling to disk**: `work_mem` too low or missing index for ORDER BY
- **Filter after the join**, instead of pushdown: rewrite the query or add an index for the predicate

4. **Propose the smallest change**: an index, a rewrite, a statistics update, or a parameter adjustment.
5. **Validate**: rerun ANALYZE, confirm the plan change, and verify reduced latency. Never "deploy and hope".

## Index design heuristics

- Put **equality columns first**, then range columns, and finally sort columns (ESR rule).
- A **covering index** (INCLUDE columns) avoids heap lookups in read-heavy queries.
- A **partial index** serves highly selective filters on skewed data (`WHERE status = 'pending'`).
- Every index adds write cost. Justify each one.

## Anti-patterns

- `SELECT *` in critical paths: forces heap access and prevents covering indexes.
- `WHERE func(col) = x`: prevents index use; store a computed column or use an expression index.
- ORM N+1: fix it in the ORM with eager loading, not with an index.
- "Add an index to every column": wastes storage and slows writes.

## Output Template

```markdown
## Query optimization - <query id>

| Field | Before | After |
|---|---|---|
| p95 latency | <ms> | <ms> |
| Rows examined | <n> | <n> |
| Plan | Seq Scan | Index Scan on <index> |

**Change**: index / rewrite / ANALYZE / parameter
**DDL**: CREATE INDEX CONCURRENTLY <name> ON <table> (<cols>)
**Validation**: rerunning EXPLAIN (ANALYZE, BUFFERS) confirms the new plan
```

## Quality Gate

- [ ] A baseline (p50/p95, rows examined, and plan) was captured before any change.
- [ ] The proposed change is the smallest that fixes the bottleneck.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` confirms the plan change and reduced latency.
- [ ] Every new index is justified against its write cost.

## References

- [Use The Index, Luke!](https://use-the-index-luke.com/)
- [PostgreSQL - Performance tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [SQL Server - Query Store](https://learn.microsoft.com/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store)
