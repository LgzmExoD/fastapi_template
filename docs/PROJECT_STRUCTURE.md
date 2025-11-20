# Project Structure

```
project/
├── app/
│   ├── api/           # API endpoints and dependencies
│   │   ├── v1/        # Version 1 of the API
│   │   └── deps.py    # Global dependencies (auth, db)
│   ├── core/          # Core config and security
│   ├── db/            # Database session and repositories
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic (optional, can be in repos)
│   ├── utils/         # Utility functions
│   └── main.py        # App entry point
├── alembic/           # Migration scripts
├── docs/              # Documentation
├── scripts/           # Shell scripts for Docker/Startup
├── tests/             # Pytest tests
├── .env.example       # Environment variables template
├── docker-compose.yml # Docker services
├── Dockerfile         # App container definition
├── pyproject.toml     # Python dependencies
└── README.md          # Main documentation
```
