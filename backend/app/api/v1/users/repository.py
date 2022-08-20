from datetime import datetime

from app.models.user import User, UserCreate, UserInDB
from app.support.db.repository import Repository
from app.support.hashing import Hashing
from fastapi import HTTPException, status
from sqlmodel import SQLModel, select


class UsersRepository(Repository):
    """All database action associated with the User resource"""

    model = User

    def register_user(self, request: UserCreate, hashing: Hashing) -> UserInDB:
        user = self.model(
            name=request.name,
            email=request.email,
            username=request.username,
            hashed_password=hashing.hash(request.password),
        )

        with self.session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

            return user  # type: ignore

    def get_user_by_username(self, username: str) -> SQLModel:
        """Find a user by username and return it."""
        with self.session(self.engine) as session:
            statement = select(self.model).where(User.username == username)
            results = session.exec(statement)
            user = results.first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
            )

        return user

    def update_user_email_verified(self, username: str) -> SQLModel:
        user = self.get_user_by_username(username)

        with self.session(self.engine) as session:
            user.email_verified = datetime.utcnow()
            session.add(user)
            session.commit()
            session.refresh(user)

        return user
