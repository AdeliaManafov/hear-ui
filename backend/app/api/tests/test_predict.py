from unittest.mock import MagicMock

from app.api.routes.predict import compute_prediction_and_explanation


def test_compute_prediction_and_explanation_structure():
    patient = {"age": 40, "hearing_loss_duration": 5.0, "implant_type": "type_b"}

    # Create a mock model wrapper with a working predict method
    mock_wrapper = MagicMock()
    mock_wrapper.model = MagicMock()
    mock_wrapper.model.feature_importances_ = [0.3, 0.5, 0.2]
    mock_wrapper.predict.return_value = [0.75]
    mock_wrapper.get_feature_names.return_value = ["age", "hearing_loss_duration", "implant_type"]
    mock_wrapper.prepare_input.return_value = MagicMock(
        values=MagicMock(return_value=[[40, 5.0, 1.0]]),
        flatten=MagicMock(return_value=[40, 5.0, 1.0]),
    )
    mock_wrapper.prepare_input.return_value.values.flatten = MagicMock(return_value=[40, 5.0, 1.0])

    result = compute_prediction_and_explanation(patient, mock_wrapper)
    assert "prediction" in result
    assert "explanation" in result
    assert isinstance(result["prediction"], float | int)
