import logging

import alembic
from alembic.config import Config
from app.db.connection import engine
from app.models import Post, User  # noqa: F401
from fastapi import FastAPI
from sqlmodel import SQLModel  # noqa: F401

logger = logging.getLogger(__name__)


def get_engine():
    return engine


async def apply_db_migrations(app: FastAPI) -> None:
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")  # type: ignore
    logger.warn("INFO:     Updating Database Schema.")


async def close_db_connection(app: FastAPI) -> None:
    pass

    """try:
        app.state._db.close()
        logger.warn("INFO: Database Connection Closed.")
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")"""
