# Sources

Source evaluations live here, one directory per source system. Sources are independent of data products — a single source evaluation is reusable across multiple data products.

## Directory Structure

```
docs/sources/
  <source-name>/
    evaluation.md       # From dos:evaluate-source
```

## Naming Convention

Use a descriptive, hyphenated name that identifies the source system: `postgres-orders-db`, `stripe-api`, `s3-clickstream-logs`. The name should be unambiguous if the organization has multiple instances of the same technology.

## Relationship to Data Products

Source evaluations are consumed by `dos:scope-data-product`, which declares which sources a data product uses. The scope document in `docs/data-products/<name>/scope.md` references sources by name.

## Source Evaluations

| Source | Description |
|--------|-------------|
| _(none yet)_ | |
