# AceAlgoTrade

## Database Migrations

The `db/migrations/001_create_tables.sql` file defines the schema for all core tables:
`users`, `brokers`, `providers`, `accounts`, `symbols`, `symbol_mappings`, `orders`, `trades`,
`positions`, and `provider_endpoints`.

Apply the migration with SQLite:

```bash
sqlite3 mydb.db < db/migrations/001_create_tables.sql
```

## Seed Data

Populate the database with example providers, broker, test user, and sample symbols:

```bash
sqlite3 mydb.db < db/seed.sql
```

## Testing

Run schema validation tests to ensure relationships and constraints remain valid:

```bash
pytest
```

