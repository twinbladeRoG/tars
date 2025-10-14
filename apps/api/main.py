from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.router import router

app = FastAPI()

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(router, prefix="/api")
