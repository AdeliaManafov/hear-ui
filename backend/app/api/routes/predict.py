"""Prediction routes - FIXED VERSION.

This version correctly handles the full pipeline input format.
"""

from typing import Any, Dict
import pandas as pd

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.core.model_wrapper import ModelWrapper
from app.api.deps import SessionDep
from sqlmodel import Session
from app.models import Prediction
from app.core.background_data import create_synthetic_background
from app.core.shap_explainer import ShapExplainer

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
    
    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
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
    }


@router.post("/")
def predict(patient: PatientData, db: SessionDep, persist: bool = False):
    """Make a prediction for a single patient."""
    try:
        # Convert to dict with German column names (using aliases)
        patient_dict = patient.model_dump(by_alias=True)
        
        # Use model_wrapper.predict which handles preprocessing
        result = model_wrapper.predict(patient_dict)
        
        # Extract scalar prediction
        try:
            prediction = float(result[0])
        except (TypeError, IndexError):
            prediction = float(result)

        # Persist prediction to DB when requested
        if persist:
            try:
                pred = Prediction(input_features=patient_dict, prediction=float(prediction), explanation={})
                db.add(pred)
                db.commit()
                db.refresh(pred)
            except Exception:
                # Do not fail the request if DB persistence fails; log silently
                pass

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
        # model_wrapper.predict may return array-like; normalize to float
        try:
            prediction = float(res[0])
        except Exception:
            prediction = float(res)

        # Attempt to produce a SHAP-based explanation. Use a synthetic
        # background appropriate for the pipeline and fall back gracefully
        # if SHAP or background transformation fails.
        explanation: dict = {}
        try:
            # Only attempt if model is loaded
            if model_wrapper.model is not None:
                raw_bg, transformed = create_synthetic_background(n_samples=50, include_transformed=True, pipeline=model_wrapper.model)
                explainer = ShapExplainer(model_wrapper.model, feature_names=None, background_data=raw_bg, use_transformed=True)

                # Prepare single sample for explainer (ModelWrapper.prepare_input handles mapping)
                sample_df = model_wrapper.prepare_input(patient)
                # Convert DataFrame/array to numpy array for explainer
                try:
                    sample_arr = sample_df.values if hasattr(sample_df, 'values') else sample_df
                except Exception:
                    sample_arr = sample_df

                shap_res = explainer.explain(sample_arr)
                feat_imp = shap_res.get('feature_importance', {}) if isinstance(shap_res, dict) else {}

                # Map detailed feature names back to canonical short keys expected by tests
                mapping = {
                    'age': ['alter', 'age'],
                    'hearing_loss_duration': ['dauer', 'hearing', 'höranamnese'],
                    'implant_type': ['implant', 'ci implantation', 'behandlung'],
                }

                # Aggregate importance for canonical keys
                for short, tokens in mapping.items():
                    total = 0.0
                    for name, val in feat_imp.items():
                        lname = name.lower()
                        if any(tok in lname for tok in tokens):
                            try:
                                total += float(val)
                            except Exception:
                                continue
                    explanation[short] = total
        except Exception:
            # If anything fails during explanation, return empty explanation but keep prediction
            explanation = {}

        return {"prediction": prediction, "explanation": explanation}
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
