"""
Database initialization script.
Creates initial superuser if it doesn't exist.
"""

import asyncio
import logging

from app.core.config import settings
from app.db.repositories.user import user as user_repo
from app.db.session import AsyncSessionLocal
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_initial_data() -> None:
    """
    Create initial database data including superuser.

    Checks if superuser exists and creates one if not found.
    """
    async with AsyncSessionLocal() as session:
        user = await user_repo.get_by_email(
            session, email=settings.FIRST_SUPERUSER_EMAIL
        )

        if not user:
            logger.info(f"Creating superuser: {settings.FIRST_SUPERUSER_EMAIL}")
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                full_name="Initial Super User",
                role="superadmin",
                is_active=True,
            )
            await user_repo.create(session, data=user_in)
            logger.info("Superuser created successfully")
        else:
            logger.info(f"Superuser already exists: {settings.FIRST_SUPERUSER_EMAIL}")


async def main() -> None:
    """Main entry point for database initialization."""
    logger.info("Initializing database data...")
    await create_initial_data()
    logger.info("Database initialization complete.")


if __name__ == "__main__":
    asyncio.run(main())
