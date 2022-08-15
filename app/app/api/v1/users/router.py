from core.db import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import schema, services

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_own_user():
    """Retrieve the current user."""
    return {"message": "Me!!"}


@router.get(
    "/{username}", response_model=schema.DisplayUser, status_code=status.HTTP_200_OK
)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Retrieve the User with the given username."""
    user = await services.get_user_by_username(username, db)
    return user


@router.post(
    "/register", response_model=schema.DisplayUser, status_code=status.HTTP_201_CREATED
)
async def register_user(request: schema.BaseUser, db: Session = Depends(get_db)):
    """Register a new user."""
    user = await services.register_user(request, db)
    return user
