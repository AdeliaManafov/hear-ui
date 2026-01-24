from app.models.feedback import Feedback, FeedbackCreate
from app.models.prediction import Prediction, PredictionCreate
from app.models.patient_record import Patient, PatientCreate
from pathlib import Path
from typing import Dict
import json
from datetime import datetime
from app.models.model_card.model_card import ModelCard, ModelMetrics

# token models (small helpers)
from app.models.token import NewPassword, Token

__all__ = [
    # Token / password reset
    "Token",
    "NewPassword",
    # Feedback
    "Feedback",
    "FeedbackCreate",
    # Prediction
    "Prediction",
    "PredictionCreate",
    # Patient
    "Patient",
    "PatientCreate",
]
def load_model_card() -> ModelCard:
    """Lädt die aktuelle Model Card."""
    # Implementierung der Lade-Logik
    pass

def save_model_card(card: ModelCard) -> None:
    """Speichert die Model Card."""
    # Implementierung der Speicher-Logik
    pass

def update_metrics(metrics: Dict[str, float]) -> None:
    """Aktualisiert die Metriken in der Model Card."""
    card = load_model_card()
    card.metrics = ModelMetrics(**metrics)
    card.last_updated = datetime.now()
    save_model_card(card)

