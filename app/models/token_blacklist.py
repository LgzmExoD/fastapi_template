from sqlalchemy import Column, DateTime, String

from app.models.base import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    token = Column(String, primary_key=True, index=True)
    expires_at = Column(DateTime, nullable=False)
