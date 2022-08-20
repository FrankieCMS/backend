"""Version 1 Base Router"""
from app.api.v1.posts.routes import router as posts_router
from app.api.v1.users.routes import router as users_router
from fastapi import APIRouter

router = APIRouter(prefix="/v1")

router.include_router(users_router)
router.include_router(posts_router)
