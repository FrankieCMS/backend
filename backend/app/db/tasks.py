import logging

from app.core.config import DATABASE_URL
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def get_engine():
    return create_engine(str(DATABASE_URL), connect_args={"options": "-c timezone=utc"})


async def get_local_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


async def connect_to_db(app: FastAPI) -> None:
    pass
    """engine = create_engine(
        str(DATABASE_URL), connect_args={"options": "-c timezone=utc"}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        app.state._db = SessionLocal()
        logger.warn("INFO: Connected to database.")
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")"""


async def close_db_connection(app: FastAPI) -> None:
    pass

    """try:
        app.state._db.close()
        logger.warn("INFO: Database Connection Closed.")
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")"""
