# https://www.jeffastor.com/blog/testing-fastapi-endpoints-with-docker-and-pytest
import os
import warnings

import alembic
import pytest
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient


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
def db(app: FastAPI):
    os.environ["TESTING"] = "1"
    from app.core.config import DATABASE_URL
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    DB_URL = f"{str(DATABASE_URL)}_test"
    engine = create_engine(DB_URL, connect_args={"options": "-c timezone=utc"})

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
