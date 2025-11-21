from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session

from app import crud
from app.api.deps import get_db
from app.api.routes.predict import compute_prediction_and_explanation
from app.models.prediction import PredictionCreate

router = APIRouter(prefix="/predict", tags=["prediction"])

# Basic CSV -> internal column mapping. Extend as needed.
COLUMN_MAPPING = {
    "alter": "age",
    "age": "age",
    "geschlecht": "gender",
    "seiten": "implant_side",
    "primäre sprache": "primary_language",
    "weitere sprachen": "secondary_language",
    "deutsch sprachbarriere": "german_barrier",
    "non-verbal": "non_verbal",
    "eltern m. schwerhörigkeit": "parents_hearing_loss",
    "geschwister m. sh": "siblings_hearing_loss",
    "tinnitus": "tinnitus",
    "schwindel": "dizziness",
    "otorrhoe": "otorrhea",
    "kopfschmerzen": "headache",
    "geschmack": "taste",
    "bildgebung, präoperativ.typ": "imaging_type",
    "bildgebung, präoperativ.befunde": "imaging_findings",
    "objektive messungen.oae (teoae/dpoae)": "oae",
    "objektive messungen.ll": "obj_ll",
    "objektive messungen.4000 hz": "obj_4000hz",
    "hörminderung operiertes ohr": "hearing_loss_op",
    "versorgung operiertes ohr": "care_op_ear",
    "zeitpunkt des hörverlusts (op_ohr)": "time_of_loss",
    "erwerbsart": "acquisition_type",
    "beginn der hörminderung (op-ohr)": "onset_interval",
    "hochgradige hörminderung oder taubheit (op-ohr)": "duration_interval",
    "ursache": "cause",
    "art der hörstörung": "disorder_type",
    "hörminderung gegenohr": "hearing_loss_other_ear",
    "versorgung gegenohr": "care_other_ear",
    "behandlung/op.ci implantation": "implant_details",
    "measure  pre-op": "measure_preop",
    "abstand": "days_between",
}


def _to_bool(val: object) -> bool | None:
    """Best-effort boolean parser for German/English values."""
    if val is None:
        return None
    s = str(val).strip().lower()
    if s in ("", "nan", "none"):
        return None
    true_vals = {"ja", "yes", "vorhanden", "true", "1", "y"}
    false_vals = {"nein", "no", "kein", "none", "false", "0", "n"}
    if s in true_vals:
        return True
    if s in false_vals:
        return False
    return None


def _parse_interval_to_years(val: object) -> float | None:
    """Map interval labels like '< 1 y', '1-2 y', '2-5 y' to approximate years."""
    if val is None:
        return None
    s = str(val).strip().lower()
    if s in ("nan", "", "nicht erhoben", "unbekannt", "unbekannt/ka"):
        return None
    mapping = {
        "< 1 y": 0.5,
        "1-2 y": 1.5,
        "2-5 y": 3.5,
        "5-10 y": 7.5,
        "10-20 y": 15.0,
        "> 20 y": 25.0,
    }
    if s in mapping:
        return mapping[s]
    # try to parse a number
    try:
        return float(s)
    except Exception:
        return None


def _normalize_header(h: str) -> str:
    return str(h).strip().lower()


@router.post("/upload", summary="Upload CSV and run batch predictions")
async def upload_csv_and_predict(
    session: Session = Depends(get_db),
    file: UploadFile = File(...),
    persist: bool = Query(False, description="Persist predictions to DB"),
):
    """Read uploaded CSV, map columns, run predictions row-by-row and optionally persist them.

    This is intentionally simple for the MVP. It reads into pandas, renames headers
    according to `COLUMN_MAPPING` (case-insensitive) and then for each row calls
    `compute_prediction_and_explanation` (existing function).
    """
    # read CSV into DataFrame
    try:
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {exc}")

    # normalize headers and rename
    mapping = {col: COLUMN_MAPPING[_normalize_header(col)] for col in df.columns if _normalize_header(col) in COLUMN_MAPPING}
    df = df.rename(columns=mapping)

    results = []
    NUMERIC_FIELDS = {"age", "measure_preop", "days_between", "obj_ll", "obj_4000hz"}
    BOOL_LIKE = {"tinnitus", "dizziness", "otorrhea", "headache", "german_barrier", "non_verbal"}
    INTERVAL_FIELDS = {"onset_interval", "duration_interval"}

    for idx, row in df.iterrows():
        # Build patient dict with a best-effort mapping. Only include known keys.
        patient = {}
        for col in df.columns:
            val = row.get(col)
            if pd.isna(val):
                continue
            # Numeric fields
            if col in NUMERIC_FIELDS:
                try:
                    patient[col] = float(val)
                except Exception:
                    continue
            # Interval-like fields -> approximate years
            elif col in INTERVAL_FIELDS:
                parsed = _parse_interval_to_years(val)
                if parsed is not None:
                    patient[col] = parsed
            # Boolean-like fields
            elif col in BOOL_LIKE:
                b = _to_bool(val)
                if b is not None:
                    patient[col] = b
            # Common well-known keys
            elif col == "age":
                try:
                    patient["age"] = int(val)
                except Exception:
                    patient["age"] = None
            elif col == "implant_type":
                patient["implant_type"] = str(val)
            else:
                # keep as string for nominal/categorical fields
                patient[col] = str(val)

        # Normalize keys expected by compute_prediction_and_explanation
        # Map any uploaded column that was renamed to a compute-friendly key
        # compute_prediction_and_explanation expects: age, hearing_loss_duration, implant_type
        if "age" not in patient:
            patient.setdefault("age", 50)
        if "hearing_loss_duration" not in patient:
            # If we have an interval field for duration, prefer it
            patient.setdefault("hearing_loss_duration", patient.get("duration_interval", 10.0))
        if "implant_type" not in patient:
            patient.setdefault("implant_type", "type_a")

        res = compute_prediction_and_explanation(patient)

        if persist:
            try:
                pred_in = PredictionCreate(
                    input_features=patient,
                    prediction=float(res.get("prediction", 0.0)),
                    explanation=res.get("explanation", {}),
                )
                crud.create_prediction(session=session, prediction_in=pred_in)
            except Exception:
                # don't fail whole batch for single-row DB errors
                pass

        results.append({"row": int(idx), "prediction": res.get("prediction"), "explanation": res.get("explanation")})

    return {"count": len(results), "results": results}
