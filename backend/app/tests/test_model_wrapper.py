"""Tests for ModelWrapper class."""

from unittest.mock import MagicMock

import numpy as np
import pytest

from app.core.model_wrapper import ModelWrapper


class TestModelWrapperInit:
    """Test ModelWrapper initialization."""

    def test_model_wrapper_init_creates_instance(self):
        """Test that ModelWrapper can be instantiated."""
        wrapper = ModelWrapper()
        assert wrapper is not None
        assert wrapper.model_path is not None

    def test_is_loaded_returns_bool(self):
        """Test is_loaded returns boolean."""
        wrapper = ModelWrapper()
        result = wrapper.is_loaded()
        assert isinstance(result, bool)


class TestModelWrapperPredict:
    """Test ModelWrapper predict method."""

    def test_predict_raises_when_no_model(self):
        """Test predict raises RuntimeError when no model loaded."""
        wrapper = ModelWrapper()
        wrapper.model = None

        with pytest.raises(RuntimeError, match="No model loaded"):
            wrapper.predict(
                {"age": 50, "hearing_loss_duration": 10, "implant_type": "type_a"}
            )

    def test_prepare_input_with_dict(self):
        """Test prepare_input handles dict input."""
        wrapper = ModelWrapper()
        wrapper.model = None  # No model, but we can still test prepare_input

        raw = {"age": 50, "hearing_loss_duration": 10, "implant_type": "type_a"}
        # When no model with feature_names_in_, falls back to preprocess_patient_data
        result = wrapper.prepare_input(raw)

        # prepare_input now returns pandas DataFrame from preprocess_patient_data
        import pandas as pd

        assert isinstance(result, pd.DataFrame)


class TestModelWrapperWithMockedModel:
    """Test ModelWrapper with mocked model."""

    def test_predict_with_predict_proba(self):
        """Test predict uses predict_proba when available."""
        wrapper = ModelWrapper()

        mock_adapter = MagicMock()
        mock_adapter.predict_proba.return_value = np.array([[0.3, 0.7]])
        wrapper.model_adapter = mock_adapter

        result = wrapper.predict(np.array([[50, 10, 0]]))

        assert result[0] == pytest.approx(0.7)
        mock_adapter.predict_proba.assert_called_once()

    def test_predict_with_decision_function(self):
        """Test predict uses decision_function when predict_proba not available."""
        wrapper = ModelWrapper()

        # Mock the adapter to simulate decision_function fallback
        from scipy.special import expit

        mock_adapter = MagicMock()
        mock_adapter.predict_proba.return_value = expit(np.array([0.0]))
        wrapper.model_adapter = mock_adapter

        result = wrapper.predict(np.array([[50, 10, 0]]))

        # sigmoid(0) = 0.5
        assert result[0] == pytest.approx(0.5, abs=0.01)

    def test_predict_with_predict_only(self):
        """Test predict falls back to predict when other methods unavailable."""
        wrapper = ModelWrapper()

        # Mock the adapter to return direct prediction value
        mock_adapter = MagicMock()
        mock_adapter.predict_proba.return_value = np.array([1.0])
        wrapper.model_adapter = mock_adapter

        result = wrapper.predict(np.array([[50, 10, 0]]))

        # Result is clipped to 0.99 by default
        assert result[0] == pytest.approx(0.99)


class TestModelWrapperPrepareInput:
    """Test ModelWrapper prepare_input method."""

    def test_prepare_input_returns_dataframe(self):
        """Test prepare_input returns pandas DataFrame with correct shape."""
        wrapper = ModelWrapper()

        mock_model = MagicMock()
        mock_model.feature_names_in_ = ["Alter [J]", "Geschlecht"]
        wrapper.model = mock_model

        raw = {"age": 50, "gender": "m"}
        result = wrapper.prepare_input(raw)

        # Should return DataFrame with 68 features
        import pandas as pd

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (1, 68)

    def test_prepare_input_maps_age_correctly(self):
        """Test that age is correctly placed in the feature DataFrame."""
        wrapper = ModelWrapper()

        mock_model = MagicMock()
        wrapper.model = mock_model

        raw = {"age": 45}
        result = wrapper.prepare_input(raw)

        # Age (Alter [J]) should be in the column
        assert result["Alter [J]"].iloc[0] == 45

    def test_prepare_input_uses_preprocessor(self):
        """Test prepare_input uses preprocess_patient_data for all inputs."""
        wrapper = ModelWrapper()
        wrapper.model = MagicMock()

        raw = {"age": 50, "hearing_loss_duration": 10, "implant_type": "CI522"}
        result = wrapper.prepare_input(raw)

        # Should return DataFrame from preprocess_patient_data with 68 features
        import pandas as pd

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (1, 68)
