# app/api/main.py

from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Register API router under versioned prefix used in the project settings
app.include_router(api_router, prefix=settings.API_V1_STR)
