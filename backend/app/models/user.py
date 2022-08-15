"""User model."""
from uuid import uuid4

from app.core.db import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    email_verification_token = Column(
        String, nullable=False, unique=True, index=True, default=uuid4()
    )
    email_verified = Column(DateTime(timezone=True), nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
