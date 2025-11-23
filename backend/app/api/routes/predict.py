"""Prediction routes.

This module exposes a `router` with prefix `/predict` and a helper
`compute_prediction_and_explanation` used by the batch endpoint and tests.
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.model_wrapper import ModelWrapper

router = APIRouter(prefix="/predict", tags=["prediction"])
model_wrapper = ModelWrapper()


class PatientData(BaseModel):
    age: float | None = None
    hearing_loss_duration: float | None = None
    implant_type: str | None = None


@router.post("/")
def predict(patient: PatientData):
    try:
        return compute_prediction_and_explanation(patient.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def _predict_test() -> dict:
    """Simple test endpoint to verify import and routing."""
    return {"ok": True}


def compute_prediction_and_explanation(patient: Dict[str, Any]) -> Dict[str, Any]:
    """Compute prediction and explanation for a single patient dict.

    The signature is intentionally simple so other modules (batch/test)
    can import and call it directly.
    """
    # 1) Prepare input
    try:
        X = model_wrapper.prepare_input(patient)
    except Exception as exc:
        raise ValueError(f"Preprocessing failed: {exc}")

    # 2) Predict
    try:
        raw_out = model_wrapper.predict(X)
        try:
            pred_val = float(raw_out[0])
        except Exception:
            pred_val = float(raw_out)
    except Exception as exc:
        raise RuntimeError(f"Prediction failed: {exc}")

    # 3) Explanation: SHAP then coefficient fallback
    explanation: Dict[str, float] = {}
    try:
        import shap

        explainer = shap.Explainer(model_wrapper.model, X)
        shap_vals = explainer(X)
        vals = shap_vals.values[0] if hasattr(shap_vals, "values") else shap_vals[0]
        if hasattr(X, "columns"):
            names = list(X.columns)
        else:
            names = getattr(model_wrapper.model, "feature_names_in_", [f"f{i}" for i in range(len(vals))])
        explanation = {n: float(v) for n, v in zip(names, vals)}
    except Exception:
        try:
            mod = model_wrapper.model
            if hasattr(mod, "coef_"):
                coef = mod.coef_[0]
                if hasattr(X, "iloc"):
                    xvals = X.iloc[0].values
                else:
                    xvals = X[0] if hasattr(X, "__iter__") else X
                if hasattr(X, "columns"):
                    names = list(X.columns)
                else:
                    names = getattr(mod, "feature_names_in_", [f"f{i}" for i in range(len(coef))])
                explanation = {n: float(c * xv) for n, c, xv in zip(names, coef, xvals)}
        except Exception:
            explanation = {}

    return {"prediction": float(pred_val), "explanation": explanation}

