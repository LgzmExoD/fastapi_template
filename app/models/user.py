"""
User database model with role-based access control and multitenancy support.
"""

import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration for access control."""

    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    User model with authentication and authorization fields.

    Supports multitenancy through optional tenant_id foreign key.
    Superadmins can have null tenant_id to access all tenants.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default=UserRole.USER.value)

    # Multitenancy support - nullable for superadmins
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    tenant = relationship("Tenant", back_populates="users")
