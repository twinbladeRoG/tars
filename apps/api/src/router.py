from fastapi import APIRouter

from src.modules.agent.router import router as agent_router
from src.modules.auth.router import router as auth_router
from src.modules.candidate.router import router as candidate_router
from src.modules.file_storage.router import router as file_storage_router
from src.modules.knowledge_base.router import router as knowledge_base_router
from src.modules.users.router import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(agent_router)
router.include_router(knowledge_base_router)
router.include_router(file_storage_router)
router.include_router(candidate_router)
