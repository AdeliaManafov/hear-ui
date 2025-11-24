from io import BytesIO
import re

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session

from app import crud
from app.api.deps import get_db
from app.api.routes.predict import compute_prediction_and_explanation, model_wrapper
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

# Mapping from normalized tokens to the German pipeline column names the model expects.
# These are used for batch uploads so the DataFrame columns match the trained pipeline.
PIPELINE_GERMAN_NAMES = {
    "alter": "Alter [J]",
    "age": "Alter [J]",
    "geschlecht": "Geschlecht",
    "primäre sprache": "Primäre Sprache",
    "primaere sprache": "Primäre Sprache",
    "tinnitus": "Symptome präoperativ.Tinnitus...",
    "beginn der hörminderung": "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...",
    "ursache": "Diagnose.Höranamnese.Ursache....Ursache...",
    "behandlung/op.ci implantation": "Behandlung/OP.CI Implantation",
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
    # remove BOM and invisible unicode BOM char if present, then normalize
    if h is None:
        return ""
    s = str(h)
    # common BOM character \ufeff
    s = s.lstrip("\ufeff")
    return s.strip().lower()


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

    # normalize headers and rename to the German pipeline column names where possible
    mapping = {}
    for col in df.columns:
        nk = _normalize_header(col)
        # try cleaned token
        if nk in PIPELINE_GERMAN_NAMES:
            mapping[col] = PIPELINE_GERMAN_NAMES[nk]
            continue
        # try splitting sections and matching last segment
        short = nk.split('.')[-1] if '.' in nk else nk
        short = short.replace('...', '')
        clean = re.sub(r"\[.*?\]", "", short)
        clean = re.sub(r"[\(\)\./\\:,]", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        if clean in PIPELINE_GERMAN_NAMES:
            mapping[col] = PIPELINE_GERMAN_NAMES[clean]
            continue

    if mapping:
        df = df.rename(columns=mapping)

    results = []
    NUMERIC_FIELDS = {"age", "measure_preop", "days_between", "obj_ll", "obj_4000hz"}
    BOOL_LIKE = {"tinnitus", "dizziness", "otorrhea", "headache", "german_barrier", "non_verbal"}
    INTERVAL_FIELDS = {"onset_interval", "duration_interval"}

    # If model exposes exact feature names, use them to build a DataFrame
    # matching the trained pipeline (avoids ColumnTransformer missing-columns).
    fnames = None
    try:
        fnames = getattr(model_wrapper.model, "feature_names_in_", None)
    except Exception:
        fnames = None

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

        # If the model exposes feature names, construct a DataFrame with
        # those exact columns and pass it directly to the model wrapper.
        if fnames is not None:
            # Build a pipeline-row that contains every required feature name.
            pipeline_row = {}
            for fname in fnames:
                low = fname.lower()

                # Prefer canonical patient keys we already normalized
                # common heuristics (age, hearing duration, implant, gender, language)
                val = None
                if "alter" in low or "age" in low:
                    val = patient.get("age") or patient.get("Alter [J]") or patient.get("alter")
                elif "höranamnese" in low or "beginn" in low or "dauer" in low or "hearing" in low:
                    val = patient.get("hearing_loss_duration") or patient.get("duration_interval")
                elif "implant" in low or "ci implantation" in low or "behandlung" in low:
                    val = patient.get("implant_type") or patient.get("implant_details") or patient.get("implant_type")
                elif "geschlecht" in low or "gender" in low:
                    val = patient.get("geschlecht") or patient.get("Geschlecht") or patient.get("gender")
                elif "sprache" in low:
                    val = patient.get("primary_language") or patient.get("primaere_sprache") or patient.get("Primäre Sprache")
                elif "tinnitus" in low:
                    val = patient.get("tinnitus")
                elif "ursache" in low or "cause" in low:
                    val = patient.get("cause") or patient.get("diagnose_ursache")
                # fallback: try direct lookup using the possibly-renamed df column
                if val is None:
                    # try patient dict entries using exact fname or lowered forms
                    val = patient.get(fname)
                if val is None:
                    # try normalized key presence
                    val = patient.get(low) or patient.get(re.sub(r"\s+", " ", low))

                pipeline_row[fname] = val

            # Create DataFrame matching pipeline columns and pass to model
            import pandas as _pd

            model_df = _pd.DataFrame([pipeline_row])
            try:
                pred_res = model_wrapper.predict(model_df)
                try:
                    prediction_value = float(pred_res[0])
                except Exception:
                    prediction_value = float(pred_res)
                res = {"prediction": prediction_value, "explanation": {}}
            except Exception as e:
                # Bubble up as compute_prediction would -- keep consistent error handling
                raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
        else:
            # Model doesn't expose feature names; rely on existing helper which
            # accepts canonical keys (age, hearing_loss_duration, implant_type)
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
