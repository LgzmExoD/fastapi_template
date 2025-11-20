# Architecture

## Overview

The application follows a layered architecture to ensure separation of concerns, scalability, and maintainability.

### Layers

1.  **API Layer (`app/api`)**:
    - Handles HTTP requests and responses.
    - Defines routes and endpoints.
    - Uses Pydantic schemas for validation.
    - Delegates business logic to the Service/Repository layer.

2.  **Service/Repository Layer (`app/db/repositories`)**:
    - Encapsulates database access logic.
    - Implements the Generic Repository pattern (`CRUDBase`).
    - Handles data manipulation and queries.

3.  **Model Layer (`app/models`)**:
    - Defines SQLAlchemy ORM models.
    - Represents the database schema.

4.  **Schema Layer (`app/schemas`)**:
    - Defines Pydantic models for data transfer (DTOs).
    - Handles serialization and validation.

5.  **Core Layer (`app/core`)**:
    - Contains configuration, security, and global dependencies.

## Key Decisions

- **AsyncIO**: The entire stack is async (FastAPI + AsyncPG + SQLAlchemy Async) for high performance.
- **Dependency Injection**: FastAPI's DI system is used for database sessions, current user, and settings.
- **Alembic**: Used for database migrations.
- **Poetry**: Used for dependency management.
