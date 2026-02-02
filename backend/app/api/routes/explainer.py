# app/api/routes/explainer.py

import logging

from fastapi import APIRouter, HTTPException, Query
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


@router.get("/methods", summary="List Available XAI Methods")
async def list_explainer_methods():
    """List all available explainer methods.

    Returns:
        List of available XAI method names and their descriptions
    """
    from app.core.explainer_registry import get_available_explainers

    methods = get_available_explainers()

    # Add descriptions
    descriptions = {
        "shap": "SHAP (SHapley Additive exPlanations) - Model-agnostic explanations",
        "coefficient": "Coefficient-based - Fast explanations for linear models",
        "coef": "Alias for 'coefficient'",
        "linear": "Alias for 'coefficient'",
        "lime": "LIME (Local Interpretable Model-agnostic Explanations) - Requires lime package",
    }

    return {
        "methods": [
            {"name": method, "description": descriptions.get(method, "No description available")}
            for method in methods
        ]
    }


@router.post(
    "/explain", response_model=ShapVisualizationResponse, summary="Get SHAP Explanation"
)
@router.post(
    "/shap",
    response_model=ShapVisualizationResponse,
    summary="Get SHAP Explanation (Alias)",
    include_in_schema=False,  # Hidden alias for backward compatibility
)
async def get_shap_explanation(
    request: ShapVisualizationRequest,
    method: str = Query(
        default="shap",
        description="XAI method to use (shap, coefficient, lime)",
    ),
):
    """Generate explanation with configurable XAI method.

    Supports multiple explanation methods:
    - shap: SHAP-based explanations (default)
    - coefficient: Fast coefficient-based explanations for linear models
    - lime: LIME explanations (requires lime package)
    """
    try:
        from app.main import app as fastapi_app

        wrapper = getattr(fastapi_app.state, "model_wrapper", None)
    except Exception:
        wrapper = None

    if not wrapper or not wrapper.is_loaded():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Explanations require a loaded model.",
        )

    logger = logging.getLogger(__name__)

    try:

        from app.core.explainer_registry import create_explainer

        # Convert request to dict with original column names (aliases)
        feature_dict = request.model_dump(by_alias=True, exclude={"include_plot"})

        # Use the preprocessor to transform input to the feature format
        preprocessed = wrapper.prepare_input(feature_dict)

        # Get prediction using preprocessed data
        # clip=True enforces probability bounds [1%, 99%]
        model_res = wrapper.predict(preprocessed, clip=True)
        try:
            float(model_res[0])
        except (TypeError, IndexError):
            float(model_res)

        # Create explainer using factory
        try:
            explainer = create_explainer(
                method=method,
                model=wrapper.model,
                feature_names=wrapper.get_feature_names(),
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Generate explanation
        explanation = explainer.explain(
            model=wrapper.model,
            input_data=preprocessed,
            feature_names=wrapper.get_feature_names(),
            include_plot=request.include_plot,
        )

        # Convert to response format
        # Sort features by absolute importance
        sorted_features = sorted(
            explanation.feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        top_features = [
            {"name": name, "importance": float(importance)}
            for name, importance in sorted_features[:10]
        ]

        # Get SHAP values as list (for backward compatibility)
        shap_values = [
            explanation.feature_importance.get(name, 0.0)
            for name in wrapper.get_feature_names()
        ]

        # Get plot if available
        plot_base64 = None
        if request.include_plot and explainer.supports_visualization():
            plot_base64 = explainer.generate_visualization(explanation)
        elif explanation.metadata and "plot_base64" in explanation.metadata:
            plot_base64 = explanation.metadata.get("plot_base64")

        return ShapVisualizationResponse(
            prediction=explanation.prediction,
            feature_importance=explanation.feature_importance,
            shap_values=shap_values,
            base_value=explanation.base_value,
            plot_base64=plot_base64,
            top_features=top_features,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Explanation generation failed")
        raise HTTPException(
            status_code=500,
            detail=f"Explanation failed: {str(exc)}",
        )

