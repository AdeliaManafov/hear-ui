from fastapi import APIRouter
from app.api.v1.endpoints import predict, explainer  # shap -> explainer

api_router = APIRouter()

api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
api_router.include_router(explainer.router, prefix="/explainer", tags=["explainer"])  # shap -> explainer
