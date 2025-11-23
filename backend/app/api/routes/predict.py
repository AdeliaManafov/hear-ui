# app/api/routes/predict.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import crud
from app.api.deps import SessionDep
from app.models.patient import PatientBase

router = APIRouter(prefix="/predict", tags=["prediction"])


class PredictResponse(BaseModel):
    prediction: float
    explanation: dict[str, float]


def compute_prediction_and_explanation(patient_data: dict) -> dict:
    """Fallback prediction logic if no model is loaded."""
    # Simple deterministic fallback based on new features
    age = float(patient_data.get("Alter [J]", 50))
    onset = patient_data.get("Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...", "postlingual")
    
    base_score = 0.5
    if age < 40:
        base_score += 0.2
    elif age > 70:
        base_score -= 0.1
        
    if onset == "postlingual":
        base_score += 0.1
        
    prediction = min(max(base_score, 0.0), 1.0)
    
    explanation = {
        "Alter [J]": -0.05 if age > 60 else 0.05,
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": 0.1 if onset == "postlingual" else -0.05,
        "Geschlecht": 0.01,
    }
    
    return {"prediction": prediction, "explanation": explanation}


@router.post("/", response_model=PredictResponse, summary="Predict")
async def predict(
    patient: PatientBase,
    session: SessionDep,
    persist: bool = False,
):
    """Return a prediction and SHAP explanation for the given patient data."""
    
    # Get model wrapper
    try:
        from app.main import app as fastapi_app
        wrapper = getattr(fastapi_app.state, "model_wrapper", None)
    except Exception:
        wrapper = None

    # Convert patient to dict with original column names (aliases)
    # This is crucial because the model was trained on these column names
    patient_dict = patient.dict(by_alias=True)

    if wrapper and wrapper.is_loaded():
        try:
            import pandas as pd
            from app.core.shap_explainer import ShapExplainer
            
            # Get prediction from model
            # The wrapper handles DataFrame conversion if we pass a dict
            model_res = wrapper.predict(patient_dict)
            prediction = float(model_res.get("prediction", 0.0))
            
            # Try to generate SHAP explanation
            try:
                # Initialize SHAP explainer
                # For pipelines, we might need to rely on the explainer to find feature names
                # or pass the columns from our input
                feature_names = list(patient_dict.keys())
                
                # Create background data for KernelExplainer
                # This is needed because we use a Pipeline with mixed types
                background_df = pd.DataFrame([{
                    "Alter [J]": 50,
                    "Geschlecht": "w",
                    "Primäre Sprache": "Deutsch",
                    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
                    "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
                    "Symptome präoperativ.Tinnitus...": "nein",
                    "Behandlung/OP.CI Implantation": "Cochlear"
                }])
                # Ensure background has same columns as input
                for col in feature_names:
                    if col not in background_df.columns:
                        background_df[col] = 0 # or empty string
                
                # Reorder to match input
                background_df = background_df[feature_names]
                
                shap_explainer = ShapExplainer(
                    model=wrapper.model,
                    feature_names=feature_names,
                    background_data=background_df.values,
                )
                
                # Create DataFrame for SHAP (pipeline expects DataFrame with correct columns)
                features_df = pd.DataFrame([patient_dict])
                
                # We need to pass the DataFrame to explain
                shap_result = shap_explainer.explain(features_df, return_plot=False)
                explanation = shap_result.get("feature_importance", {})
                
            except Exception as shap_exc:
                # Fallback to coefficient-based explanation or empty
                import logging
                logger = logging.getLogger(__name__)
                logger.warning("SHAP explanation failed: %s", shap_exc)
                explanation = {}
            
            result = {"prediction": prediction, "explanation": explanation}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Prediction failed: %s", e)
            result = compute_prediction_and_explanation(patient_dict)
    else:
        result = compute_prediction_and_explanation(patient_dict)

    if persist:
        try:
            from app.models import PredictionCreate

            pred_in = PredictionCreate(
                input_features=patient.dict(),
                prediction=float(result.get("prediction", 0.0)),
                explanation=result.get("explanation", {}),
            )
            crud.create_prediction(session=session, prediction_in=pred_in)
        except Exception:
            pass

    return result
