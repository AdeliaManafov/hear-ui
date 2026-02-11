import logging
import os
from datetime import datetime
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ----- Models -----
class ModelMetrics(BaseModel):
    accuracy: float | None = 0.62
    precision: float | None = None
    recall: float | None = None
    f1_score: float | None = 0.55
    roc_auc: float | None = None


class ModelFeature(BaseModel):
    name: str
    description: str


class ModelCard(BaseModel):
    name: str
    version: str
    last_updated: str
    model_type: str
    model_path: str | None = None
    features: list[ModelFeature]
    metrics: ModelMetrics | None = None
    intended_use: list[str]
    not_intended_for: list[str]
    limitations: list[str]
    recommendations: list[str]
    metadata: dict[str, Any] | None = None


# ----- Load Function -----
def load_model_card() -> ModelCard:
    """
    Load model card information. Try to extract as much as possible automatically.
    Manual fields (metrics, intended_use, recommendations, limitations) must be filled later.
    """
    metadata: dict[str, Any] = {}

    # ----- Try importing FastAPI wrapper -----
    try:
        from app.main import app as fastapi_app

        wrapper = getattr(fastapi_app.state, "model_wrapper", None)
    except Exception as e:
        logger.warning("FastAPI import failed: %s", e)
        wrapper = None

    # ----- Model info -----
    if wrapper:
        model = getattr(wrapper, "model", None)
        model_type = type(model).__name__ if model else "Unknown"
        model_path = getattr(wrapper, "model_path", None)

        # n_features
        n_features = None
        try:
            if model is not None:
                if hasattr(model, "n_features_in_"):
                    n_features = model.n_features_in_
        except Exception:
            n_features = None

        metadata.update(
            {
                "is_loaded": wrapper.is_loaded()
                if callable(getattr(wrapper, "is_loaded", None))
                else False,
                "n_features": n_features,
                "model_repr": repr(model),
            }
        )
    else:
        model_type = "RandomForestClassifier (scikit-learn)"
        model_path = os.path.abspath("backend/app/models/random_forest_final.pkl")

    # ----- Features -----
    features: list[ModelFeature] = []
    try:
        from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF

        features = [ModelFeature(name=f, description="") for f in EXPECTED_FEATURES_RF]
        metadata["n_features_from_preprocessor"] = len(features)
    except Exception:
        features = [
            ModelFeature(
                name="39 clinical features",
                description="RandomForest model for cochlear implant outcome prediction",
            )
        ]

    # ----- SHAP Top Features (optional) -----
    try:
        if (
            wrapper
            and wrapper.is_loaded()
            and hasattr(wrapper, "background")
            and hasattr(wrapper, "sample_for_shap")
        ):
            from app.core.shap_explainer import ShapExplainer

            sample = wrapper.sample_for_shap()
            explainer = ShapExplainer(wrapper.model, background_data=wrapper.background)
            top_features = explainer.get_top_features(sample, top_k=10)
            metadata["top_shap_features"] = top_features
    except Exception as e:
        logger.info("Could not extract top SHAP features: %s", e)

    # ----- Return ModelCard -----
    return ModelCard(
        name="HEAR CI Prediction Model",
        version="v1 (draft)",
        last_updated=datetime.now().strftime("%Y-%m-%d"),
        model_type=model_type,
        model_path=model_path,
        features=features,
        metrics=ModelMetrics(),  # Must be filled manually
        intended_use=[
            "Support clinicians estimating outcome probability",
            "Decision support tool for cochlear implant planning",
        ],
        not_intended_for=[
            "Autonomous clinical decisions",
            "Use outside validated populations",
            "Legal or administrative decisions",
        ],
        limitations=[
            "Performance depends on background dataset used for SHAP",
            "Bias possible due to preprocessing defaults",
            "Not validated outside training population",
        ],
        recommendations=[
            "Use only as support tool",
            "Human medical judgment has priority",
            "Regular evaluation recommended",
        ],
        metadata=metadata,
    )
