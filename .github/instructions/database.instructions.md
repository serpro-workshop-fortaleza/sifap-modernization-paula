---
description: "Use when writing database repositories, migrations, schema changes, SQL queries, indexes, and rollback-safe data changes."
applyTo: "backend/src/main/java/**/infrastructure/**,backend/src/main/resources/db/migration/**"
---

# Database conventions - Flyway migrations and repositories

This file activates when you edit persistence code in `backend/src/main/java/**/infrastructure/**` or Flyway migrations in `backend/src/main/resources/db/migration/**`. It teaches migration hygiene, repository query safety, indexing, and rollback-safe schema changes in PostgreSQL 16. Entity and FDT-to-JPA mapping belong to [`modular-monolith.instructions.md`](modular-monolith.instructions.md); reading the Adabas FDT that informs a schema belongs to [`natural-adabas.instructions.md`](natural-adabas.instructions.md).

## Flyway migrations

Migrations are versioned, forward-only, and immutable after merge. Name them `V<n>__<snake_case_description>.sql`. Make one logical change per file. All identifiers use `snake_case`.

```sql
-- V1__create_resource.sql
CREATE TABLE resource (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    label       VARCHAR(120) NOT NULL,
    amount      NUMERIC(15, 2) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_resource_label ON resource (label);
```

> [!WARNING]
> Never edit a migration already run against a shared database. Flyway validates its checksum and will fail. Fix forward with a new `V<n+1>__` migration.

## Monetary values and precision

Monetary and packed decimal fields map to `NUMERIC(precision, scale)` in PostgreSQL and `BigDecimal` in Java. Never use `float`, `double`, `real`, or `money`.

```sql
amount NUMERIC(15, 2) NOT NULL -- maps to BigDecimal with scale 2
```

## Repositories

Repositories are Spring Data interfaces. Use derived query methods or `@Query` with JPQL and **named parameters**. Never concatenate strings, as that enables SQL injection.

```java
interface ResourceRepository extends JpaRepository<Resource, UUID> {

    Optional<Resource> findByLabel(String label);

    @Query("select r from Resource r where r.amount >= :floor")
    List<Resource> findAllAtOrAbove(@Param("floor") BigDecimal floor);
}
```

- Do not use `@Transactional` on repositories; the service owns the transaction boundary.
- Return `Optional<T>` for single lookups, never `null`.
- In native queries, still bind parameters (`:name` / `?1`); never interpolate strings.

## Indexes and constraints

Declare uniqueness, foreign keys, and indexes in the migration, not in application code. Index the columns your repositories use in filters and joins.

```sql
CREATE INDEX ix_payment_resource_id ON payment (resource_id);
ALTER TABLE payment
    ADD CONSTRAINT fk_payment_resource
    FOREIGN KEY (resource_id) REFERENCES resource (id);
```

## Rollback-safe change (expand / contract)

Never rename or drop a column in the same release that deploys code using it. Split every breaking change across releases to keep rollback safe.

| Phase | Migration | Release |
|---|---|---|
| Expand | Add the new nullable column or table | N |
| Backfill | Copy data in batches; dual-write in the application | N |
| Contract | Drop the old column/constraint once nothing reads it | N+1 |

The [`safe-migration`](../skills/safe-migration/SKILL.md) skill owns the full zero-downtime procedure and backfill checklist.

## Query performance

Avoid N+1 queries: fetch associations with `@EntityGraph` or JPQL `join fetch` and check an actual plan with `EXPLAIN ANALYZE`. The [`query-optimization`](../skills/query-optimization/SKILL.md) skill owns index and plan analysis.

```java
@EntityGraph(attributePaths = "payments")
List<Resource> findByLabelStartingWith(String prefix);
```

## Conventions

| Rule | Rationale |
|---|---|
| `V<n>__snake_case.sql`, forward-only | Deterministic, checksum-validated history |
| Tables and columns in `snake_case` | Idiomatic PostgreSQL, stable across tools |
| `NUMERIC` for money, `BigDecimal` in Java | No binary floating-point rounding in monetary values |
| JPQL / derived queries with bound parameters | No SQL injection and portable across dialects |
| Indexes and FKs declared in migrations | Schema reproducible from version control |
| Expand-contract for breaking changes | Every deployment is rollback-safe |

## Do / Don't

| Do | Don't |
|---|---|
| Add a new `V<n+1>__` migration to fix the schema | Edit an already applied migration |
| Bind all parameters | Concatenate values into SQL/JPQL |
| Keep `@Transactional` in the service | Annotate repositories as transactional |
| Backfill in batches, then contract | Drop and recreate a live table |

## PR Checklist

- [ ] The migration follows `V<n>__snake_case.sql` and changes one thing
- [ ] No previously applied migration was edited
- [ ] Monetary/packed fields use `NUMERIC(p, s)` mapped to `BigDecimal`
- [ ] Every query binds parameters; there is no string concatenation
- [ ] New filter/join columns are indexed; foreign keys are declared
- [ ] Breaking changes use expand → backfill → contract across releases
