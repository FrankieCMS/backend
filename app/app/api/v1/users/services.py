from sqlalchemy.orm import Session
from models.user import User as UserModel
from . schema import BaseUser


async def register_user(request: BaseUser, db: Session) -> UserModel:
    """Creates a new user in the database."""
    user = UserModel(
        name=request.name,
        email=request.email,
        username=request.username,
        hashed_password=request.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
