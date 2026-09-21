---
name: "generate-jpa-from-fdt"
description: "Generates JPA entity classes from Adabas FDT definitions, using JSONB for MU/PE fields."
argument-hint: "ddm=01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm context=<context> package=<java.package> dateformat=<format>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /generate-jpa-from-fdt

## Objective

Parse an Adabas DDM and generate a JPA entity with correct types, explicit MU/PE handling, and a corresponding Flyway migration.

## When to Invoke

At the start of Stage 3, when preparing a bounded context's data layer.

## Preconditions

- `02-modern-spec/bounded-contexts.md` identifies the DDM owner
- The DDM is in `01-archaeology/legacy-sifap/adabas-ddms/`
- The target package has been defined

## Inputs the Team Must Provide

- DDM path
- Bounded context and Java package
- Legacy date format, such as packed `YYYYMMDD` or alphanumeric `YYYY-MM-DD`

## What I Will Do

- Parse the FDT, map Java/JPA fields, handle MU as JSONB or `@ElementCollection` and PE as `@OneToMany` entities
- Generate PostgreSQL 16 DDL in Flyway
- Mark cryptic names with FIXME

## What I Will NOT Do

- Invent meaning or date formats
- Create stored procedures
- Omit MU/PE fields

## Output Format

1. `src/main/java/[package]/domain/[EntityName].java`
2. `db/migration/V[NNN]__create_[table_name].sql`

## Definition of Done

- [ ] The entity compiles and covers all fields
- [ ] MU uses JSONB (`@JdbcTypeCode(SqlTypes.JSON)`) or `@ElementCollection`
- [ ] PE uses a separate entity with `@OneToMany`
- [ ] The migration is valid PostgreSQL 16 DDL
- [ ] Cryptic names have `// FIXME: confirm semantics` and are referred as open questions

## Prompt Body

You are `@builder`. Create a JPA entity from the specified DDM.

**Step 1 - Parse the FDT.** Extract the level, short name, long name, A/N/P/B/D/T format, length, and DE/MU/PE/SU. Present a table for review.

**Step 2 - Map types.**

| Adabas | Java | JPA | Notes |
|---|---|---|---|
| A(n) | `String` | `@Column(length = n)` | |
| N(n) without decimals | `Long` or `Integer` | `@Column` | Use `Long` for IDs |
| N(n.m) | `BigDecimal` | `@Column(precision=n, scale=m)` | Always use for monetary amounts |
| P(n.m) | `BigDecimal` | `@Column(precision=n, scale=m)` | Packed decimal |
| D | `LocalDate` | `@Column` | Confirm the format |
| T | `LocalDateTime` | `@Column` | |
| B(n) | `byte[]` | `@Lob` | Rare |
| MU field | `List<T>` | JSONB or `@ElementCollection` | The team chooses |
| PE group | `List<EmbeddedEntity>` | `@OneToMany` | Separate entity |

For MU, present JSONB, simpler and less queryable, and `@ElementCollection`, more queryable with a separate table. The team chooses.

**Step 3 - Handle PE.** Create a dedicated entity and table, `@ManyToOne` to the parent, mapped fields, and an occurrence index.

**Step 4 - Handle superdescriptors.** Add a composite index:

```java
@Table(indexes = @Index(columnList = "field_a, field_b"))
```

**Step 5 - Mark cryptic names.**

```java
/** FIXME: confirm semantics with the team for Adabas field XX */
@Column(name = "xx_value", length = 20)
private String xxValue;
```

Ask a person to record the question in `mysteries-found.md` with `path:line`; do not answer it or change its status.

**Step 6 - Generate Flyway.** Use snake_case, matching types, the selected JSONB option, PE tables, keys, indexes, and obvious `CHECK` constraints. Name it `V[NNN]__create_[table_name].sql`.

**Step 7 - Verify compilation.** Compile and report problems.

## Example Invocation

```text
/generate-jpa-from-fdt ddm=01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm context=<context> package=<java.package> dateformat=<format>
```
