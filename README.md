# FastAPI Multitenant Template

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-00a393.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063.svg)](https://docs.pydantic.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Async](https://img.shields.io/badge/async-100%25-brightgreen.svg)](https://docs.python.org/3/library/asyncio.html)

Production-ready FastAPI template with PostgreSQL, JWT authentication, multitenancy support, and comprehensive analytics.

## 📖 About the Project

This is a professional, production-grade starter template designed for scalable SaaS applications and enterprise APIs. Unlike basic tutorials, this project implements senior-level patterns and best practices out of the box.

It solves the common pain points of starting a new FastAPI project:
- **Multitenancy**: Built-in support for both row-level and schema-level isolation.
- **Authentication**: Robust JWT flow with refresh tokens, blacklisting, and security headers.
- **Architecture**: Clean, maintainable structure using SQLAlchemy 2.0 (Async), Pydantic v2, and Dependency Injection.
- **Developer Experience**: Zero-config setup, auto-reloading, and comprehensive linting (Ruff, Black, MyPy).
- **Observability**: Integrated analytics dashboard and metrics endpoints.

Whether you're building a startup MVP or a microservice for a larger system, this template saves you weeks of boilerplate setup.

## ✨ Features

- **🚀 FastAPI** - Modern async web framework with automatic API documentation
- **🗄️ PostgreSQL** - Async database operations with SQLAlchemy 2.0
- **🔐 JWT Authentication** - Secure token-based auth with refresh tokens and blacklisting
- **👥 Multitenancy** - Row-based and schema-based strategies
- **🎭 RBAC** - Role-Based Access Control (superadmin, admin, user)
- **📊 Analytics** - Built-in metrics and monitoring endpoints
- **🔄 Alembic Migrations** - Database version control
- **✅ Type Safety** - Full type hints with Pydantic v2
- **🐳 Docker Support** - Ready for containerization
- **📝 Auto Documentation** - Swagger UI and ReDoc

## 📊 Analytics Endpoints

The template includes comprehensive analytics for monitoring your application:

- **System Metrics** - Total users, tenants, and activity overview
- **User Metrics** - User distribution by role, activity status, and tenant
- **Tenant Metrics** - Tenant statistics and user distribution
- **Activity Metrics** - Login tracking and engagement data

Access metrics at:
- `GET /api/v1/analytics/system` - Overall system metrics
- `GET /api/v1/analytics/users` - Detailed user metrics
- `GET /api/v1/analytics/tenants` - Detailed tenant metrics
- `GET /api/v1/analytics/activity` - Activity and engagement metrics

### 📈 Visual Dashboard
Access the built-in analytics dashboard at: `http://localhost:8000/api/v1/dashboard`

## 🚀 Quick Start

1. **Configure environment**

Copy `.env.example` to `.env` and update with your PostgreSQL credentials:

```bash
cp .env.example .env
```

2. **Run setup**

```bash
python setup.py
```

3. **Start server**

```bash
python run.py
```

Access the API at http://localhost:8000/docs

## 📁 Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/    # API endpoints (login, users, tenants, analytics)
│       └── api.py        # Router aggregation
├── core/
│   ├── config.py         # Settings management
│   └── security.py       # Auth utilities (JWT, password hashing)
├── db/
│   ├── repositories/     # Data access layer
│   └── session.py        # Database session configuration
├── models/               # SQLAlchemy models
├── schemas/              # Pydantic schemas (request/response)
└── main.py               # Application entry point
```

## 🏢 Multitenancy

The template supports two multitenancy strategies:

### Row-Based (Default)
All tenants share the same database schema. Data is filtered by `tenant_id`.

```env
MULTITENANCY_STRATEGY="row"
```

**Pros:** Simple, efficient for small-medium scale
**Cons:** Shared resources, careful query filtering required

### Schema-Based
Each tenant has its own PostgreSQL schema for complete data isolation.

```env
MULTITENANCY_STRATEGY="schema"
```

**Pros:** Complete data isolation, better for compliance
**Cons:** More complex, higher resource usage

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/login/access-token` - Login (get access + refresh tokens)
- `POST /api/v1/logout` - Logout (blacklist current token)
- `GET /api/v1/login/test-token` - Verify token validity

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users` - List all users (admin only)
- `POST /api/v1/users` - Create new user (admin only)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user (admin only)

### Tenants
- `GET /api/v1/tenants` - List all tenants (superadmin only)
- `POST /api/v1/tenants` - Create new tenant (superadmin only)
- `GET /api/v1/tenants/{id}` - Get tenant by ID (superadmin only)
- `PUT /api/v1/tenants/{id}` - Update tenant (superadmin only)

### Analytics
- `GET /api/v1/analytics/system` - System-wide metrics
- `GET /api/v1/analytics/users` - User statistics and distribution
- `GET /api/v1/analytics/tenants` - Tenant statistics
- `GET /api/v1/analytics/activity?days=30` - Activity metrics

## 🛠️ Development

### Create migration

```bash
alembic revision --autogenerate -m "description"
```

### Apply migrations

```bash
alembic upgrade head
```

### Run tests

```bash
pytest
```

### Code formatting

```bash
black app/
ruff check app/
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJECT_NAME` | Application name | - |
| `SECRET_KEY` | JWT secret key | - |
| `POSTGRES_SERVER` | Database host | localhost |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | - |
| `POSTGRES_DB` | Database name | - |
| `MULTITENANCY_STRATEGY` | Multitenancy mode (`row` or `schema`) | row |
| `FIRST_SUPERUSER_EMAIL` | Initial admin email | - |
| `FIRST_SUPERUSER_PASSWORD` | Initial admin password | - |

## 🐳 Docker

Build and run with Docker:

```bash
docker-compose up -d
```

## 🧪 Testing

Run the test suite:

```bash
pytest --cov=app tests/
```

## 📚 Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🏗️ Architecture

This template follows **Clean Architecture** principles:

- **API Layer** - FastAPI routes and dependencies
- **Business Logic** - Service layer (can be extended)
- **Data Access** - Repository pattern with SQLAlchemy
- **Models** - Database models and Pydantic schemas

## 🔒 Security Features

- ✅ JWT access and refresh tokens
- ✅ Password hashing with bcrypt
- ✅ Token blacklisting for logout
- ✅ Role-based access control (RBAC)
- ✅ SQL injection protection (ORM)
- ✅ XSS protection (Pydantic validation)
- ✅ CORS configuration
- ✅ Environment-based secrets

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- [Python-JOSE](https://github.com/mpdavis/python-jose) - JWT implementation

---

**⭐ If you find this template useful, please consider giving it a star!**
