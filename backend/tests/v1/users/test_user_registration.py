from typing import Type

import pytest
from app.api.v1.users.repository import UsersRepository
from app.support.hashing import Hashing
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.future import Engine
from sqlmodel import Session


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
                "password_confirmation": "password",
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
    async def test_passwords_must_match_if_password_is_not_matched(
        self, app: FastAPI, client: TestClient
    ):
        response = client.post(
            "/api/v1/users/register",
            json={
                "name": "Francisco Barrento",
                "username": "fbarrento",
                "email": "francisco.barrento@gmail.com",
                "password": "password",
                "password_confirmation": "other_password",
            },
        )

        data = response.json()

        assert data["detail"] == "The passwords don't match."
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_username_must_be_unique(self, app: FastAPI, client: TestClient):
        response = client.post(
            "/api/v1/users/register",
            json={
                "name": "Francisco Barrento",
                "username": "fbarrento",
                "email": "francisco.barrento@gmail.com",
                "password": "password",
                "password_confirmation": "password",
            },
        )

        data = response.json()

        assert data["detail"] == "Username already exists."
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.asyncio
    async def test_email_must_be_unique(self, app: FastAPI, client: TestClient):
        response = client.post(
            "/api/v1/users/register",
            json={
                "name": "Francisco Barrento",
                "username": "fbarrentos",
                "email": "francisco.barrento@gmail.com",
                "password": "password",
                "password_confirmation": "password",
            },
        )

        data = response.json()

        assert data["detail"] == "Email already exists."
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.asyncio
    async def test_password_is_encrypted(
        self, db_session: Type[Session], db_engine: Engine
    ):
        user_repo = UsersRepository(session=db_session, engine=db_engine)

        user = user_repo.get_user_by_username("fbarrento")
        assert (user.hashed_password,) != "password"
        hashing = Hashing()

        assert hashing.verify_hash("password", str(user.hashed_password))
