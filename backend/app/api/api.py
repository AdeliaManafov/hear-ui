# app/api/api.py

from fastapi import APIRouter
from app.api.routes import predict, utils
from app.core.config import settings

api_router = APIRouter()

# Only include MVP routes: prediction + small utilities (health check)
api_router.include_router(predict.router, tags=["prediction"], prefix="/api/v1")
api_router.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])
