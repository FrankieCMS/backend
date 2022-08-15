import pytest
from app.api.v1.users.repository import UsersRepository
from app.support.hashing import Hashing
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestUserRegistration:
    @pytest.mark.asyncio
    async def test_register_user(self, app: FastAPI, client: TestClient):
        response = client.post(
            "/api/v1/users/register",
            json={
                "name": "Francisco Barrento",
                "username": "fbarrento",
                "email": "francisco.barrento@gmail.com",
                "password": "password",
                "password_confirmation": "string",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "francisco.barrento@gmail.com"
        assert "id" in data
        user_id = data["id"]
        username = data["username"]

        response = client.get(f"/api/v1/users/{username}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "francisco.barrento@gmail.com"
        assert data["id"] == user_id

    @pytest.mark.asyncio
    async def test_password_is_encrypted(self, db: Session):
        user_repo = UsersRepository(db=db)

        user = await user_repo.get_user_by_username("fbarrento")
        assert user.hashed_password != "password"
        hashing = Hashing()

        assert hashing.verify_hash("password", str(user.hashed_password))
