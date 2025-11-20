"""
Token blacklist repository for logout functionality.
"""

from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select

from app.db.repository import BaseRepository
from app.models.token_blacklist import TokenBlacklist


class TokenBlacklistCreate(BaseModel):
    """Schema for creating a blacklisted token."""

    token: str
    expires_at: datetime


class TokenBlacklistUpdate(BaseModel):
    """Schema for updating a blacklisted token (not used)."""

    pass


class TokenBlacklistRepository(
    BaseRepository[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistUpdate]
):
    """Repository for managing blacklisted tokens."""

    async def is_blacklisted(self, db, token: str) -> bool:
        """
        Check if a token is blacklisted.

        Args:
            db: Database session
            token: JWT token to check

        Returns:
            bool: True if token is blacklisted, False otherwise
        """
        result = await db.execute(
            select(TokenBlacklist).where(TokenBlacklist.token == token)
        )
        return result.scalar_one_or_none() is not None


token_blacklist = TokenBlacklistRepository(TokenBlacklist)
