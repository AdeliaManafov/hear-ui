# app/core/predict.py
from typing import Dict

def dummy_predict(patient_data: dict) -> Dict:
    """
    Dummy-Vorhersage für MVP. Gibt Wahrscheinlichkeit und SHAP-ähnliche Erklärung zurück.
    """
    # Beispiel: feste Wahrscheinlichkeit
    prediction = 0.65

    # Dummy SHAP Feature-Importance
    explanation = {
        "age": 0.2,
        "hearing_loss_duration": 0.3,
        "implant_type": 0.15,
        "other_feature": 0.1
    }

    return {"prediction": prediction, "explanation": explanation}
