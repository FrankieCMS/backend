"""User Schemas"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    """Base User Schema"""
    name: Optional[str]
    username: str
    email: EmailStr
    password: str

class DisplayUser(BaseModel):
    """Display User Schema"""
    id: int
    name: Optional[str]
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
