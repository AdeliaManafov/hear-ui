from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import logging

from app.api.deps import get_db
from app import crud
from app.models import Patient, PatientCreate
from app.api.routes.predict import compute_prediction_and_explanation
from app.api.routes import shap as shap_route
from app.api.routes.shap import ShapVisualizationRequest

# Helpers to normalize stored CSV headers to model-friendly keys
from app.api.routes.predict_batch import (
    COLUMN_MAPPING,
    _normalize_header,
    _to_bool,
    _parse_interval_to_years,
)
import re


def _normalize_input_features_for_model(input_features: dict) -> dict:
    """Normalize stored `input_features` (from CSV import) into the canonical
    keys expected by the prediction pipeline (e.g. `age`, `gender`,
    `implant_type`, `hearing_loss_duration`, `primary_language`, ...).

    This mirrors the logic used in `predict_batch.upload_csv_and_predict` so
    values persisted from the CSV import will be transformed into the shape
    the `ModelWrapper` preprocessors expect.
    """
    if not input_features:
        return {}

    patient = {}

    NUMERIC_FIELDS = {"age", "measure_preop", "days_between", "obj_ll", "obj_4000hz"}
    BOOL_LIKE = {"tinnitus", "dizziness", "otorrhea", "headache", "german_barrier", "non_verbal"}
    INTERVAL_FIELDS = {"onset_interval", "duration_interval"}

    for k, v in input_features.items():
        if v is None:
            continue
        # Normalize header and map
        nk = _normalize_header(k)

        # Try to reduce verbose section prefixes (e.g. 'diagnose.höranamnese.')
        short = nk.split('.')[-1] if '.' in nk else nk
        # strip trailing ellipses and bracketed units, remove punctuation and collapse
        short = short.replace('...', '')
        clean = re.sub(r"\[.*?\]", "", short)
        clean = re.sub(r"[\(\)\./\\:,]", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()

        # Lookup in COLUMN_MAPPING using multiple fallbacks
        mapped = COLUMN_MAPPING.get(clean)
        if not mapped:
            mapped = COLUMN_MAPPING.get(nk)
        if not mapped:
            # fallback: try substring matching against mapping keys
            for mk, mv in COLUMN_MAPPING.items():
                if mk in nk or mk in clean:
                    mapped = mv
                    break
        if not mapped:
            mapped = k

        # Skip empty strings
        if isinstance(v, str) and v.strip() == "":
            continue

        # Numbers
        try:
            fv = float(v)
            if mapped in NUMERIC_FIELDS or mapped == "age":
                patient["age" if mapped == "age" else mapped] = fv
                continue
        except Exception:
            pass

        # Intervals -> years
        if mapped in INTERVAL_FIELDS:
            parsed = _parse_interval_to_years(v)
            if parsed is not None:
                # duration_interval maps to hearing_loss_duration
                if mapped == "duration_interval":
                    patient["hearing_loss_duration"] = parsed
                else:
                    patient[mapped] = parsed
                continue

        # Boolean-like
        b = _to_bool(v)
        if b is not None:
            patient[mapped] = b
            continue

        # Re-map some keys to canonical names expected by the model
        if mapped == "implant_details":
            patient["implant_type"] = str(v)
            continue

        if mapped == "cause":
            patient["hearing_loss_cause"] = v
            continue

        if mapped == "dizziness":
            # model/pydantic expects 'vertigo' field name
            patient["vertigo"] = v
            continue

        # Accept common names directly
        if mapped in ("age", "gender", "primary_language", "hearing_loss_cause", "tinnitus"):
            patient[mapped] = v
            continue

        # If original key looks like German alias (contains non-ascii or brackets), keep as-is
        patient[mapped] = v

    # Ensure required fallbacks
    patient.setdefault("age", 50)
    patient.setdefault("hearing_loss_duration", patient.get("duration_interval", 10.0))
    patient.setdefault("implant_type", patient.get("implant_type", "unknown"))
    patient.setdefault("gender", patient.get("gender", "w"))
    patient.setdefault("primary_language", patient.get("primary_language", "Deutsch"))

    return patient


def _get_expected_feature_names_from_wrapper(wrapper) -> list[str]:
    # If the wrapper's model exposes feature names use them (transformed names),
    # otherwise fall back to a conservative set derived from the Patient Pydantic model
    fnames = None
    try:
        fnames = getattr(wrapper.model, "feature_names_in_", None)
    except Exception:
        fnames = None

    # `feature_names_in_` may be a numpy.ndarray / pandas.Index / list/tuple.
    # Avoid using its truth value (numpy raises ValueError for arrays with
    # more than one element). Instead check for None and length.
    try:
        if fnames is not None and hasattr(fnames, "__len__") and len(fnames) > 0:
            return list(fnames)
    except Exception:
        # Any unexpected issue converting to list -> ignore and fall back
        fnames = None

    # conservative expected names (raw pipeline inputs / common aliases)
    return [
        "age",
        "gender",
        "primary_language",
        "hearing_loss_onset",
        "hearing_loss_duration",
        "hearing_loss_cause",
        "implant_type",
    ]


def _get_missing_features_for_prediction(normalized: dict) -> list[str]:
    """Return list of missing features given a normalized patient dict.

    This checks the app-level model wrapper if available to determine expected
    feature names; otherwise returns a fallback list.
    """
    try:
        from app.main import app as fastapi_app
        wrapper = getattr(fastapi_app.state, "model_wrapper", None)
    except Exception:
        wrapper = None

    expected = _get_expected_feature_names_from_wrapper(wrapper) if wrapper else [
        "age",
        "gender",
        "primary_language",
        "hearing_loss_duration",
        "implant_type",
    ]

    # Helper: turn model-feature-like names into canonical keys we use in `normalized`.
    def _canonicalize_feature_name(fn: str) -> str:
        if not fn:
            return fn
        # strip common transformer prefixes like 'num__', 'cat__'
        if "__" in fn:
            fn = fn.split("__", 1)[1]
        # If it's a one-hot encoded name like 'Primäre Sprache_Deutsch', remove the category suffix
        if "_" in fn:
            parts = fn.rsplit("_", 1)
            if len(parts) == 2 and parts[1] != "":
                fn = parts[0]

        # normalize header and map using COLUMN_MAPPING if possible
        try:
            norm = _normalize_header(fn)
            # further clean: remove bracketed units, punctuation and extra whitespace
            clean = re.sub(r"\[.*?\]", "", norm)
            clean = re.sub(r"[\(\)\./\\:,]", " ", clean)
            clean = re.sub(r"\s+", " ", clean).strip()

            mapped = COLUMN_MAPPING.get(clean, None)
            if mapped:
                return mapped

            # heuristic keyword matches for common German tokens -> canonical mapping
            KEYWORD_MAP = {
                "alter": "age",
                "geschlecht": "gender",
                "primäre sprache": "primary_language",
                "primare sprache": "primary_language",
                "sprache": "primary_language",
                "tinnitus": "tinnitus",
                "beginn der hörminderung": "onset_interval",
                "ursache": "cause",
                "behandlung": "implant_details",
                "implantation": "implant_details",
                "ci implantation": "implant_details",
                "behandlung/op.ci implantation": "implant_details",
            }
            for k, v in KEYWORD_MAP.items():
                if k in clean:
                    return v

            # fallback: return cleaned token if it's already canonical (age, gender, ...)
            return clean
        except Exception:
            return fn

    missing = []
    # canonicalize expected names and deduplicate
    canonical_expected = []
    for name in expected:
        try:
            cname = _canonicalize_feature_name(name)
        except Exception:
            cname = name
        if cname not in canonical_expected:
            canonical_expected.append(cname)

    for name in canonical_expected:
        # tolerant check: treat None or empty string as missing
        present = False
        # build candidate keys to check in the normalized dict
        candidates = {name}
        # canonical alias map: expected feature names -> normalized patient keys
        EXPECTED_ALIASES = {
            "cause": "hearing_loss_cause",
            "implant_details": "implant_type",
            "hearing_loss_onset": "hearing_loss_onset",
            "hearing_loss_duration": "hearing_loss_duration",
        }
        if name in EXPECTED_ALIASES:
            candidates.add(EXPECTED_ALIASES[name])
        try:
            # original expected normalized and mapped form
            norm_name = _normalize_header(name)
            candidates.add(norm_name)
            mapped = COLUMN_MAPPING.get(norm_name)
            if mapped:
                candidates.add(mapped)
        except Exception:
            pass

        # also consider simple lowercased or stripped variants
        candidates.update({c.lower() for c in list(candidates) if isinstance(c, str)})

        for c in candidates:
            if c in normalized:
                val = normalized.get(c)
                if val is not None and not (isinstance(val, str) and val.strip() == ""):
                    present = True
                    break

        if not present:
            missing.append(name)

    return missing

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
        # Normalize stored features into the canonical shape the compute helper expects
        normalized = _normalize_input_features_for_model(input_features)

        # Check for missing features and return helpful error if any
        missing = _get_missing_features_for_prediction(normalized)
        if missing:
            raise HTTPException(status_code=400, detail={
                "error": "missing_features",
                "missing": missing,
            })

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
            model_res = wrapper.predict(normalized)
            # extract a scalar prediction from different possible return types
            if isinstance(model_res, dict):
                prediction = float(model_res.get("prediction", 0.0))
            else:
                try:
                    prediction = float(model_res[0])
                except Exception:
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


@router.get("/{patient_id}/shap")
async def shap_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    """Return SHAP explanation for a stored patient by delegating to the SHAP route.

    This constructs a `ShapVisualizationRequest` from the saved input_features
    and calls the existing SHAP handler.
    """
    p = crud.get_patient(session=session, patient_id=patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    input_features = p.input_features or {}

    # Normalize into canonical keys and build ShapVisualizationRequest
    normalized = _normalize_input_features_for_model(input_features)

    # Coerce/normalize types expected by the Pydantic model used by SHAP
    def _bool_to_ja_nein(v):
        if isinstance(v, bool):
            return "ja" if v else "nein"
        if v is None:
            return "nein"
        return str(v)

    # Robust conversions: input coming from CSV imports may contain
    # unexpected strings for numeric fields (e.g. misplaced values). Coerce
    # carefully and fall back to sensible defaults while logging warnings.
    age_val = normalized.get("age", 50)
    try:
        age = int(float(age_val))
    except Exception:
        logger.warning("Could not coerce age=%r for patient %s, defaulting to 50", age_val, patient_id)
        age = 50

    def _to_float_safe(v, default):
        try:
            return float(v)
        except Exception:
            logger.warning("Could not coerce float for value %r for patient %s, defaulting to %s", v, patient_id, default)
            return default

    req_data = {
        "age": age,
        "gender": str(normalized.get("gender", "w")),
        "primary_language": str(normalized.get("primary_language", "Deutsch")),
        "hearing_loss_onset": str(normalized.get("hearing_loss_onset", normalized.get("onset_interval", "Unbekannt"))),
        "hearing_loss_duration": _to_float_safe(normalized.get("hearing_loss_duration", 10.0), 10.0),
        "hearing_loss_cause": str(normalized.get("hearing_loss_cause", normalized.get("cause", "Unbekannt"))),
        "tinnitus": _bool_to_ja_nein(normalized.get("tinnitus", "nein")),
        "vertigo": _bool_to_ja_nein(normalized.get("vertigo", "nein")),
        "implant_type": str(normalized.get("implant_type", "unknown")),
        "include_plot": False,
    }

    try:
        req = ShapVisualizationRequest(**req_data)
    except Exception:
        # Fallback for Pydantic v2/v1 differences
        req = ShapVisualizationRequest.model_validate(req_data) if hasattr(ShapVisualizationRequest, 'model_validate') else ShapVisualizationRequest(**req_data)

    # Delegate to existing SHAP handler (async)
    return await shap_route.get_shap_explanation(req)


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
        normalized = _normalize_input_features_for_model(input_features)
        missing = _get_missing_features_for_prediction(normalized)

        return {"ok": len(missing) == 0, "missing_features": missing}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in validate_patient_api for %s", patient_id)
        raise HTTPException(status_code=500, detail=str(e))
