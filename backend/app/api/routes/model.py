from fastapi import APIRouter
from app.core.models.model_card import load_model_card

router = APIRouter()

@router.get("/model-card")
async def get_model_card():
    """Endpoint zum Abrufen der Model Card."""
    return load_model_card()

