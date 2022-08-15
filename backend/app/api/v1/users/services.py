from app.models.user import User as UserModel
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .schema import UserCreate


async def register_user(request: UserCreate, db: Session) -> UserModel:
    """Creates a new user in the database."""
    user = UserModel(
        name=request.name,
        email=request.email,
        username=request.username,
        hashed_password=request.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_user_by_username(username: str, db: Session) -> UserModel:
    """Find a user by username and return it."""
    user = db.query(UserModel).filter(UserModel.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    return user
