"""
Database connection health check with retry logic.
Ensures database is ready before application starts.
"""

import logging

from sqlalchemy import text
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)

from app.db.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_RETRIES = 60 * 5  # 5 minutes worth of retries
RETRY_WAIT_SECONDS = 1


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_fixed(RETRY_WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def check_db_connection() -> None:
    """
    Verify database connection is available.

    Raises:
        Exception: If database connection fails after all retries
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


async def main() -> None:
    """Main entry point for database health check."""
    logger.info("Checking database connection...")
    await check_db_connection()
    logger.info("Database connection established successfully.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
