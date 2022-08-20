"""FrankieCMS Database Session Configuration"""
import logging
import os

from app.core import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


DB_URL = (
    f"{config.DATABASE_URL}_test"
    if os.environ.get("TESTING")
    else str(config.DATABASE_URL)
)

engine = create_engine(DB_URL, connect_args={"options": "-c timezone=utc"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():  # type: ignore
    """Get the DB Connection Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
