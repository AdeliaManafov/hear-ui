# app/api/routes/shap.py

from fastapi import APIRouter, HTTPException
import logging
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
        
        # Get prediction (ModelWrapper.predict may return array-like or numeric)
        model_res = wrapper.predict(feature_dict)
        # normalize prediction extraction
        try:
            if isinstance(model_res, dict):
                prediction = float(model_res.get("prediction", 0.0))
            else:
                # array-like or scalar
                try:
                    prediction = float(model_res[0])
                except Exception:
                    prediction = float(model_res)
        except Exception:
            prediction = 0.0
        
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
        
        # Create DataFrame for SHAP and pass numpy values to explainer
        features_df = pd.DataFrame([feature_dict])

        # Convert to numpy array for the explainer implementation
        sample_array = features_df.values

        # Get SHAP explanation (may fail for pipelines with mixed dtypes)
        try:
            shap_result = shap_explainer.explain(
                sample_array,
                return_plot=request.include_plot,
            )

            # Ensure we have a mapping result
            if not isinstance(shap_result, dict):
                shap_result = {"feature_importance": {}, "shap_values": [], "base_value": 0.0}

            # Get top features (pass numpy array to the explainer helper)
            top_features = shap_explainer.get_top_features(sample_array, top_k=5)

            return ShapVisualizationResponse(
                prediction=prediction,
                feature_importance=shap_result.get("feature_importance", {}),
                shap_values=shap_result.get("shap_values", []),
                base_value=shap_result.get("base_value", 0.0),
                plot_base64=shap_result.get("plot_base64"),
                top_features=top_features,
            )

        except Exception as shap_exc:
            # Fallback: compute a simple feature-importance map from model internals
            logger = logging.getLogger(__name__)
            logger.warning("SHAP explainer failed, falling back to estimator-based importances: %s", shap_exc)

            try:
                model = wrapper.model
                final = model.steps[-1][1] if hasattr(model, "steps") else model

                if hasattr(final, "feature_importances_"):
                    importances = list(getattr(final, "feature_importances_"))
                    feature_importance = {n: float(v) for n, v in zip(feature_names, importances)}
                elif hasattr(final, "coef_"):
                    coef = getattr(final, "coef_")
                    try:
                        coef_arr = coef[0] if coef.ndim > 1 else coef
                    except Exception:
                        coef_arr = coef
                    feature_importance = {n: float(v) for n, v in zip(feature_names, list(coef_arr))}
                else:
                    feature_importance = {n: 0.0 for n in feature_names}
            except Exception as exc2:
                logger.exception("Failed to compute fallback feature importance: %s", exc2)
                feature_importance = {n: 0.0 for n in feature_names}

            # Prepare top features
            sorted_feats = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
            top_features = [{"feature": f, "importance": v, "value": None} for f, v in sorted_feats[:5]]

            return ShapVisualizationResponse(
                prediction=prediction,
                feature_importance=feature_importance,
                shap_values=[],
                base_value=0.0,
                plot_base64=None,
                top_features=top_features,
            )
        
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.exception("SHAP explanation failed")
        raise HTTPException(
            status_code=500,
            detail=f"SHAP explanation failed: {str(exc)}",
        )
