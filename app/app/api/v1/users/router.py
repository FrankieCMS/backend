from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from . import schema, services

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get('/me')
def get_own_user():
    """Retrieve the current user."""
    return {
        'message': 'Me!!'
    }

@router.post('/register', response_model=schema.DisplayUser, status_code=status.HTTP_201_CREATED)
async def register_user(request: schema.BaseUser, db: Session = Depends(get_db) ):
    """Register a new user."""
    user = await services.register_user(request, db)
    return user
