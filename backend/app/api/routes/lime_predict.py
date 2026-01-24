from fastapi import APIRouter, HTTPException
from app.ml.explainers.lime_explainer import LimeExplainer
from app.models.prediction import PredictionInput, PredictionOutput
from app.core.model import model  # Ihr bestehendes Modell

router = APIRouter()

# Initialisiere LIME Explainer
feature_names = ['age', 'hearing_loss_duration', 'implant_type']
explainer = LimeExplainer(model, feature_names)

@router.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        # Vorhersage machen
        prediction = model.predict_proba(input_data)

        # LIME-Erklärung generieren
        explanation = explainer.explain(input_data)

        return {
            "prediction": float(prediction[0][1]),  # Wahrscheinlichkeit für positive Klasse
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
