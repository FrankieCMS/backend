# https://www.jeffastor.com/blog/testing-fastapi-endpoints-with-docker-and-pytest
import os
import warnings

import alembic
import pytest
from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")  # type: ignore
    yield
    alembic.command.downgrade(config, "base")  # type: ignore


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application

    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
