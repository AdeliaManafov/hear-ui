# app/api/api.py

from fastapi import APIRouter
from app.api.routes import predict, predict_batch, utils, feedback
from app.core.config import settings

api_router = APIRouter()

# Register resource routers without the version prefix. The top-level
# FastAPI app applies the API version (`settings.API_V1_STR`) as a prefix.
api_router.include_router(predict.router)
api_router.include_router(predict_batch.router)
api_router.include_router(utils.router)
api_router.include_router(feedback.router)
