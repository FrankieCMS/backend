from app.api.server import get_application
from app.db.db import DB_URL, get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URL, connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


print(DB_URL)
exit()


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = get_application()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
