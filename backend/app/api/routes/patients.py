import logging
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel import Session

from app import crud
from app.api.deps import get_db
from app.models import Patient, PatientCreate, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])

logger = logging.getLogger(__name__)


class PaginatedPatientsResponse(BaseModel):
    """Paginated response for patient list."""

    items: list[Patient]
    total: int
    limit: int
    offset: int
    has_more: bool


@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient_api(
    patient_in: PatientCreate = Body(
        ...,
        example={
            "input_features": {
                "Alter [J]": 45,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
            },
            "display_name": "Muster, Anna",
        },
    ),
    session: Session = Depends(get_db),
):
    """Create a new patient record via JSON (no CSV upload).

    Args:
        patient_in: PatientCreate object with input_features dict and optional display_name
        session: Database session

    Returns:
        Created Patient object with id and created_at

    Example:
        POST /api/v1/patients/
        {
          "input_features": {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch"
          },
          "display_name": "Muster, Anna"
        }
    """
    try:
        # Validate that input_features is provided
        if not patient_in.input_features:
            raise HTTPException(
                status_code=400, detail="input_features is required and cannot be empty"
            )

        # Create patient in database
        patient = crud.create_patient(session=session, patient_in=patient_in)
        return patient

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to create patient")
        raise HTTPException(
            status_code=500, detail=f"Failed to create patient: {str(e)}"
        )


@router.get("/")
def list_patients_api(
    session: Session = Depends(get_db),
    limit: int = Query(
        default=100, ge=1, le=1000, description="Maximum number of patients to return"
    ),
    offset: int = Query(default=0, ge=0, description="Number of patients to skip"),
    paginated: bool = Query(
        default=False, description="Return paginated response with metadata"
    ),
):
    """List patients with optional pagination.

    Args:
        limit: Maximum number of patients (1-1000, default 100)
        offset: Number of patients to skip (default 0)
        paginated: If True, returns {items, total, limit, offset, has_more}
                   If False (default), returns just the list for backward compatibility
    """
    patients = crud.list_patients(session=session, limit=limit, offset=offset)

    if paginated:
        total = crud.count_patients(session=session)
        return PaginatedPatientsResponse(
            items=patients,
            total=total,
            limit=limit,
            offset=offset,
            has_more=(offset + len(patients)) < total,
        )

    # Backward compatible: return just the list
    return patients


@router.get("/search")
def search_patients_api(
    q: str = Query(..., min_length=1, description="Search query for patient name"),
    session: Session = Depends(get_db),
    limit: int = Query(
        default=1000, ge=1, le=5000, description="Maximum number of patients to scan"
    ),
    offset: int = Query(
        default=0, ge=0, description="Offset when listing patients to scan"
    ),
):
    """Search patients by name-like fields inside stored `input_features`.

    This performs a simple substring, case-insensitive match against common
    name-like keys found in the `input_features` JSON blob (e.g. `Name`,
    `Vorname`, `Nachname`, `full_name`). The implementation is intentionally
    conservative and runs in Python by fetching a page of patients and
    inspecting their `input_features`. For very large datasets a dedicated
    DB-side JSON query should be implemented.
    """
    # keys that may contain a person's name inside the `input_features` JSON
    name_keys = ["name", "Name", "Vorname", "Nachname", "full_name", "fullname"]

    q_lower = q.lower()

    patients = crud.list_patients(session=session, limit=limit, offset=offset)
    # Prefer DB-side search if available (faster for production with Postgres)
    results: list[dict] = []
    try:
        db_results = crud.search_patients_by_name(
            session=session, q=q, limit=limit, offset=offset
        )
        for p in db_results:
            results.append(
                {"id": str(p.id), "name": getattr(p, "display_name", None) or ""}
            )
        return results
    except Exception:
        # If DB-side search is not available or fails (e.g., SQLite/dev),
        # fall back to the conservative Python scanning approach below.
        pass

    for p in patients:
        if not getattr(p, "input_features", None):
            continue
        input_features = p.input_features or {}
        candidate = None
        for k in name_keys:
            v = input_features.get(k)
            if v:
                candidate = str(v)
                break
        # Some datasets might store a single combined `name` under other keys
        # so as a fallback, join string values from input_features and search
        if not candidate:
            # try to find any string-like value that looks like a name
            for val in input_features.values():
                if isinstance(val, str) and len(val) > 0:
                    # take the first string-ish value as a fallback candidate
                    candidate = val
                    break

        if candidate and q_lower in candidate.lower():
            results.append({"id": str(p.id), "name": candidate})

    return results


@router.get("/{patient_id}", response_model=Patient)
def get_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    p = crud.get_patient(session=session, patient_id=patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p


@router.put("/{patient_id}", response_model=Patient)
def update_patient_api(
    patient_id: UUID,
    patient_update: PatientUpdate = Body(
        ...,
        example={
            "input_features": {
                "Alter [J]": 50,
                "Geschlecht": "m",
                "Primäre Sprache": "Deutsch",
            },
            "display_name": "Mustermann, Max",
        },
    ),
    session: Session = Depends(get_db),
):
    """Update an existing patient's data.

    Args:
        patient_id: UUID of the patient to update
        patient_update: PatientUpdate object with fields to update (all optional)
        session: Database session

    Returns:
        Updated Patient object

    Example:
        PUT /api/v1/patients/{patient_id}
        {
          "input_features": {
            "Alter [J]": 50,
            "Geschlecht": "m"
          },
          "display_name": "Mustermann, Max"
        }
    """
    try:
        # Only include fields that were actually provided (not None)
        update_data = patient_update.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        updated_patient = crud.update_patient(
            session=session, patient_id=patient_id, patient_update=update_data
        )

        if not updated_patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        return updated_patient

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to update patient %s", patient_id)
        raise HTTPException(
            status_code=500, detail=f"Failed to update patient: {str(e)}"
        )


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_api(patient_id: UUID, session: Session = Depends(get_db)):
    """Delete a patient from the database.

    Args:
        patient_id: UUID of the patient to delete
        session: Database session

    Returns:
        204 No Content on success

    Example:
        DELETE /api/v1/patients/{patient_id}
    """
    try:
        deleted = crud.delete_patient(session=session, patient_id=patient_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Return 204 No Content (FastAPI handles this automatically)
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to delete patient %s", patient_id)
        raise HTTPException(
            status_code=500, detail=f"Failed to delete patient: {str(e)}"
        )


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
            # Use clip=True to enforce probability bounds [1%, 99%]
            model_res = wrapper.predict(input_features, clip=True)
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

    # Use the SAME input_features that the /predict endpoint uses
    # This ensures consistent preprocessing and model predictions
    try:
        from app.main import app as fastapi_app

        wrapper = getattr(fastapi_app.state, "model_wrapper", None)
    except Exception:
        wrapper = None

    if not wrapper or not wrapper.is_loaded():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. SHAP explanations require a loaded model.",
        )

    try:
        import numpy as np

        from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF

        # Use wrapper.predict() with clip=True to ensure consistent behavior
        # with /predict/simple endpoint (clips to [1%, 99%])
        model_res = wrapper.predict(input_features, clip=True)

        try:
            prediction = float(model_res[0])
        except (TypeError, IndexError):
            prediction = float(model_res)

        # Now prepare preprocessed data separately for feature importance calculation
        preprocessed = wrapper.prepare_input(input_features)

        # Get SHAP-based feature importance (shows both positive AND negative contributions)
        feature_importance = {}
        feature_values = {}
        shap_values = []
        base_value = 0.0

        try:
            from app.core.shap_explainer import ShapExplainer

            model = wrapper.model

            # Get sample values from preprocessed data
            if hasattr(preprocessed, "values"):
                sample_vals = preprocessed.values.flatten()
            elif hasattr(preprocessed, "flatten"):
                sample_vals = preprocessed.flatten()
            else:
                sample_vals = np.array(preprocessed).flatten()

            # Use SHAP TreeExplainer for Random Forest (provides both positive and negative contributions)
            if hasattr(model, "feature_importances_"):
                try:
                    logger.info("Attempting SHAP TreeExplainer for patient %s", patient_id)
                    # Initialize SHAP explainer
                    shap_explainer = ShapExplainer(
                        model=model,
                        feature_names=EXPECTED_FEATURES_RF,
                        use_transformed=True,
                    )

                    # Compute SHAP values
                    explanation_result = shap_explainer.explain(
                        preprocessed, return_plot=False
                    )

                    feature_importance = explanation_result.get(
                        "feature_importance", {}
                    )
                    shap_values = explanation_result.get("shap_values", [])
                    base_value = explanation_result.get("base_value", 0.0)

                    # Store actual feature values
                    feature_values = {}
                    for i, fname in enumerate(EXPECTED_FEATURES_RF):
                        val = sample_vals[i] if i < len(sample_vals) else 0.0
                        feature_values[fname] = float(val)

                    logger.info(
                        "✅ SHAP SUCCESS for patient %s: %d features, positive=%d, negative=%d",
                        patient_id,
                        len(feature_importance),
                        sum(1 for v in feature_importance.values() if v > 0),
                        sum(1 for v in feature_importance.values() if v < 0),
                    )

                except Exception as shap_error:
                    logger.error(
                        "❌ SHAP explanation failed, falling back to feature_importances_: %s",
                        shap_error,
                        exc_info=True,
                    )
                    # Fallback to feature_importances_ if SHAP fails
                    importances = model.feature_importances_
                    for i, fname in enumerate(EXPECTED_FEATURES_RF):
                        val = sample_vals[i] if i < len(sample_vals) else 0.0
                        importance = (
                            float(importances[i]) if i < len(importances) else 0.0
                        )
                        contribution = importance * val
                        feature_importance[fname] = contribution
                        feature_values[fname] = float(val)
                        shap_values.append(contribution)
            else:
                # For non-tree models, use feature_importances_ fallback
                logger.info(
                    "Model does not have feature_importances_, using empty explanation"
                )
                feature_importance = dict.fromkeys(EXPECTED_FEATURES_RF, 0.0)
                feature_values = dict.fromkeys(EXPECTED_FEATURES_RF, 0.0)
                shap_values = [0.0] * len(EXPECTED_FEATURES_RF)

        except Exception as e:
            logger.warning("Failed to compute feature importance: %s", e)
            # Provide empty but valid response
            feature_importance = dict.fromkeys(EXPECTED_FEATURES_RF, 0.0)
            feature_values = dict.fromkeys(EXPECTED_FEATURES_RF, 0.0)
            shap_values = [0.0] * len(EXPECTED_FEATURES_RF)

        # Get top 5 features by absolute importance
        sorted_feats = sorted(
            feature_importance.items(), key=lambda x: abs(x[1]), reverse=True
        )
        top_features = [
            {"feature": f, "importance": v, "value": feature_values.get(f, 0.0)}
            for f, v in sorted_feats[:5]
        ]

        from app.api.routes.explainer import ShapVisualizationResponse

        return ShapVisualizationResponse(
            prediction=prediction,
            feature_importance=feature_importance,
            feature_values=feature_values,
            shap_values=shap_values,
            base_value=base_value,
            plot_base64=None,
            top_features=top_features,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("SHAP explanation failed for patient %s", patient_id)
        raise HTTPException(status_code=500, detail=f"SHAP explanation failed: {exc}")


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
        has_age = any(k in input_features for k in ["Alter [J]", "alter", "age"])
        has_gender = any(
            k in input_features for k in ["Geschlecht", "geschlecht", "gender"]
        )

        missing = []
        if not has_age:
            missing.append("Alter [J] (age)")
        if not has_gender:
            missing.append("Geschlecht (gender)")

        return {
            "ok": len(missing) == 0,
            "missing_features": missing,
            "features_count": len(input_features),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in validate_patient_api for %s", patient_id)
        raise HTTPException(status_code=500, detail=str(e))
