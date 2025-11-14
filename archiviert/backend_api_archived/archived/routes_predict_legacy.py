from fastapi import APIRouter
from pydantic import BaseModel
from app.core.predict import dummy_predict

router = APIRouter(prefix="/api/v1", tags=["prediction"])

class PatientData(BaseModel):
    age: int
    hearing_loss_duration: float
    implant_type: str
    # weitere Felder nach Bedarf

@router.post("/predict")
async def predict(patient: PatientData):
    result = dummy_predict(patient.dict())
    return result
