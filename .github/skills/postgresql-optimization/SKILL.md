---
name: "postgresql-optimization"
description: "Develop and optimize PostgreSQL using its advanced features: JSONB, array, range, and geometric types, custom types, full-text search, window functions, indexing, and extensions. Use when someone wants to write, tune, or speed up PostgreSQL queries, schemas, or performance. To review existing code, use postgresql-code-review."
---
# PostgreSQL development and optimization

Specialized PostgreSQL guidance for `${selection}` (or the whole project when nothing is selected). Covers PostgreSQL-specific features and optimization patterns: JSONB, arrays, ranges, geometric types, full-text search, window functions, indexing, and the extension ecosystem. To review existing PostgreSQL code rather than create it, use [`postgresql-code-review`](../postgresql-code-review/SKILL.md).

> [!IMPORTANT]
> The SIFAP 2.0 backend runs **PostgreSQL 16** through **JPA/Hibernate**. Create application queries with JPQL, Spring Data derived queries, or bound native parameters, never string-concatenated SQL. Schema changes are delivered as forward-only Flyway migrations in `backend/src/main/resources/db/migration/`. For generic execution plan and index analysis, see [`query-optimization`](../query-optimization/SKILL.md). For migration safety, see [`database.instructions.md`](../../instructions/database.instructions.md). These files are authoritative where there is overlap.

## When to Invoke

- "Write a fast JSONB containment query for this table."
- "Speed up this aggregation; it performs a sequential scan."
- "Design the appropriate index for this filter and sort."
- "Model this with a range type and an exclusion constraint."

## PostgreSQL-specific features

### JSONB operations

```sql
-- Advanced JSONB queries
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- GIN index for JSONB performance
CREATE INDEX idx_events_data_gin ON events USING gin(data);

-- JSONB containment and path queries
SELECT * FROM events
WHERE data @> '{"type": "login"}'
  AND data #>> '{user,role}' = 'admin';

-- JSONB aggregation
SELECT jsonb_agg(data) FROM events WHERE data ? 'user_id';
```

### Array operations

```sql
-- PostgreSQL arrays
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    tags TEXT[],
    categories INTEGER[]
);

-- Array queries and operations
SELECT * FROM posts WHERE 'postgresql' = ANY(tags);
SELECT * FROM posts WHERE tags && ARRAY['database', 'sql'];
SELECT * FROM posts WHERE array_length(tags, 1) > 3;

-- Array aggregation
SELECT array_agg(DISTINCT category) FROM posts, unnest(categories) as category;
```

### Window functions and analytics

```sql
-- Advanced window functions
SELECT
    product_id,
    sale_date,
    amount,
    -- Running totals
    SUM(amount) OVER (PARTITION BY product_id ORDER BY sale_date) as running_total,
    -- Moving averages
    AVG(amount) OVER (PARTITION BY product_id ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg,
    -- Rankings
    DENSE_RANK() OVER (PARTITION BY EXTRACT(month FROM sale_date) ORDER BY amount DESC) as monthly_rank,
    -- Lag/Lead for comparisons
    LAG(amount, 1) OVER (PARTITION BY product_id ORDER BY sale_date) as prev_amount
FROM sales;
```

### Full-text search

```sql
-- PostgreSQL full-text search
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    search_vector tsvector
);

-- Updates the search vector
UPDATE documents
SET search_vector = to_tsvector('english', title || ' ' || content);

-- GIN index for search performance
CREATE INDEX idx_documents_search ON documents USING gin(search_vector);

-- Search queries
SELECT * FROM documents
WHERE search_vector @@ plainto_tsquery('english', 'postgresql database');

-- Ranks the results
SELECT *, ts_rank(search_vector, plainto_tsquery('postgresql')) as rank
FROM documents
WHERE search_vector @@ plainto_tsquery('postgresql')
ORDER BY rank DESC;
```

## PostgreSQL performance tuning

### Query optimization

```sql
-- EXPLAIN ANALYZE for performance analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'::date
GROUP BY u.id, u.name;

-- Identifies slow queries in pg_stat_statements
SELECT query, calls, total_time, mean_time, rows,
       100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

### Index strategies

```sql
-- Composite indexes for multicolumn queries
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Partial indexes for filtered queries
CREATE INDEX idx_active_users ON users(created_at) WHERE status = 'active';

-- Expression indexes for computed values
CREATE INDEX idx_users_lower_email ON users(lower(email));

-- Covering indexes to avoid table lookups
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total, created_at);
```

### Connection and memory management

```sql
-- Checks connection usage
SELECT count(*) as connections, state
FROM pg_stat_activity
GROUP BY state;

-- Monitors memory usage
SELECT name, setting, unit
FROM pg_settings
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem');
```

## Advanced PostgreSQL data types

### Custom types and domains

```sql
-- Creates custom types
CREATE TYPE address_type AS (
    street TEXT,
    city TEXT,
    postal_code TEXT,
    country TEXT
);

CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- Uses domains to validate data
CREATE DOMAIN email_address AS TEXT
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Table using custom types
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email email_address NOT NULL,
    address address_type,
    status order_status DEFAULT 'pending'
);
```

### Range types

```sql
-- PostgreSQL range types
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    reservation_period tstzrange,
    price_range numrange
);

-- Range queries
SELECT * FROM reservations
WHERE reservation_period && tstzrange('2024-07-20', '2024-07-25');

-- Excludes overlapping ranges
ALTER TABLE reservations
ADD CONSTRAINT no_overlap
EXCLUDE USING gist (room_id WITH =, reservation_period WITH &&);
```

### Geometric types

```sql
-- PostgreSQL geometric types
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    coordinates POINT,
    coverage CIRCLE,
    service_area POLYGON
);

-- Geometric queries
SELECT name FROM locations
WHERE coordinates <-> point(40.7128, -74.0060) < 10; -- Within 10 units

-- GiST index for geometric data
CREATE INDEX idx_locations_coords ON locations USING gist(coordinates);
```

## PostgreSQL extensions and tools

### Useful extensions

```sql
-- Enables frequently used extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";     -- Cryptographic functions
CREATE EXTENSION IF NOT EXISTS "unaccent";     -- Removes accents from text
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Trigram matching
CREATE EXTENSION IF NOT EXISTS "btree_gin";    -- GIN indexes for btree types

-- Extension usage
SELECT uuid_generate_v4();                     -- Generates UUIDs
SELECT crypt('password', gen_salt('bf'));      -- Hashes passwords
SELECT similarity('postgresql', 'postgersql'); -- Fuzzy matching
```

### Monitoring queries

```sql
-- Database size and growth
SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;

-- Table and index sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Unused indexes
```

### PostgreSQL-specific optimization tips

- **Use EXPLAIN (ANALYZE, BUFFERS)** for detailed query analysis
- **Configure postgresql.conf** for the workload (OLTP versus OLAP)
- **Use connection pooling** (pgbouncer) in high-concurrency applications
- **Run VACUUM and ANALYZE regularly** for optimal performance
- **Partition large tables** with PostgreSQL 10+ declarative partitioning
- **Use pg_stat_statements** to monitor query performance

## Monitoring and maintenance

### Query performance monitoring

```sql
-- Identifies slow queries
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Checks index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

### Database maintenance

- **VACUUM and ANALYZE**: regular performance maintenance
- **Index maintenance**: monitor and rebuild fragmented indexes
- **Statistics updates**: keep query planner statistics current
- **Log analysis**: regularly review PostgreSQL logs

## Common query patterns

### Pagination

```sql
-- BAD: OFFSET for large datasets
SELECT * FROM products ORDER BY id OFFSET 10000 LIMIT 20;

-- GOOD: cursor-based pagination
SELECT * FROM products
WHERE id > $last_id
ORDER BY id
LIMIT 20;
```

### Aggregation

```sql
-- BAD: inefficient grouping
SELECT user_id, COUNT(*)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY user_id;

-- GOOD: optimized with a partial index
CREATE INDEX idx_orders_recent ON orders(user_id)
WHERE order_date >= '2024-01-01';

SELECT user_id, COUNT(*)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY user_id;
```

### JSON queries

```sql
-- BAD: inefficient JSON query
SELECT * FROM users WHERE data::text LIKE '%admin%';

-- GOOD: JSONB operators and GIN index
CREATE INDEX idx_users_data_gin ON users USING gin(data);

SELECT * FROM users WHERE data @> '{"role": "admin"}';
```

## Optimization checklist

### Query analysis

- [ ] Run EXPLAIN ANALYZE on expensive queries
- [ ] Look for sequential scans on large tables
- [ ] Check whether join algorithms are appropriate
- [ ] Review WHERE clause selectivity
- [ ] Analyze sorting and aggregation operations

### Index strategy

- [ ] Create indexes for frequently queried columns
- [ ] Use composite indexes for multicolumn searches
- [ ] Consider partial indexes for filtered queries
- [ ] Remove unused or duplicate indexes
- [ ] Monitor index bloat and fragmentation

### Security review

- [ ] Use parameterized queries exclusively
- [ ] Implement appropriate access controls
- [ ] Enable row-level security when necessary
- [ ] Audit access to sensitive data
- [ ] Use secure connection methods

### Performance monitoring

- [ ] Set up query performance monitoring
- [ ] Define appropriate logging settings
- [ ] Monitor connection pool usage
- [ ] Track database growth and maintenance needs
- [ ] Configure alerts for performance degradation

## Advanced PostgreSQL features

### Window functions

```sql
-- Running totals and rankings
SELECT
    product_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY product_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY amount DESC) as rank
FROM sales;
```

### Common Table Expressions (CTEs)

```sql
-- Recursive queries for hierarchical data
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 as level
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

Provide specific, actionable PostgreSQL optimizations that improve query performance, security, and maintainability and leverage its advanced features.

## Output Template

Report each optimization as before/after, with the plan change and exact DDL.

```markdown
## PostgreSQL optimization — <query or object>

| Field | Before | After |
|---|---|---|
| p95 latency | <ms> | <ms> |
| Plan | Seq Scan on `orders` | Index Scan on `idx_orders_data` |
| Rows examined | <n> | <n> |

**Change**: index | rewrite | type/constraint | configuration
**DDL**: CREATE INDEX idx_orders_data ON orders USING gin(data);
**Validation**: rerunning EXPLAIN (ANALYZE, BUFFERS) confirms the new plan and lower latency
```

## Quality Gate

- [ ] A baseline plan and latency were captured with `EXPLAIN (ANALYZE, BUFFERS)` before any change.
- [ ] The chosen PostgreSQL feature (JSONB, array, range, full-text search, or window function) suits the access pattern.
- [ ] Indexes match filters, joins, and sorts; each new index is justified against its write cost.
- [ ] Application access remains parameterized (JPQL, derived query, or bound native query), with no string-built SQL.
- [ ] Schema changes are forward-only Flyway migrations and can be safely rolled back.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` confirms the plan change and reduced latency.
