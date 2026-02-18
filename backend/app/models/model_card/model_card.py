from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime
import logging
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# -------------------------------------------------
# ----- Models ------------------------------------
# -------------------------------------------------

class ModelMetrics(BaseModel):
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    roc_auc: Optional[float] = None


class ModelFeature(BaseModel):
    name: str
    description: str


class ModelCard(BaseModel):
    name: str
    version: str
    last_updated: str
    model_type: str
    model_path: Optional[str] = None
    features: List[ModelFeature]
    metrics: Optional[ModelMetrics] = None
    intended_use: List[str]
    not_intended_for: List[str]
    limitations: List[str]
    recommendations: List[str]
    metadata: Optional[Dict[str, Any]] = None


# -------------------------------------------------
# ----- JSON Config Loader ------------------------
# -------------------------------------------------

def load_model_card_config() -> dict:
    """
    Loads model card config from JSON file.
    """
    config_path = Path(__file__).parent / "model_card_config.json"

    if not config_path.exists():
        logger.warning("Model card config JSON not found: %s", config_path)
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error("Error reading model card config JSON: %s", e)
        return {}


# -------------------------------------------------
# ----- Load Function -----------------------------
# -------------------------------------------------

def load_model_card() -> ModelCard:
    """
    Load model card information.
    Static fields come from JSON config.
    Dynamic fields are extracted from runtime model.
    """

    metadata: Dict[str, Any] = {}

    # ----- Load JSON config -----
    config = load_model_card_config()

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
                elif hasattr(model, "coef_"):
                    coef = model.coef_
                    n_features = (
                        coef.shape[1]
                        if getattr(coef, "ndim", 1) > 1
                        else len(coef)
                    )
        except Exception:
            n_features = None

        metadata.update({
            "is_loaded": wrapper.is_loaded()
            if callable(getattr(wrapper, "is_loaded", None))
            else False,
            "n_features": n_features,
            "model_repr": repr(model),
        })

    else:
        model_type = "LogisticRegression (scikit-learn)"
        model_path = os.path.abspath(
            "backend/app/models/logreg_best_model.pkl"
        )

    # ----- Features -----
    features: List[ModelFeature] = []
    try:
        from app.core.preprocessor import EXPECTED_FEATURES

        features = [
            ModelFeature(name=f, description="")
            for f in EXPECTED_FEATURES
        ]

        metadata["n_features_from_preprocessor"] = len(features)

    except Exception:
        features = [
            ModelFeature(
                name="68 clinical features",
                description="See backend/app/core/preprocessor.py",
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
            explainer = ShapExplainer(
                wrapper.model,
                background_data=wrapper.background,
            )

            top_features = explainer.get_top_features(
                sample,
                top_k=10,
            )

            metadata["top_shap_features"] = top_features

    except Exception as e:
        logger.info("Could not extract top SHAP features: %s", e)

    # ----- Metrics from JSON -----
    metrics = None
    if config.get("metrics"):
        try:
            metrics = ModelMetrics(**config.get("metrics", {}))
        except Exception as e:
            logger.error("Error parsing metrics config: %s", e)

    # ----- Return ModelCard -----
    return ModelCard(
        name=config.get("name", "Unknown Model"),
        version=config.get("version", "Unknown"),
        last_updated=datetime.now().strftime("%Y-%m-%d"),

        model_type=model_type,
        model_path=model_path,
        features=features,

        metrics=metrics,

        intended_use=config.get("intended_use", []),
        not_intended_for=config.get("not_intended_for", []),
        limitations=config.get("limitations", []),
        recommendations=config.get("recommendations", []),

        metadata=metadata,
    )
