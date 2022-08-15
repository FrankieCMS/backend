"""User Schemas"""
from datetime import datetime
from typing import Optional

from app.schemas.core import CoreModel, IDModeMixin
from pydantic import EmailStr


class UserBase(CoreModel):
    """Base User Schema"""

    name: Optional[str]
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    password_confirmation: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase, IDModeMixin):
    """Display User Schema"""

    email: str
    email_verification_token: str
    email_verified: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserPublic(UserBase, IDModeMixin):
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
