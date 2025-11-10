# app/api/routes/predict.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter(prefix="/predict", tags=["prediction"])


class PatientData(BaseModel):
    age: int
    hearing_loss_duration: float
    implant_type: str


class PredictResponse(BaseModel):
    prediction: float
    explanation: Dict[str, float]


def dummy_predict(patient: dict) -> dict:
    # Dummy-Vorhersage + SHAP-ähnliche Erklärung
    return {
        "prediction": 0.65,
        "explanation": {
            "age": 0.2,
            "hearing_loss_duration": 0.3,
            "implant_type": 0.15,
            "other_feature": 0.1,
        },
    }


@router.post("/", response_model=PredictResponse, summary="Predict")
async def predict(patient: PatientData):
    """Return a prediction and SHAP-like explanation for the given patient data."""
    return dummy_predict(patient.dict())
