# app/api/routes/predict.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["prediction"])

class PatientData(BaseModel):
    age: int
    hearing_loss_duration: float
    implant_type: str

def dummy_predict(patient: dict) -> dict:
    # Dummy-Vorhersage + SHAP-ähnliche Erklärung
    return {
        "prediction": 0.65,
        "explanation": {
            "age": 0.2,
            "hearing_loss_duration": 0.3,
            "implant_type": 0.15,
            "other_feature": 0.1
        }
    }

@router.post("/predict")
async def predict(patient: PatientData):
    return dummy_predict(patient.dict())
