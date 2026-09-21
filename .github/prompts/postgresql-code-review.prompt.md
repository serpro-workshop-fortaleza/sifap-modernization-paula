---
name: "postgresql-code-review"
description: "Review SQL and schemas against PostgreSQL 16 best practices and anti-patterns, delegating the checklist to the postgresql-code-review skill."
argument-hint: "selection=<sql-or-schema>"
agent: "dba"
tools: ["read", "search"]
---
# /postgresql-code-review

## Objective

Review PostgreSQL SQL, schemas, functions, and security features (JSONB, arrays, custom types, and Row Level Security) in a selection or across the project. Return a verdict with concrete fixes. The complete checklist is in the [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) skill. This prompt applies it to the SIFAP 2.0 database (PostgreSQL 16 through JPA/Hibernate) without repeating it.

> [!IMPORTANT]
> Any user input concatenated into SQL is an injection flaw and results in automatic rejection. Bind all parameters.

## When to Invoke

During code review of a migration, query, function, or schema change in Stages 3 or 4, before merging into `develop`.

## Preconditions

- The SQL or schema under review is available (a selection, migration file, or the project)
- The tables involved and their existing indexes are known or can be looked up in `db/migration/`
- The target is PostgreSQL 16

## Inputs the Team Must Provide

- `selection`: the SQL, schema, or migration to review (defaults to the current selection or project)
- The tables involved and all PII columns within them
- Ask the user for any missing information

## What I Will Do

- Apply the checklist in the [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) skill to the selection
- Check data type choices (CITEXT, TIMESTAMPTZ, ENUM, and JSONB), index types (GIN/GiST/partial), and constraints
- Confirm that each query is parameterized and each PII column is masked or commented
- Issue a verdict, Approved / Needs fixing / Rejected, with corrected SQL

## What I Will NOT Do

- Approve SQL with string concatenation or an unbound parameter
- Rewrite the JPA entity mapping here. Mapping changes go back to the owning module
- Treat JSONB as an opaque string or ignore PostgreSQL-specific operators
- Assume whether a column contains PII. I flag anything that is not identified

## Output Format

```markdown
### Verdict
Needs fixing: missing GIN index for a JSONB containment query.

### Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | High | Unparameterized status filter | `data->>'status' = '` + input |
| 2 | Medium | No index for `data @> ...` | Seq Scan on `orders` |

### Corrected SQL
CREATE INDEX idx_orders_data ON orders USING gin(data);
SELECT id FROM orders WHERE data @> :filter;
```

## Definition of Done

- [ ] A verdict is stated: Approved / Needs fixing / Rejected
- [ ] Each finding has severity and evidence (file/line or a plan excerpt)
- [ ] The corrected SQL is parameterized and ready to use
- [ ] Each PII column is masked or contains a `COMMENT`

## Prompt Body

The [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) skill defines PostgreSQL-specific anti-patterns and the quality checklist. Read it, then apply it to the selection.

**Step 1: run static analysis.**
Reject concatenated user input. Flag `SELECT *` on wide tables, generic types where suitable PostgreSQL types exist, and missing constraints.

**Step 2: apply the skill.**
Work through the skill's areas: JSONB, arrays, custom types/domains, schema design, functions/triggers, extensions, and RLS.

**Step 3: follow the kit's rules.**
Confirm PostgreSQL 16 features, parameterized access through JPA/Hibernate, rollback-safe migrations in `backend/src/main/resources/db/migration/`, and a `COMMENT` on every PII column.

**Step 4: issue the verdict.**
State Approved, Needs fixing, or Rejected with the corrected SQL and rationale.

## Example Invocation

```text
/postgresql-code-review selection=backend/src/main/resources/db/migration/V3__payment.sql
```
