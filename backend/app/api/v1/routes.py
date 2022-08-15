"""Version 1 Base Router"""
from app.api.v1.users.routes import router as users_router
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(users_router)
