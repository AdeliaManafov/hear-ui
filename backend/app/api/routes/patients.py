from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import logging

from app.api.deps import get_db
from app import crud
from app.models import Patient, PatientCreate
from app.api.routes import explainer as explainer_route
from app.api.routes.explainer import ShapVisualizationRequest

router = APIRouter(prefix="/patients", tags=["patients"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[Patient])
def list_patients_api(session: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    return crud.list_patients(session=session, limit=limit, offset=offset)


@router.get("/{patient_id}", response_model=Patient)
def get_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    p = crud.get_patient(session=session, patient_id=patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p


@router.get("/{patient_id}/predict")
def predict_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    """Return prediction for a stored patient (uses existing compute helper)."""
    try:
        p = crud.get_patient(session=session, patient_id=patient_id)
        if not p:
            raise HTTPException(status_code=404, detail="Patient not found")

        input_features = p.input_features or {}
        
        if not input_features:
            raise HTTPException(status_code=400, detail="Patient has no input features")

        # Prefer the app-level model wrapper (app.state) so we rely on the same
        # wrapper instance the rest of the application uses (and its load status).
        try:
            from app.main import app as fastapi_app
            wrapper = getattr(fastapi_app.state, "model_wrapper", None)
        except Exception:
            wrapper = None

        if not wrapper or not wrapper.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")

        try:
            model_res = wrapper.predict(input_features)
            # extract a scalar prediction from different possible return types
            try:
                prediction = float(model_res[0])
            except (TypeError, IndexError):
                prediction = float(model_res)
            return {"prediction": prediction, "explanation": {}}
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Prediction failed for patient %s", patient_id)
            raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in predict_patient_api for %s", patient_id)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}/explainer")
async def explainer_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    """Return SHAP explanation for a stored patient by delegating to the SHAP route.

    This constructs a `ShapVisualizationRequest` from the saved input_features
    and calls the existing SHAP handler.
    """
    p = crud.get_patient(session=session, patient_id=patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    input_features = p.input_features or {}

    if not input_features:
        raise HTTPException(status_code=400, detail="Patient has no input features")

    # Build request data from input_features, mapping to expected field names
    def _get_value(keys, default):
        for k in keys:
            if k in input_features:
                return input_features[k]
        return default

    def _bool_to_ja_nein(v):
        if isinstance(v, bool):
            return "ja" if v else "nein"
        if v is None:
            return "nein"
        return str(v)

    # Extract age with fallback
    age_val = _get_value(["Alter [J]", "alter", "age"], 50)
    try:
        age = int(float(age_val))
    except Exception:
        age = 50

    req_data = {
        "age": age,
        "gender": str(_get_value(["Geschlecht", "geschlecht", "gender"], "w")),
        "primary_language": str(_get_value(["Primäre Sprache", "primary_language"], "Deutsch")),
        "hearing_loss_onset": str(_get_value(["Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...", "onset"], "Unbekannt")),
        "hearing_loss_duration": 10.0,
        "hearing_loss_cause": str(_get_value(["Diagnose.Höranamnese.Ursache....Ursache...", "cause"], "Unbekannt")),
        "tinnitus": _bool_to_ja_nein(_get_value(["Symptome präoperativ.Tinnitus...", "tinnitus"], False)),
        "vertigo": _bool_to_ja_nein(_get_value(["Symptome präoperativ.Schwindel...", "schwindel"], False)),
        "implant_type": str(_get_value(["Behandlung/OP.CI Implantation", "implant_details", "implant_type"], "unknown")),
        "include_plot": False,
    }

    try:
        req = ShapVisualizationRequest(**req_data)
    except Exception:
        req = ShapVisualizationRequest.model_validate(req_data) if hasattr(ShapVisualizationRequest, 'model_validate') else ShapVisualizationRequest(**req_data)

    # Delegate to existing explainer handler (async)
    return await explainer_route.get_shap_explanation(req)


@router.get("/{patient_id}/validate")
def validate_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    """Validate stored patient `input_features` against expected model inputs.

    Returns a JSON object with `ok: bool` and `missing_features: list`.
    """
    try:
        p = crud.get_patient(session=session, patient_id=patient_id)
        if not p:
            raise HTTPException(status_code=404, detail="Patient not found")

        input_features = p.input_features or {}
        
        # Check for essential features that the preprocessor needs
        essential_keys = [
            "Alter [J]", "alter", "age",
            "Geschlecht", "geschlecht", "gender",
        ]
        
        has_age = any(k in input_features for k in ["Alter [J]", "alter", "age"])
        has_gender = any(k in input_features for k in ["Geschlecht", "geschlecht", "gender"])
        
        missing = []
        if not has_age:
            missing.append("Alter [J] (age)")
        if not has_gender:
            missing.append("Geschlecht (gender)")
        
        return {"ok": len(missing) == 0, "missing_features": missing, "features_count": len(input_features)}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in validate_patient_api for %s", patient_id)
        raise HTTPException(status_code=500, detail=str(e))
