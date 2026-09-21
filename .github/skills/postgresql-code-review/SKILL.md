---
name: "postgresql-code-review"
description: "Review existing PostgreSQL SQL, schemas, and functions for specific anti-patterns, quality, and security: JSONB operations, array usage, custom types, schema design, function optimization, and Row Level Security (RLS). Use when someone requests a review, audit, or critical assessment of existing PostgreSQL code or a migration. To create or optimize new features, use postgresql-optimization."
---
# PostgreSQL code review

Specialized PostgreSQL code review for `${selection}` (or the whole project when nothing is selected). Focuses on PostgreSQL-specific best practices, anti-patterns, and quality standards, not generic SQL. To create or tune new PostgreSQL features instead of reviewing existing ones, use [`postgresql-optimization`](../postgresql-optimization/SKILL.md).

> [!IMPORTANT]
> The SIFAP 2.0 backend accesses **PostgreSQL 16** through **JPA/Hibernate**. Application queries must use JPQL, Spring Data derived queries, or bound native parameters, never string-concatenated SQL. The schema lives in Flyway migrations in `backend/src/main/resources/db/migration/`. Where this skill and [`database.instructions.md`](../../instructions/database.instructions.md) overlap, the instruction file is authoritative.

## When to Invoke

- "Review this migration for PostgreSQL anti-patterns."
- "Audit our JSONB and array usage."
- "Does this schema use the correct PostgreSQL types?"
- "Check this PL/pgSQL function and RLS policy before merging."

## PostgreSQL-specific review areas

### JSONB best practices

```sql
-- BAD: inefficient JSONB usage
SELECT * FROM orders WHERE data->>'status' = 'shipped';  -- No index support

-- GOOD: indexable JSONB queries
CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));
SELECT * FROM orders WHERE data @> '{"status": "shipped"}';

-- BAD: deep nesting without evaluation
UPDATE orders SET data = data || '{"shipping":{"tracking":{"number":"123"}}}';

-- GOOD: structured JSONB with validation
ALTER TABLE orders ADD CONSTRAINT valid_status
CHECK (data->>'status' IN ('pending', 'shipped', 'delivered'));
```

### Array operations review

```sql
-- BAD: inefficient array operations
SELECT * FROM products WHERE 'electronics' = ANY(categories);  -- No index

-- GOOD: GIN-indexed array queries
CREATE INDEX idx_products_categories ON products USING gin(categories);
SELECT * FROM products WHERE categories @> ARRAY['electronics'];

-- BAD: array concatenation in loops
-- This would be inefficient in a function or procedure

-- GOOD: batch array operations
UPDATE products SET categories = categories || ARRAY['new_category']
WHERE id IN (SELECT id FROM products WHERE condition);
```

### PostgreSQL schema design review

```sql
-- BAD: does not use PostgreSQL features
CREATE TABLE users (
    id INTEGER,
    email VARCHAR(255),
    created_at TIMESTAMP
);

-- GOOD: PostgreSQL-optimized schema
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,  -- Case-insensitive email
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Adds a JSONB GIN index for metadata queries
CREATE INDEX idx_users_metadata ON users USING gin(metadata);
```

### Custom types and domains

```sql
-- BAD: uses generic types for specific data
CREATE TABLE transactions (
    amount DECIMAL(10,2),
    currency VARCHAR(3),
    status VARCHAR(20)
);

-- GOOD: PostgreSQL custom types
CREATE TYPE currency_code AS ENUM ('USD', 'EUR', 'GBP', 'JPY');
CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');
CREATE DOMAIN positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0);

CREATE TABLE transactions (
    amount positive_amount NOT NULL,
    currency currency_code NOT NULL,
    status transaction_status DEFAULT 'pending'
);
```

## PostgreSQL-specific anti-patterns

### Performance anti-patterns

- **Avoiding PostgreSQL-specific indexes**: not using GIN/GiST for appropriate data types
- **Misusing JSONB**: treating JSONB as a plain string field
- **Ignoring array operators**: using inefficient array operations
- **Poor partition key selection**: not leveraging PostgreSQL partitioning effectively

### Schema design issues

- **Not using ENUM types**: using VARCHAR for limited value sets
- **Ignoring constraints**: not including CHECK constraints to validate data
- **Using incorrect data types**: using VARCHAR instead of TEXT or CITEXT
- **Not structuring JSONB**: using JSONB without structure or validation

### Function and trigger issues

```sql
-- BAD: inefficient trigger function
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();  -- Should use TIMESTAMPTZ
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- GOOD: optimized trigger function
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Configures the trigger to fire only when necessary
CREATE TRIGGER update_modified_time_trigger
    BEFORE UPDATE ON table_name
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION update_modified_time();
```

## PostgreSQL extension usage review

### Extension best practices

```sql
-- Checks whether the extension exists before creating it
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Uses extensions appropriately
-- UUID generation
SELECT uuid_generate_v4();

-- Password hashing
SELECT crypt('password', gen_salt('bf'));

-- Fuzzy text matching
SELECT word_similarity('postgres', 'postgre');
```

## PostgreSQL security review

### Row Level Security (RLS)

```sql
-- GOOD: RLS implementation
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_data_policy ON sensitive_data
    FOR ALL TO application_role
    USING (user_id = current_setting('app.current_user_id')::INTEGER);
```

### Privilege management

```sql
-- BAD: overly broad permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;

-- GOOD: granular permissions
GRANT SELECT, INSERT, UPDATE ON specific_table TO app_user;
GRANT USAGE ON SEQUENCE specific_table_id_seq TO app_user;
```

## PostgreSQL code quality checklist

### Schema design

- [ ] Uses appropriate PostgreSQL data types (CITEXT, JSONB, arrays)
- [ ] Leverages ENUM types for constrained values
- [ ] Implements appropriate CHECK constraints
- [ ] Uses TIMESTAMPTZ instead of TIMESTAMP
- [ ] Defines custom domains for reusable constraints

### Performance considerations

- [ ] Uses appropriate index types (GIN for JSONB/arrays, GiST for ranges)
- [ ] Uses containment operators (@>, ?) in JSONB queries
- [ ] Uses PostgreSQL-specific operators in array operations
- [ ] Uses window functions and CTEs correctly
- [ ] Uses PostgreSQL-specific functions efficiently

### PostgreSQL feature usage

- [ ] Uses extensions where appropriate
- [ ] Implements PL/pgSQL stored procedures where beneficial
- [ ] Leverages PostgreSQL's advanced SQL features
- [ ] Uses PostgreSQL-specific optimization techniques
- [ ] Implements appropriate error handling in functions

### Security and compliance

- [ ] Implements Row Level Security (RLS) when necessary
- [ ] Manages roles and privileges correctly
- [ ] Uses PostgreSQL's built-in encryption functions
- [ ] Implements audit trails with PostgreSQL features

## PostgreSQL-specific review guidelines

1. **Data type optimization**: confirm appropriate use of PostgreSQL-specific types
2. **Index strategy**: review index types and confirm use of PostgreSQL-specific indexes
3. **JSONB structure**: validate JSONB schema design and query patterns
4. **Function quality**: review PL/pgSQL function efficiency and best practices
5. **Extension usage**: check appropriate use of PostgreSQL extensions
6. **Performance features**: check use of PostgreSQL's advanced features
7. **Security implementation**: review PostgreSQL-specific security features

Focus on PostgreSQL's unique features and confirm that the code leverages its capabilities rather than treating it as a generic SQL database.

## Output Template

Deliver the review with a verdict, a findings table, and corrected SQL ready to paste.

```markdown
## PostgreSQL review — <file or selection>

**Verdict**: Approved | Fix required | Rejected

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| 1 | High | User input concatenated into SQL | `... WHERE status = '` + input | Bind `:status` through JPQL or a parameterized native query |
| 2 | Medium | JSONB containment query without a GIN index | Seq Scan on `orders` | `CREATE INDEX idx_orders_data ON orders USING gin(data)` |
| 3 | Low | VARCHAR used for case-insensitive email | `email VARCHAR(255)` | Use `CITEXT` with a `CHECK` constraint |

### Corrected SQL
CREATE INDEX idx_orders_data ON orders USING gin(data);
-- The repository query remains parameterized: WHERE data @> :filter
```

## Quality Gate

- [ ] There is a verdict: Approved, Fix required, or Rejected.
- [ ] Every finding has a severity and concrete evidence (file/line or plan excerpt).
- [ ] No user input is concatenated into SQL; all parameters are bound (JPQL, derived query, or bound native query).
- [ ] PostgreSQL-specific types, index types (GIN/GiST/partial), and `CHECK`/`ENUM`/domain constraints have been validated.
- [ ] Personal data, such as CPF or benefit amounts, is masked in logs or documented with a column `COMMENT`.
- [ ] Corrected SQL is ready to paste, and all schema changes can be safely rolled back (see [`database.instructions.md`](../../instructions/database.instructions.md)).
