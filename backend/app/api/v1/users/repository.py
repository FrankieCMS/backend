from app.api.v1.users.schema import UserCreate
from app.db.repositories.base import BaseRepository
from app.models.user import User as UserModel
from app.support.hashing import Hashing
from fastapi import HTTPException, status


class UsersRepository(BaseRepository):
    """All database action associated with the User resource"""

    base_model = UserModel

    async def register_user(self, request: UserCreate, hashing: Hashing) -> UserModel:
        user = self.base_model(
            name=request.name,
            email=request.email,
            username=request.username,
            hashed_password=hashing.hash(request.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> UserModel:
        """Find a user by username and return it."""
        user = self.db.query(UserModel).filter(UserModel.username == username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
            )

        return user
