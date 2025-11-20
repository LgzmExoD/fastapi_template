# How to Extend

## Adding a New Resource

1.  **Model**: Create a new file in `app/models/` (e.g., `item.py`). Inherit from `Base`.
2.  **Schema**: Create a new file in `app/schemas/` (e.g., `item.py`). Define `ItemCreate`, `ItemUpdate`, `Item`.
3.  **Repository**: Create a new file in `app/db/repositories/` (e.g., `item.py`). Inherit from `CRUDBase`.
4.  **Endpoint**: Create a new file in `app/api/v1/endpoints/` (e.g., `items.py`). Define routes.
5.  **Router**: Register the new router in `app/api/v1/api.py`.
6.  **Migration**: Run `alembic revision --autogenerate` and `alembic upgrade head`.

## Adding a New Role

1.  Update `UserRole` enum in `app/models/user.py`.
2.  Update `app/api/deps.py` to add a dependency checker for the new role (e.g., `get_current_active_manager`).

## Switching to Schema-Based Multitenancy

1.  Update `MULTITENANCY_STRATEGY` in `.env`.
2.  Implement a middleware to handle schema switching in `app/main.py`.
3.  Update Alembic `env.py` to handle multiple schemas.
