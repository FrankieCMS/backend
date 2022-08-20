from app.core import config
from sqlmodel import SQLModel, create_engine

DB_URL = (
    f"{config.DATABASE_URL}_test"
    if os.environ.get("TESTING")
    else str(config.DATABASE_URL)
)


engine = create_engine(DB_URL, echo=True, connect_args={"options": "-c timezone=utc"})
