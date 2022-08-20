"""User model."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel


class BaseUser(SQLModel):
    name: str = Field(max_length=100, nullable=True)
    username: str = Field(
        sa_column=Column("name", String(100), nullable=False, unique=True, index=True),
    )
    email: str = Field(
        sa_column=Column("email", String, nullable=False, unique=True, index=True)
    )
    email_verified: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )
    )


class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
