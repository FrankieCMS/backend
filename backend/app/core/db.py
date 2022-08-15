"""FrankieCMS Database Session Configuration"""
import logging
import os

from core import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

DATABASE_DRIVER = config.DATABASE_DRIVER
DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = (
    f"{config.DATABASE_NAME}" if os.environ.get("TESTING") else config.DATABASE_NAME
)

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@\
{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"options": "-c timezone=utc"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get the DB Connection Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
