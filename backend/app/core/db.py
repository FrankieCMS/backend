"""FrankieCMS Database Session Configuration"""
import logging

from app.core import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


engine = create_engine(
    str(config.DATABASE_URL), connect_args={"options": "-c timezone=utc"}
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
