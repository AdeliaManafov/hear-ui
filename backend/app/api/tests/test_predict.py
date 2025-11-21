
from app.api.routes.predict import compute_prediction_and_explanation


def test_compute_prediction_and_explanation_structure():
    patient = {"age": 40, "hearing_loss_duration": 5.0, "implant_type": "type_b"}
    result = compute_prediction_and_explanation(patient)
    assert "prediction" in result
    assert "explanation" in result
    assert isinstance(result["prediction"], (float, int))
    assert isinstance(result["explanation"], dict)
    # explanation keys should at least contain the feature names used
    for key in ["age", "hearing_loss_duration", "implant_type"]:
        assert key in result["explanation"]
        # values should be numeric
        assert isinstance(result["explanation"][key], (float, int))
