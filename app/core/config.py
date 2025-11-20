"""
Application configuration using Pydantic settings.
Loads environment variables from .env file.
"""

from typing import Any, List, Optional

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden via .env file or environment variables.
    """

    # Application
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        """
        Construct database URI from individual components if not provided.

        Args:
            v: Existing database URI if provided
            info: Field validation info containing other field values

        Returns:
            Complete PostgreSQL async database URI
        """
        if isinstance(v, str):
            return v

        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        host = info.data.get("POSTGRES_SERVER")
        port = info.data.get("POSTGRES_PORT")
        db = info.data.get("POSTGRES_DB")

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    # Multitenancy
    MULTITENANCY_STRATEGY: str = "row"  # Options: "row" or "schema"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Initial superuser
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", extra="ignore"
    )


settings = Settings()
