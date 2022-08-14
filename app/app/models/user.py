"""User Model."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from core.db import Base


class User(Base):
    """User model."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        )
