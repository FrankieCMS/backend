"""Version 1 Base Router"""
from api.v1.users.router import router as users_router
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(users_router)
