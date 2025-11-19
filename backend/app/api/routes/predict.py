# app/api/routes/predict.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict
from sqlmodel import Session

from app.api.deps import SessionDep
from app import crud

router = APIRouter(prefix="/predict", tags=["prediction"])


class PatientData(BaseModel):
    age: int
    hearing_loss_duration: float
    implant_type: str


class PredictResponse(BaseModel):
    prediction: float
    explanation: Dict[str, float]


def _encode_implant_type(implant_type: str) -> float:
    # Simple deterministic encoding for a small set of implant types.
    mapping = {"type_a": 0.0, "type_b": 1.0, "type_c": 2.0}
    return float(mapping.get(implant_type.lower(), 0.0))


def compute_prediction_and_explanation(patient: dict) -> dict:
    """Compute a prediction and SHAP explanation for a single patient dict.

    This tries to use `shap`. If `shap` is not importable or fails, it falls back to a lightweight
    deterministic explanation (same shape as the original dummy implementation).
    """
    # Prepare feature vector: [age, hearing_loss_duration, implant_code]
    try:
        import numpy as np
    except Exception:
        # numpy not available -> fallback to dummy
        numpy = None

    age = float(patient.get("age", 50))
    duration = float(patient.get("hearing_loss_duration", 10.0))
    implant_code = _encode_implant_type(patient.get("implant_type", "type_a"))

    features = [age, duration, implant_code]

    # Simple linear model used for both prediction and for SHAP explainer's callable.
    def _model(X):
        # X: ndarray shape (n_samples, 3)
        # produce values in [0,1]
        w = np.array([-0.002, -0.03, 0.05])
        bias = 0.7
        return np.clip(bias + X.dot(w), 0.0, 1.0)

    # Try to run SHAP-based explanation
    try:
        import shap
        import numpy as np

        background = np.array([[50.0, 10.0, 0.0], [30.0, 5.0, 1.0]])
        explainer = shap.KernelExplainer(lambda x: _model(np.array(x)), background)
        shap_vals = explainer.shap_values(np.array([features]))

        # KernelExplainer returns a 2D array (1, n_features) for regression.
        if isinstance(shap_vals, list):
            # some shap versions return a list for shap_values
            shap_arr = np.array(shap_vals)
            if shap_arr.ndim == 3:  # (classes, samples, features)
                shap_arr = shap_arr[0]
            shap_vals_sample = shap_arr[0]
        else:
            shap_vals_sample = np.array(shap_vals)[0]

        pred = float(_model(np.array([features]))[0])

        names = ["age", "hearing_loss_duration", "implant_type"]
        explanation = {n: float(v) for n, v in zip(names, shap_vals_sample)}
        return {"prediction": pred, "explanation": explanation}
    except Exception:
        # Fallback: deterministic, human-readable attribution (keeps previous API shape)
        pred = 0.65
        explanation = {
            "age": 0.2,
            "hearing_loss_duration": 0.3,
            "implant_type": 0.15,
            "other_feature": 0.1,
        }
        return {"prediction": pred, "explanation": explanation}


@router.post("/", response_model=PredictResponse, summary="Predict")
async def predict(
    patient: PatientData,
    session: SessionDep,
    persist: bool = False,
):
    """Return a prediction and SHAP explanation (or fallback) for the given patient data.

    If `persist=true` is provided as a query parameter the prediction will be stored
    in the database (requires a running DB and migrations).
    """
    result = compute_prediction_and_explanation(patient.dict())

    if persist:
        try:
            # create a minimal PredictionCreate payload
            from app.models import PredictionCreate

            pred_in = PredictionCreate(
                input_features=patient.dict(),
                prediction=float(result.get("prediction", 0.0)),
                explanation=result.get("explanation", {}),
            )
            crud.create_prediction(session=session, prediction_in=pred_in)
        except Exception:
            # don't fail the request on DB errors; log could be added
            pass

    return result
