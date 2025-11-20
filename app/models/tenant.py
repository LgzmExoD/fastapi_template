"""
Tenant database model for multitenancy support.
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Tenant(Base):
    """
    Tenant model for multitenancy implementation.

    Supports both row-based and schema-based multitenancy strategies.
    - Row-based: All tenants share tables, filtered by tenant_id
    - Schema-based: Each tenant has its own PostgreSQL schema
    """

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    schema_name = Column(
        String, unique=True, nullable=True
    )  # For schema-based strategy
    is_active = Column(Boolean, default=True)

    # Relationships
    users = relationship("User", back_populates="tenant")
