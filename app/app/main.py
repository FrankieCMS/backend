"""FrankieCMS Backend API entrypoint"""
from fastapi import FastAPI

app = FastAPI()

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
