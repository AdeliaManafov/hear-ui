"""Prediction routes - FIXED VERSION.

This version correctly handles the full pipeline input format.
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.api.deps import SessionDep
from app.core.background_data import create_synthetic_background
from app.core.shap_explainer import ShapExplainer
from app.models import Prediction

router = APIRouter(prefix="/predict", tags=["prediction"])


class PatientData(BaseModel):
    """Patient data matching the pipeline's expected columns.

    All fields are optional. When a field is omitted, the preprocessor will use
    its own defaults (typically 0 for numeric, empty/unknown for categorical).
    DO NOT add defaults here as they can silently change predictions.
    """

    # Use Field with alias to map Python-friendly names to German column names
    alter: float | None = Field(default=None, alias="Alter [J]")
    geschlecht: str | None = Field(default=None, alias="Geschlecht")
    primaere_sprache: str | None = Field(default=None, alias="Primäre Sprache")
    diagnose_beginn: str | None = Field(
        default=None, alias="Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..."
    )
    diagnose_ursache: str | None = Field(
        default=None, alias="Diagnose.Höranamnese.Ursache....Ursache..."
    )
    symptome_tinnitus: str | None = Field(
        default=None, alias="Symptome präoperativ.Tinnitus..."
    )
    behandlung_ci: str | None = Field(
        default=None, alias="Behandlung/OP.CI Implantation"
    )

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
                "Behandlung/OP.CI Implantation": "Cochlear",
            }
        },
    }


@router.post("/")
def predict(
    patient: PatientData, db: SessionDep, request: Request, persist: bool = False
):
    """Make a prediction for a single patient."""
    # DEBUG: force output to stderr
    import sys

    print("[DEBUG PREDICT] Entered predict function", file=sys.stderr, flush=True)

    # Use the canonical model wrapper from app state
    model_wrapper = request.app.state.model_wrapper
    print(
        f"[DEBUG PREDICT] Wrapper ID: {id(model_wrapper)}, loaded={model_wrapper.is_loaded()}",
        file=sys.stderr,
        flush=True,
    )

    if not model_wrapper or not model_wrapper.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert to dict with German column names (using aliases)
        patient_dict = patient.model_dump(by_alias=True)
        print(
            f"[DEBUG PREDICT] Patient dict: {patient_dict}", file=sys.stderr, flush=True
        )

        # Use model_wrapper.predict which handles preprocessing
        # clip=True enforces probability bounds [1%, 99%]
        result = model_wrapper.predict(patient_dict, clip=True)
        print(f"[DEBUG PREDICT] Raw result: {result}", file=sys.stderr, flush=True)

        # Extract scalar prediction
        try:
            prediction = float(result[0])
        except (TypeError, IndexError):
            prediction = float(result)

        # Persist prediction to DB when requested
        persist_error: str | None = None
        persisted_id: str | None = None

        if persist:
            try:
                pred = Prediction(
                    input_features=patient_dict,
                    prediction=float(prediction),
                    explanation={},
                )
                db.add(pred)
                db.commit()
                db.refresh(pred)
                persisted_id = str(pred.id)
            except Exception as e:
                # Log the error but don't fail the request
                import logging

                logging.getLogger(__name__).warning(
                    f"Failed to persist prediction: {e}"
                )
                persist_error = str(e)
                # Rollback to clean state
                try:
                    db.rollback()
                except Exception:
                    pass

        response = {
            "prediction": float(prediction),
            "explanation": {},  # Basic endpoint doesn't include SHAP
        }

        # Include persistence info when persist=true was requested
        if persist:
            response["persisted"] = persist_error is None
            if persisted_id:
                response["prediction_id"] = persisted_id
            if persist_error:
                response["persist_error"] = persist_error

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


def compute_prediction_and_explanation(
    patient: dict[str, Any], model_wrapper
) -> dict[str, Any]:
    """Compute prediction for a patient dict (used by batch endpoint).

    Args:
        patient: Dict with German column names
        model_wrapper: The ModelWrapper instance to use

    Returns:
        Dict with prediction and empty explanation
    """
    # The ModelWrapper handles preprocessing and accepts a raw dict with
    # canonical keys. Prefer using `model_wrapper.predict` so batch upload can
    # provide flexible input (headers normalized before calling this function).
    try:
        # clip=True enforces probability bounds [1%, 99%]
        res = model_wrapper.predict(patient, clip=True)
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
                raw_bg, transformed = create_synthetic_background(
                    n_samples=50, include_transformed=True, pipeline=model_wrapper.model
                )
                explainer = ShapExplainer(
                    model_wrapper.model,
                    feature_names=None,
                    background_data=raw_bg,
                    use_transformed=True,
                )

                # Prepare single sample for explainer (ModelWrapper.prepare_input handles mapping)
                sample_df = model_wrapper.prepare_input(patient)
                # Convert DataFrame/array to numpy array for explainer
                try:
                    sample_arr = (
                        sample_df.values if hasattr(sample_df, "values") else sample_df
                    )
                except Exception:
                    sample_arr = sample_df

                shap_res = explainer.explain(sample_arr)
                feat_imp = (
                    shap_res.get("feature_importance", {})
                    if isinstance(shap_res, dict)
                    else {}
                )

                # Map detailed feature names back to canonical short keys expected by tests
                mapping = {
                    "age": ["alter", "age"],
                    "hearing_loss_duration": ["dauer", "hearing", "höranamnese"],
                    "implant_type": ["implant", "ci implantation", "behandlung"],
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
