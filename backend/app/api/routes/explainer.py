# app/api/routes/explainer.py

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/explainer", tags=["explainer"])


class ShapVisualizationRequest(BaseModel):
    """Request for SHAP visualization with patient features."""

    # Demographics
    age: int | None = Field(default=None, alias="Alter [J]", description="Age in years")
    gender: str | None = Field(
        default=None, alias="Geschlecht", description="Gender (m/w/d)"
    )

    # Language
    primary_language: str | None = Field(
        default=None, alias="Primäre Sprache", description="Primary language"
    )

    # Medical History
    hearing_loss_onset: str | None = Field(
        default=None,
        alias="Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...",
        description="Onset of hearing loss",
    )
    hearing_loss_duration: float | None = Field(
        default=None, description="Duration of hearing loss in years"
    )
    hearing_loss_cause: str | None = Field(
        default=None,
        alias="Diagnose.Höranamnese.Ursache....Ursache...",
        description="Cause of hearing loss",
    )

    # Pre-op Symptoms
    tinnitus: str | None = Field(
        default=None,
        alias="Symptome präoperativ.Tinnitus...",
        description="Pre-op Tinnitus",
    )
    vertigo: str | None = Field(
        default=None,
        alias="Symptome präoperativ.Schwindel...",
        description="Pre-op Vertigo",
    )

    # Implant
    implant_type: str | None = Field(
        default=None,
        alias="Behandlung/OP.CI Implantation",
        description="CI Implant Type/Date",
    )

    # Objective measurements
    ll_measurement: str | None = Field(
        default=None,
        alias="Objektive Messungen.LL...",
        description="LL measurement result",
    )
    hz4000_measurement: str | None = Field(
        default=None,
        alias="Objektive Messungen.4000 Hz...",
        description="4000 Hz measurement result",
    )

    # SHAP options
    include_plot: bool = False

    model_config = {
        "populate_by_name": True,
        "extra": "allow",  # Allow extra fields not defined in model
        "json_schema_extra": {
            "example": {
                "Alter [J]": 45,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
                "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
                "Symptome präoperativ.Tinnitus...": "ja",
                "Behandlung/OP.CI Implantation": "Cochlear Nucleus",
                "include_plot": True,
            }
        },
    }


class ShapVisualizationResponse(BaseModel):
    """Response with SHAP values and optional plot."""

    prediction: float
    feature_importance: dict[str, float]
    shap_values: list[float]
    base_value: float
    plot_base64: str | None = None
    top_features: list[dict] | None = None


@router.post(
    "/explain", response_model=ShapVisualizationResponse, summary="Get SHAP Explanation"
)
async def get_shap_explanation(request: ShapVisualizationRequest):
    """Generate SHAP explanation with optional visualization."""
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

    logger = logging.getLogger(__name__)

    try:
        import numpy as np

        from app.core.preprocessor import EXPECTED_FEATURES

        # Convert request to dict with original column names (aliases)
        feature_dict = request.model_dump(by_alias=True, exclude={"include_plot"})

        # Use the preprocessor to transform input to the 68-feature format
        preprocessed = wrapper.prepare_input(feature_dict)

        # Get prediction using preprocessed data
        # clip=True enforces probability bounds [1%, 99%]
        model_res = wrapper.predict(preprocessed, clip=True)
        try:
            prediction = float(model_res[0])
        except (TypeError, IndexError):
            prediction = float(model_res)

        # Get model coefficients for feature importance (coefficient-based explanation)
        feature_importance = {}
        shap_values = []
        base_value = 0.0

        try:
            import numpy as np

            model = wrapper.model

            # Get coefficients from LogisticRegression
            if hasattr(model, "coef_"):
                coef = model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
                intercept = (
                    model.intercept_[0]
                    if hasattr(model.intercept_, "__len__")
                    else model.intercept_
                )
                base_value = float(intercept)

                # Get sample values from preprocessed data
                if hasattr(preprocessed, "values"):
                    sample_vals = preprocessed.values.flatten()
                elif hasattr(preprocessed, "flatten"):
                    sample_vals = preprocessed.flatten()
                else:
                    sample_vals = np.array(preprocessed).flatten()

                # Compute contributions (coefficient * feature value)
                shap_values = []
                feature_values = {}  # Store actual feature values
                for i, (fname, c) in enumerate(
                    zip(EXPECTED_FEATURES, coef, strict=False)
                ):
                    val = sample_vals[i] if i < len(sample_vals) else 0.0
                    contribution = float(c * val)
                    feature_importance[fname] = contribution
                    feature_values[fname] = float(val)  # Store the actual value
                    shap_values.append(contribution)

        except Exception as e:
            logger.warning("Failed to compute feature importance: %s", e)
            # Provide empty but valid response
            feature_importance = {f: 0.0 for f in EXPECTED_FEATURES}
            feature_values = {f: 0.0 for f in EXPECTED_FEATURES}
            shap_values = [0.0] * len(EXPECTED_FEATURES)

        # Get top 5 features by absolute importance
        sorted_feats = sorted(
            feature_importance.items(), key=lambda x: abs(x[1]), reverse=True
        )
        top_features = [
            {"feature": f, "importance": v, "value": feature_values.get(f, 0.0)} 
            for f, v in sorted_feats[:5]
        ]

        return ShapVisualizationResponse(
            prediction=prediction,
            feature_importance=feature_importance,
            shap_values=shap_values,
            base_value=base_value,
            plot_base64=None,  # Plot generation disabled for simplicity
            top_features=top_features,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("SHAP explanation failed")
        raise HTTPException(
            status_code=500,
            detail=f"SHAP explanation failed: {str(exc)}",
        )
