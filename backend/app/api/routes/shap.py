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
        
        # Get prediction
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
        
        # Generate background data (transformed features)
        from app.core.background_data import create_synthetic_background, get_feature_names_from_pipeline
        
        # Create synthetic background and transform it
        raw_background, transformed_background = create_synthetic_background(
            n_samples=50,
            include_transformed=True,
            pipeline=wrapper.model
        )
        
        if transformed_background is None:
            raise HTTPException(
                status_code=500,
                detail="Could not create transformed background data for SHAP"
            )
        
        # Get transformed feature names
        transformed_feature_names = get_feature_names_from_pipeline(wrapper.model)
        if not transformed_feature_names:
            raise HTTPException(
                status_code=500,
                detail="Could not extract feature names from pipeline"
            )
        
        # Initialize SHAP explainer on transformed features. Pass the raw background
        # DataFrame so the explainer can deterministically encode/transform it.
        shap_explainer = ShapExplainer(
            model=wrapper.model,
            feature_names=transformed_feature_names,
            background_data=raw_background,
            use_transformed=True,  # Work on transformed features
        )
        
        # Transform input sample
        if hasattr(wrapper.model, 'named_steps'):
            preprocessor = wrapper.model.named_steps.get('preprocessor')
            if preprocessor:
                features_df = pd.DataFrame([feature_dict])
                transformed_sample = preprocessor.transform(features_df)
            else:
                raise HTTPException(status_code=500, detail="No preprocessor found in pipeline")
        else:
            transformed_sample = wrapper.prepare_input(feature_dict)
            if hasattr(transformed_sample, 'values'):
                transformed_sample = transformed_sample.values
        
        # Get SHAP explanation on transformed sample
        try:
            shap_result = shap_explainer.explain(
                transformed_sample,
                return_plot=request.include_plot,
            )
            
            if isinstance(shap_result, dict) and (shap_result.get("error") or not shap_result.get("feature_importance")):
                raise RuntimeError(f"SHAP explainer error: {shap_result.get('error')}")
            
            if not isinstance(shap_result, dict):
                shap_result = {"feature_importance": {}, "shap_values": [], "base_value": 0.0}
            
            # Get top features
            top_features = shap_explainer.get_top_features(transformed_sample, top_k=5)
            
            return ShapVisualizationResponse(
                prediction=prediction,
                feature_importance=shap_result.get("feature_importance", {}),
                shap_values=shap_result.get("shap_values", []),
                base_value=shap_result.get("base_value", 0.0),
                plot_base64=shap_result.get("plot_base64"),
                top_features=top_features,
            )
        
        except Exception as shap_exc:
            logger = logging.getLogger(__name__)
            logger.warning("SHAP failed (%s), using coefficient fallback", shap_exc)
            
            # Coefficient-based fallback
            feature_importance = {}
            try:
                estimator = wrapper.model.steps[-1][1] if hasattr(wrapper.model, 'steps') else wrapper.model
                if hasattr(estimator, 'coef_'):
                    coef = estimator.coef_[0] if len(estimator.coef_.shape) > 1 else estimator.coef_
                    # Get sample values
                    if hasattr(transformed_sample, 'flatten'):
                        sample_vals = transformed_sample.flatten()
                    else:
                        sample_vals = transformed_sample[0] if len(transformed_sample) > 0 else transformed_sample
                    
                    # Compute contributions
                    for i, (fname, c, val) in enumerate(zip(transformed_feature_names, coef, sample_vals)):
                        feature_importance[fname] = float(c * val)
                elif hasattr(estimator, 'feature_importances_'):
                    # Tree-based: use feature importances
                    for fname, imp in zip(transformed_feature_names, estimator.feature_importances_):
                        feature_importance[fname] = float(imp)
            except Exception:
                feature_importance = {n: 0.0 for n in transformed_feature_names}
            
            # Create top features
            sorted_feats = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
            top_features = [
                {"feature": f, "importance": v, "value": None} for f, v in sorted_feats[:5]
            ]
            
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
