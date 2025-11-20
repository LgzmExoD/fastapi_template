"""
SQLAlchemy declarative base class.
"""

from typing import Any

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Automatically generates table names from class names.
    """

    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.

        Returns:
            Lowercase class name as table name
        """
        return cls.__name__.lower()
