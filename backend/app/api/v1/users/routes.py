from datetime import timedelta
from typing import Any

from app.api.dependencies.database import get_repository
from app.api.dependencies.hashing import get_hashing
from app.api.dependencies.mail import get_mailer
from app.api.v1.users.notifications import send_registration_mail
from app.api.v1.users.repository import UsersRepository
from app.models.user import UserCreate, UserInDB, UserPublic
from app.services.mailer import MailService
from app.support.hashing import Hashing
from fastapi import APIRouter, Depends, Request, status

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register_user(
    request: UserCreate,
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    hashing: Hashing = Depends(get_hashing),
    mail: MailService = Depends(get_mailer),
) -> UserInDB:
    """Register a new user."""
    user = user_repo.register_user(request, hashing)
    token = hashing.create_token(
        {"id": user.id, "subject": user.username, "email": user.email},
        timedelta(days=7),
    )

    await send_registration_mail(
        email_to=request.email, body={"username": request.username, "token": token}
    )

    return user


@router.get(
    "/verification",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
)
async def verify_user_email(
    request: Request,
    token: str,
    hashing: Hashing = Depends(get_hashing),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> Any:
    payload = hashing.decode_token(token)
    user = user_repo.update_user_email_verified(str(payload.get("subject")))

    return user


@router.get("/{username}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str, user_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    """Retrieve the User with the given username."""
    user = user_repo.get_user_by_username(username)
    return user
