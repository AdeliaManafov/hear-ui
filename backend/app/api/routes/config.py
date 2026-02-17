"""Configuration routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter(prefix="/config", tags=["config"])


class PredictionThresholdResponse(BaseModel):
    threshold: float


@router.get("/prediction-threshold", response_model=PredictionThresholdResponse)
def get_prediction_threshold() -> PredictionThresholdResponse:
    """Return the configured prediction threshold used by the frontend."""
    return PredictionThresholdResponse(threshold=settings.PREDICTION_THRESHOLD)
