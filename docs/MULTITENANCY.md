# Multitenancy

This template supports two strategies for multitenancy. The strategy can be configured via `MULTITENANCY_STRATEGY` in `.env`.

## 1. Row-Based (Shared Database, Shared Schema)

**Default Strategy.**

All tenants share the same database and tables. Every table has a `tenant_id` column (foreign key to `tenants` table).

### Pros
- **Simplicity**: Easy to manage migrations (one schema).
- **Resource Efficiency**: Connection pooling is efficient.
- **Cross-tenant reporting**: Easy to query across tenants.

### Cons
- **Data Isolation**: Relies on application logic (WHERE clauses). Risk of data leak if developer forgets the filter.
- **Backup/Restore**: Hard to backup/restore a single tenant.

### Implementation
- `app/models/user.py`: `tenant_id` column.
- `app/api/deps.py`: Ensure users can only access data belonging to their tenant (logic needs to be enforced in Repositories).

## 2. Schema-Based (Shared Database, Separate Schemas)

Each tenant has its own schema (namespace) in the same database.

### Pros
- **Data Isolation**: Better than row-based. Postgres enforces schema boundaries.
- **Naming**: Tables have same names in different schemas.

### Cons
- **Migrations**: Complex. Must run migrations for every tenant schema.
- **Connections**: Can be tricky with connection pooling if not managed correctly (search_path).

### Implementation Guide (If switching to Schema-based)

1.  **Middleware**: Create a middleware that extracts tenant ID/subdomain from request.
2.  **Search Path**: Set `SET search_path TO tenant_schema` at the start of the request/session.
3.  **Alembic**: Configure `env.py` to iterate over schemas and apply migrations.

## Current Implementation

The current code implements **Row-Based** primarily.
- `Tenant` model exists.
- `User` model has `tenant_id`.
- API endpoints allow Superadmins to manage Tenants.

To enforce isolation:
- Always filter queries by `tenant_id` in Repositories when the user is not a Superadmin.
