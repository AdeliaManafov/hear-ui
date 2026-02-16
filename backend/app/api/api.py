# app/api/api.py

from fastapi import APIRouter

from app.api.routes import (
    config,
    explainer,
    features,
    feedback,
    model_card,
    patients,
    predict,
    predict_batch,
    utils,
)

api_router = APIRouter()

# Register resource routers without the version prefix. The top-level
# FastAPI app applies the API version (`settings.API_V1_STR`) as a prefix.
api_router.include_router(predict.router)
api_router.include_router(predict_batch.router)
api_router.include_router(utils.router)
api_router.include_router(config.router)
api_router.include_router(feedback.router)
api_router.include_router(explainer.router)
api_router.include_router(features.router)
api_router.include_router(patients.router)
api_router.include_router(model_card.router)
