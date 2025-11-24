"""Prediction routes - FIXED VERSION.

This version correctly handles the full pipeline input format.
"""

from typing import Any, Dict
import pandas as pd

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.model_wrapper import ModelWrapper

router = APIRouter(prefix="/predict", tags=["prediction"])
model_wrapper = ModelWrapper()


class PatientData(BaseModel):
    """Patient data matching the pipeline's expected columns."""
    
    # Use Field with alias to map Python-friendly names to German column names
    # All fields are optional to handle missing data gracefully
    alter: float | None = Field(default=50.0, alias="Alter [J]")
    geschlecht: str | None = Field(default="w", alias="Geschlecht")
    primaere_sprache: str | None = Field(default="Deutsch", alias="Primäre Sprache")
    diagnose_beginn: str | None = Field(default="Unbekannt", alias="Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...")
    diagnose_ursache: str | None = Field(default="Unbekannt", alias="Diagnose.Höranamnese.Ursache....Ursache...")
    symptome_tinnitus: str | None = Field(default="nein", alias="Symptome präoperativ.Tinnitus...")
    behandlung_ci: str | None = Field(default="Cochlear", alias="Behandlung/OP.CI Implantation")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Alter [J]": 45,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
                "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
                "Symptome präoperativ.Tinnitus...": "ja",
                "Behandlung/OP.CI Implantation": "Cochlear"
            }
        }


@router.post("/")
def predict(patient: PatientData):
    """Make a prediction for a single patient."""
    try:
        # Convert to dict with German column names (using aliases)
        patient_dict = patient.dict(by_alias=True)
        
        # Create DataFrame (pipeline expects this format)
        df = pd.DataFrame([patient_dict])
        
        # Get prediction from model
        prediction = model_wrapper.model.predict(df)[0]
        
        return {
            "prediction": float(prediction),
            "explanation": {}  # Basic endpoint doesn't include SHAP
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/test")
def _predict_test() -> dict:
    """Simple test endpoint."""
    return {"ok": True, "model_loaded": model_wrapper.is_loaded()}


def compute_prediction_and_explanation(patient: Dict[str, Any]) -> Dict[str, Any]:
    """Compute prediction for a patient dict (used by batch endpoint).
    
    Args:
        patient: Dict with German column names
        
    Returns:
        Dict with prediction and empty explanation
    """
    # The ModelWrapper handles preprocessing and accepts a raw dict with
    # canonical keys. Prefer using `model_wrapper.predict` so batch upload can
    # provide flexible input (headers normalized before calling this function).
    try:
        res = model_wrapper.predict(patient)
        # model_wrapper.predict may return an array-like of probabilities or a
        # scalar; normalize to float
        try:
            # If it's array-like, take first element
            prediction = float(res[0])
        except Exception:
            prediction = float(res)
        return {"prediction": prediction, "explanation": {}}
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
