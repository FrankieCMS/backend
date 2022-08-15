"""FrankieCMS Backend API entrypoint"""
from app.api.v1.router import router as v1_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(v1_router)


@app.get("/")
def root():
    """Welcome Message."""
    return {"Hello": "Mundo!"}


@app.get("/version")
def version():
    """FrankieCMS Version."""
    return {"Version": "1.0.0"}
