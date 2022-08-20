from datetime import datetime

from app.models.user import User, UserCreate, UserInDB
from app.support.db.repository import Repository
from app.support.hashing import Hashing
from pydantic import EmailStr
from sqlmodel import select


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

    def get_user_by_username(self, username: str) -> UserInDB:
        """Find a user by username and return it."""
        with self.session(self.engine) as session:
            statement = select(self.model).where(User.username == username)
            results = session.exec(statement)
            user = results.first()

        return user  # type: ignore

    def get_user_by_email(self, email: EmailStr) -> UserInDB:
        """Find a user by username and return it."""
        with self.session(self.engine) as session:
            statement = select(self.model).where(User.email == email)
            results = session.exec(statement)
            user = results.first()

        return user  # type: ignore

    def update_user_email_verified(self, username: str) -> UserInDB:
        user = self.get_user_by_username(username)

        with self.session(self.engine) as session:
            user.email_verified = datetime.utcnow()
            session.add(user)
            session.commit()
            session.refresh(user)

        return user  # type: ignore
