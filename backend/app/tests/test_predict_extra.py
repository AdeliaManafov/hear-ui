"""Additional tests for predict route behavior."""
from unittest.mock import patch, MagicMock
from app.api.routes.predict import PatientData, predict
from app.models import Prediction


def test_predict_persist_error():
    patient = PatientData()
    mock_db = MagicMock()
    mock_db.add = MagicMock()
    # commit raises
    mock_db.commit.side_effect = Exception("db commit failed")
    mock_db.rollback = MagicMock()

    with patch('app.api.routes.predict.model_wrapper') as mock_wrapper:
        mock_wrapper.predict.return_value = [0.9]
        res = predict(patient=patient, db=mock_db, persist=True)

        assert res['prediction'] == 0.9
        assert res.get('persisted') is False
        assert 'persist_error' in res


def test_predict_persist_success():
    patient = PatientData()
    mock_db = MagicMock()
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    with patch('app.api.routes.predict.model_wrapper') as mock_wrapper:
        mock_wrapper.predict.return_value = [0.66]
        res = predict(patient=patient, db=mock_db, persist=True)

        assert res['prediction'] == 0.66
        assert res.get('persisted') is True
        assert 'prediction_id' in res or res.get('prediction_id') is None
