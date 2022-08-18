from datetime import timedelta
from typing import Any

from app.api.dependencies.database import get_repository
from app.api.dependencies.hashing import get_hashing
from app.api.dependencies.mail import get_mailer
from app.api.v1.users.notifications import send_registration_mail
from app.api.v1.users.repository import UsersRepository
from app.core.db import get_db
from app.services.mailer import MailService
from app.support.hashing import Hashing
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from . import schema, services

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register", response_model=schema.UserPublic, status_code=status.HTTP_201_CREATED
)
async def register_user(
    request: schema.UserCreate,
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    hashing: Hashing = Depends(get_hashing),
    mail: MailService = Depends(get_mailer),
) -> str:
    """Register a new user."""
    user = await user_repo.register_user(request, hashing)
    token = hashing.create_token(
        {"id": user.id, "subject": user.username, "email": user.email},
        timedelta(days=7),
    )

    await send_registration_mail(
        email_to=request.email, body={"username": request.username, "token": token}
    )

    return user


@router.get("/me", response_model=schema.UserInDB, status_code=status.HTTP_200_OK)
async def get_own_user(current_user: str = "fbarrento", db: Session = Depends(get_db)):
    """Retrieve the current user."""
    user = await services.get_user_by_username(current_user, db)
    return user


@router.get(
    "/verification",
    response_model=schema.UserInDB,
    status_code=status.HTTP_202_ACCEPTED,
)
async def verify_user_email(
    request: Request,
    token: str,
    hashing: Hashing = Depends(get_hashing),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> Any:
    payload = hashing.decode_token(token)
    user = await user_repo.update_user_email_verified(str(payload.get("subject")))

    return user


@router.get(
    "/{username}", response_model=schema.UserPublic, status_code=status.HTTP_200_OK
)
async def get_user_by_username(
    username: str, user_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    """Retrieve the User with the given username."""
    user = await user_repo.get_user_by_username(username)
    return user
