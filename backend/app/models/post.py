from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from app.support.models.mixins import IDMixin
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import User


class BasePost(SQLModel):
    __tablename__: str = "posts"
    title: str = Field(index=True)
    content: str
    extended: Optional[dict[str, Any]] = Field(sa_column=Column(JSONB), nullable=True)
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

    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="posts")


class Post(IDMixin, BasePost, table=True):
    pass


class PostCreate(SQLModel):
    title: str
    content: str
    extended: Optional[dict]
    user_id: int

    user: "User" = Relationship(back_populates="posts")
