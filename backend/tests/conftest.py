# https://www.jeffastor.com/blog/testing-fastapi-endpoints-with-docker-and-pytest
import os
import warnings
from typing import Type

import alembic
import pytest
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.future import Engine
from sqlmodel import Session


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
@pytest.fixture()
def db_session(app: FastAPI) -> Type[Session]:
    os.environ["TESTING"] = "1"
    return Session


@pytest.fixture()
def db_engine(app: FastAPI) -> Engine:
    os.environ["TESTING"] = "1"
    from app.db.connection import engine

    return engine


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
