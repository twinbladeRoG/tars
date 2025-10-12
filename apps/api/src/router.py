from fastapi import APIRouter

from src.modules.users.router import router as user_router

router = APIRouter()

router.include_router(user_router)
