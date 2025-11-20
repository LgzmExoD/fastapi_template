# Database

## Stack

- **PostgreSQL**: Relational database.
- **SQLAlchemy 2.0**: ORM and Query builder.
- **AsyncPG**: High-performance async driver.
- **Alembic**: Migration tool.

## Configuration

Database connection is configured in `app/core/config.py` and `app/db/session.py`.

## Migrations

1.  **Create a revision**:
    ```bash
    alembic revision --autogenerate -m "Description"
    ```

2.  **Apply migrations**:
    ```bash
    alembic upgrade head
    ```

## Repository Pattern

We use a Generic Repository pattern (`app/db/repository.py`) to standardize CRUD operations.

- `get(id)`
- `get_multi(skip, limit)`
- `create(obj_in)`
- `update(db_obj, obj_in)`
- `remove(id)`

Extend `CRUDBase` for specific model needs (e.g., `CRUDUser` in `app/db/repositories/user.py`).
