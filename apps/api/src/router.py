from fastapi import APIRouter

from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
