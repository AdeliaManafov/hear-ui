import logging
import os
from datetime import datetime
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ----- Models -----
class ModelMetrics(BaseModel):
    accuracy: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1_score: float | None = None
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
                elif hasattr(model, "coef_"):
                    coef = model.coef_
                    n_features = (
                        coef.shape[1] if getattr(coef, "ndim", 1) > 1 else len(coef)
                    )
        except Exception:
            n_features = None

        metadata.update(
            {
                "is_loaded": wrapper.is_loaded()
                if callable(getattr(wrapper, "is_loaded", None))
                else False,
                "n_features": n_features,
                "model_repr": repr(model),
                "model_description": "Random Forest Classifier: Ensemble von Entscheidungsbäumen, nicht-linear, robuste Vorhersagen bei heterogenen Patient:innenmerkmalen",
                "training_data": "Beispiel Patienten",
                "train_test_split": "80/20",
            }
        )
    else:
        model_type = "LogisticRegression (scikit-learn)"
        model_path = os.path.abspath("backend/app/models/logreg_best_model.pkl")

    # ----- Features -----
    # Use Random Forest features (39 features) instead of legacy LR features (68)
    features: list[ModelFeature] = []
    try:
        from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF

        # Filter out placeholder features (will be replaced with real features later)
        features = [
            ModelFeature(name=f, description=f"Klinisches Merkmal: {f}")
            for f in EXPECTED_FEATURES_RF
            if not f.startswith("_placeholder")
        ]
        metadata["n_features_from_adapter"] = len(features)
    except Exception:
        features = [
            ModelFeature(
                name="39 klinische Merkmale",
                description="Siehe backend/app/core/rf_dataset_adapter.py",
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
        version="v1.0",
        last_updated=datetime.now().strftime("%Y-%m-%d"),
        model_type=model_type,
        model_path=model_path,
        features=features,
        metrics=ModelMetrics(
            accuracy=0.82,
            precision=0.84,
            recall=0.80,
            f1_score=0.82,
            roc_auc=0.87,
        ),
        intended_use=[
            "Unterstützung von Ärzt:innen bei der Abschätzung der Erfolgswahrscheinlichkeit eines Cochlea-Implantats",
            "Entscheidungshilfe für die Planung von CI-Operationen",
            "Bildungswerkzeug zur Demonstration von XAI-Methoden in der klinischen Entscheidungsfindung",
        ],
        not_intended_for=[
            "Autonome klinische Entscheidungen ohne ärztliche Bewertung",
            "Verwendung außerhalb der validierten Patient:innenpopulation",
            "Rechtliche oder administrative Entscheidungen",
            "Patient:innen unter 18 Jahren",
        ],
        limitations=[
            "Modell basiert auf einem begrenzten Datensatz (N=137)",
            "Nicht validiert außerhalb der Trainingspopulation (Universitätsklinikum Essen)",
            "Vorhersagen sind unterstützende Hinweise, keine deterministischen Ergebnisse",
            "Mögliche Biases in Bezug auf Altersgruppen, Geschlecht und Art des Hörverlusts",
            "Modell-Performance kann bei Edge Cases variieren, die im Training nicht vertreten waren",
            "Vorhersagen bei fehlenden oder unvollständigen Daten weniger zuverlässig",
            "SHAP-Interpretationen zeigen relative Einflussgrößen, nicht absolute Kausalität",
        ],
        recommendations=[
            "Nur als Unterstützungswerkzeug verwenden – menschliche medizinische Urteilsfähigkeit hat Vorrang",
            "Ergebnisse stets im klinischen Kontext und unter Berücksichtigung der Patient:innenhistorie interpretieren",
            "SHAP-Erklärungen nutzen, um Vorhersagen nachzuvollziehen und kritisch zu bewerten",
            "Regelmäßige Evaluation und Aktualisierung des Modells empfohlen (z. B. alle 6 Monate)",
            "Bei unerwarteten Vorhersagen: manuelle Überprüfung der Eingabedaten",
        ],
        metadata=metadata,
    )
