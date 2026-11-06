---
id: postgres
title: PostgreSQL
paths: ["**/*.sql", "**/db/migration/**", "**/migrations/**", "**/flyway/**"]
commands: ["psql", "pg_dump", "flyway"]
---
PostgreSQL.

Schema and migrations
- Every schema change is a new, forward-only migration (Flyway `V<n>__description.sql`, Liquibase, or the framework's tool). Never edit a migration that has run anywhere.
- snake_case, plural table names (`players`, `tag_scans`), singular columns; `id` primary keys, `<table>_id` foreign keys.
- Types: `bigint` or `uuid` ids (`generated always as identity` over `serial`), `timestamptz` for every timestamp, `text` over `varchar(n)` unless a limit is a real rule, `numeric` for money, `jsonb` only for truly schemaless data.
- Constraints in the database: `NOT NULL` by default, foreign keys, `UNIQUE`, and `CHECK` for domain rules.
- Index foreign keys and the columns you filter or sort on; create indexes on large live tables `CONCURRENTLY` (outside a transaction).
- Large-table changes in safe steps: add nullable column, backfill in batches, then add the constraint; avoid long locks.

Queries
- Always parameterized; never build SQL with string concatenation.
- Select the columns you need, not `*`, in application queries.
- Check plans with `EXPLAIN (ANALYZE, BUFFERS)` before and after optimizing; fix N+1 patterns in the application.
- Keep transactions short; set the isolation level deliberately when correctness depends on it.

Working with it
- Read-only exploration first (`psql -c 'select …'`, `\d table`). Ask before running `DELETE`, `UPDATE` without a narrow `WHERE`, `TRUNCATE` or `DROP` against any database with data that matters.
- Location data: PostGIS types (`geography(Point, 4326)`) with GiST indexes, not latitude/longitude float pairs, when distances or areas matter.
