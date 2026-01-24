from fastapi import APIRouter, HTTPException
import logging
import numpy as np
from app.models.explainers.lime_explainer import LimeExplainer
from app.models.prediction import PredictionInput
from app.core.model import model, wrapper  # bestehendes Modell + wrapper für preprocessing

router = APIRouter(prefix="/lime", tags=["lime"])

# Definiere die Features, die LIME erwartet
FEATURE_NAMES = ['age', 'hearing_loss_duration', 'implant_type']

# Initialisiere LIME Explainer
lime_explainer = LimeExplainer(model, FEATURE_NAMES)


@router.post("/predict")
async def lime_predict(input_data: PredictionInput):
    """LIME-basierte Vorhersage mit Erklärung"""
    logger = logging.getLogger(__name__)
    try:
        # Konvertiere Input in dict
        input_dict = input_data.model_dump(by_alias=True)

        # Preprocessing: Input auf Modell-Features anpassen
        if wrapper is not None:
            preprocessed = wrapper.prepare_input(input_dict)
        else:
            # fallback: simple array
            preprocessed = np.array([
                input_dict.get('age', 0),
                input_dict.get('hearing_loss_duration', 0),
                1 if input_dict.get('implant_type', '') == 'type_a' else 0
            ]).reshape(1, -1)

        # Prediction
        pred_proba = model.predict_proba(preprocessed)
        try:
            prediction = float(pred_proba[0][1])  # Wahrscheinlichkeit positive Klasse
        except Exception:
            prediction = float(pred_proba[0])

        # LIME Erklärung vorbereiten
        lime_explainer.prepare_training_data(preprocessed)  # Trainingsdaten für LIME
        explanation = lime_explainer.explain(preprocessed[0])

        # Top Features extrahieren
        sorted_features = sorted(
            explanation.items(),
            key=lambda x: abs(x[1]['importance']),
            reverse=True
        )
        top_features = [
            {"feature": f, "importance": v['importance'], "direction": v['direction']}
            for f, v in sorted_features[:5]
        ]

        return {
            "prediction": prediction,
            "feature_importance": {f: v['importance'] for f, v in explanation.items()},
            "top_features": top_features,
        }

    except Exception as e:
        logger.exception("LIME prediction failed")
        raise HTTPException(status_code=500, detail=str(e))
