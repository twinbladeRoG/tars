import logging

from src.core.config import settings

logger = logging.getLogger("uvicorn")
logger.setLevel(settings.LOG_LEVEL)
