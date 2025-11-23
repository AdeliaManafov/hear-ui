# app/api/routes/shap.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.patient import PatientBase

router = APIRouter(prefix="/shap", tags=["shap"])


class ShapVisualizationRequest(PatientBase):
    """Request for SHAP visualization."""
    include_plot: bool = True


class ShapVisualizationResponse(BaseModel):
    """Response with SHAP values and optional plot."""
    prediction: float
    feature_importance: dict[str, float]
    shap_values: list[float]
    base_value: float
    plot_base64: str | None = None
    top_features: list[dict] | None = None


@router.post("/explain", response_model=ShapVisualizationResponse, summary="Get SHAP Explanation")
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

    try:
        import pandas as pd
        from app.core.shap_explainer import ShapExplainer
        
        # Convert request to dict with original column names (aliases)
        feature_dict = request.dict(by_alias=True, exclude={"include_plot"})
        
        # Get prediction
        model_res = wrapper.predict(feature_dict)
        prediction = float(model_res.get("prediction", 0.0))
        
        # Initialize SHAP explainer
        feature_names = list(feature_dict.keys())
        
        # Create background data for KernelExplainer
        background_df = pd.DataFrame([{
            "Alter [J]": 50,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
            "Symptome präoperativ.Tinnitus...": "nein",
            "Behandlung/OP.CI Implantation": "Cochlear"
        }])
        # Ensure background has same columns as input
        for col in feature_names:
            if col not in background_df.columns:
                background_df[col] = 0
        
        # Reorder to match input
        background_df = background_df[feature_names]

        shap_explainer = ShapExplainer(
            model=wrapper.model,
            feature_names=feature_names,
            background_data=background_df.values,
        )
        
        # Create DataFrame for SHAP
        features_df = pd.DataFrame([feature_dict])
        
        # Get SHAP explanation
        shap_result = shap_explainer.explain(
            features_df,
            return_plot=request.include_plot,
        )
        
        # Get top features
        top_features = shap_explainer.get_top_features(features_df, top_k=5)
        
        return ShapVisualizationResponse(
            prediction=prediction,
            feature_importance=shap_result.get("feature_importance", {}),
            shap_values=shap_result.get("shap_values", []),
            base_value=shap_result.get("base_value", 0.0),
            plot_base64=shap_result.get("plot_base64"),
            top_features=top_features,
        )
        
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"SHAP explanation failed: {str(exc)}",
        )
