# Filename: app/models/base.py
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declared_attr
from app.database import Base

class BaseMixin:
    """
    A base class for SQLAlchemy models that provides a
    common `id` column and a simple table name convention.
    """
    @declared_attr
    def __tablename__(cls):
        """Generates a pluralized table name from the class name."""
        return cls.__name__.lower() + 's'

    id = Column(Integer, primary_key=True, index=True)
