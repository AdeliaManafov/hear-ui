
from unittest.mock import MagicMock

import numpy as np

from app.api.routes.predict import compute_prediction_and_explanation


def test_compute_prediction_and_explanation_structure():
    patient = {"age": 40, "hearing_loss_duration": 5.0, "implant_type": "type_b"}

    # Create a mock model_wrapper
    mock_wrapper = MagicMock()
    mock_wrapper.model = None  # Disable SHAP explanation
    mock_wrapper.predict.return_value = np.array([0.75])

    result = compute_prediction_and_explanation(patient, mock_wrapper)
    assert "prediction" in result
    assert "explanation" in result
    assert isinstance(result["prediction"], (float, int))
