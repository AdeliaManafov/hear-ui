# app/api/api.py

from fastapi import APIRouter

from app.api.routes import feedback, predict, predict_batch, shap, utils, patients

api_router = APIRouter()

# Register resource routers without the version prefix. The top-level
# FastAPI app applies the API version (`settings.API_V1_STR`) as a prefix.
api_router.include_router(predict.router)
api_router.include_router(predict_batch.router)
api_router.include_router(utils.router)
api_router.include_router(feedback.router)
api_router.include_router(shap.router)
api_router.include_router(patients.router)
