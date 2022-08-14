"""FrankieCMS Backend API entrypoint"""
from fastapi import FastAPI

from api.v1.router import router as v1_router

app = FastAPI()

app.include_router(v1_router)

@app.get('/')
def root():
    """Welcome Message."""
    return {
        'Hello': 'Mundo!'
    }

@app.get('/version')
def version():
    """FrankieCMS Version."""
    return {
        'Version': "1.0.0"
    }
