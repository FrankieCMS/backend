"""User model."""
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from app.support.models.mixins import IDMixin
from pydantic import EmailStr
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import Post


class UserBase(SQLModel):
    __tablename__: str = "users"
    name: str = Field(max_length=100, sa_column=Column("name", String, nullable=True))
    username: str = Field(
        sa_column=Column(
            "username", String(100), nullable=False, unique=True, index=True
        ),
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

    posts: List["Post"] = Relationship(back_populates="post")


class User(IDMixin, UserBase, table=True):
    pass


class UserCreate(SQLModel):
    name: Optional[str]
    username: str
    email: EmailStr
    password: str
    password_confirmation: str


class UserUpdate(UserBase):
    pass


class UserInDB(IDMixin, UserBase):
    """Display User Schema"""

    pass


class UserPublic(IDMixin):
    name: Optional[str]
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
