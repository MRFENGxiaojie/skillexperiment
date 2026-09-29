---
name: database-design
description: Database design principles and decision making. Schema design, indexing strategy, ORM selection, serverless databases. Use when the user asks to design a database schema, choose a database or ORM, optimize indexing or queries, or plan migrations.
allowed-tools: Read, Write, Edit, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Database Design

> **Learn to THINK, not copy SQL patterns.**

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

- Read `database-selection.md` when choosing a database; it covers PostgreSQL vs Neon vs Turso vs SQLite.
- Read `orm-selection.md` when choosing an ORM; it covers Drizzle vs Prisma vs Kysely.
- Read `schema-design.md` when designing schema; it covers normalization, primary keys, and relationships.
- Read `indexing.md` when optimizing performance; it covers index types and composite indexes.
- Read `optimization.md` when optimizing queries; it covers N+1 and EXPLAIN ANALYZE.
- Read `migrations.md` when making schema changes; it covers safe migrations and serverless databases.

---

## ⚠️ Core Principle

- Decide database preferences from available context; ask only if genuinely uncertain and unobtainable
- Choose database/ORM based on CONTEXT
- Do not default to PostgreSQL for everything

---

## Decision Checklist

Before designing the schema:

- [ ] Asked the user about database preference?
- [ ] Chose database for THIS context?
- [ ] Considered the deployment environment?
- [ ] Planned indexing strategy?
- [ ] Defined relationship types?

---

## Anti-Patterns

❌ Defaulting to PostgreSQL for simple apps (SQLite may be enough)
❌ Skipping indexing
❌ Using SELECT * in production
❌ Storing JSON when structured data is better
❌ Ignoring N+1 queries

## Workflow

1. **Identify requirements**: Derive the data model from the request and available context, expected query patterns, scale, and deployment environment
2. **Choose the database**: Use the `database-selection.md` reference to match requirements to the right engine — don't default to PostgreSQL
3. **Design the schema**: Apply normalization principles, define primary keys and relationships, plan indexes for the expected query patterns
4. **Select the ORM**: Match the ORM to the database choice and team context using `orm-selection.md`
5. **Plan migrations**: Define a safe migration strategy, especially for serverless databases where long-running migrations are problematic

## Output Format

A complete database design deliverable includes:

- **Database choice** with rationale (why this engine, not the alternatives)
- **Schema diagram or DDL** showing tables, columns, types, primary keys, foreign keys, and indexes
- **Indexing strategy** — which queries each index supports and why
- **ORM recommendation** with a brief justification

## Limitations

- Does not cover data warehousing, OLAP, or analytical database patterns — focused on application databases
- Does not handle database administration tasks (backup strategy, replication setup, user management)
- Schema designs are starting points — real-world performance requires benchmarking with production-scale data
- Does not replace database-specific documentation — always consult the official docs for version-specific features and limits

