"""Additional tests for app.core.model_wrapper – targeting uncovered branches.

Focuses on: load_model (joblib/pickle), predict_with_confidence, clip_probabilities,
_auto_detect_model_adapter, predict with pre-processed input.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, mock_open, patch

import numpy as np
import pytest

from app.core.model_wrapper import (
    PROB_CLIP_MAX,
    PROB_CLIP_MIN,
    ModelWrapper,
    clip_probabilities,
)


# ===========================================================================
# clip_probabilities
# ===========================================================================


class TestClipProbabilities:
    def test_clips_low(self):
        result = clip_probabilities(np.array([0.0, 0.005]))
        assert all(result >= PROB_CLIP_MIN)

    def test_clips_high(self):
        result = clip_probabilities(np.array([1.0, 0.999]))
        assert all(result <= PROB_CLIP_MAX)

    def test_no_clip_needed(self):
        result = clip_probabilities(np.array([0.5]))
        assert result[0] == pytest.approx(0.5)

    def test_custom_bounds(self):
        result = clip_probabilities(np.array([0.0, 1.0]), min_val=0.1, max_val=0.9)
        assert result[0] == pytest.approx(0.1)
        assert result[1] == pytest.approx(0.9)


# ===========================================================================
# ModelWrapper – load_model
# ===========================================================================


class TestModelWrapperLoadModel:
    def test_file_not_found(self):
        """load_model raises FileNotFoundError for missing file."""
        with patch("app.core.model_wrapper.MODEL_PATH", "/nonexistent/model.pkl"):
            wrapper = ModelWrapper.__new__(ModelWrapper)
            wrapper.model = None
            wrapper.model_adapter = None
            wrapper.dataset_adapter = MagicMock()
            wrapper.model_path = "/nonexistent/model.pkl"
            with pytest.raises(FileNotFoundError):
                wrapper.load_model()

    def test_joblib_fallback_to_pickle(self):
        """When joblib.load fails, falls back to pickle.load."""
        import pickle

        fake_model = "fake_model_sentinel"

        with (
            patch("app.core.model_wrapper.MODEL_PATH", "/fake/model.pkl"),
            patch("os.path.exists", return_value=True),
            patch("app.core.model_wrapper.joblib") as mock_joblib,
            patch("builtins.open", mock_open(read_data=pickle.dumps(fake_model))),
            patch.object(ModelWrapper, "_auto_detect_model_adapter", return_value=MagicMock()),
        ):
            mock_joblib.load.side_effect = Exception("joblib fail")

            wrapper = ModelWrapper.__new__(ModelWrapper)
            wrapper.model = None
            wrapper.model_adapter = None
            wrapper.dataset_adapter = MagicMock()
            wrapper.model_path = "/fake/model.pkl"
            wrapper.load_model()
            assert wrapper.model is not None

    def test_pickle_only_when_no_joblib(self):
        """When joblib is None, uses pickle directly."""
        import pickle

        fake_model = "fake_model_sentinel"

        with (
            patch("app.core.model_wrapper.MODEL_PATH", "/fake/model.pkl"),
            patch("os.path.exists", return_value=True),
            patch("app.core.model_wrapper.joblib", None),
            patch("builtins.open", mock_open(read_data=pickle.dumps(fake_model))),
            patch.object(ModelWrapper, "_auto_detect_model_adapter", return_value=MagicMock()),
        ):
            wrapper = ModelWrapper.__new__(ModelWrapper)
            wrapper.model = None
            wrapper.model_adapter = None
            wrapper.dataset_adapter = MagicMock()
            wrapper.model_path = "/fake/model.pkl"
            wrapper.load_model()
            assert wrapper.model is not None


# ===========================================================================
# ModelWrapper – _auto_detect_model_adapter
# ===========================================================================


class TestAutoDetectModelAdapter:
    def test_no_model_raises(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = None
        with pytest.raises(RuntimeError, match="No model loaded"):
            wrapper._auto_detect_model_adapter()

    def test_sklearn_model(self):
        from sklearn.linear_model import LogisticRegression

        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = LogisticRegression()
        adapter = wrapper._auto_detect_model_adapter()
        assert adapter.get_model_type() == "sklearn"

    def test_generic_model_with_predict(self):
        """Any model with predict() gets SklearnModelAdapter."""
        m = MagicMock()
        m.predict = MagicMock()
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = m
        adapter = wrapper._auto_detect_model_adapter()
        assert adapter.get_model_type() == "sklearn"


# ===========================================================================
# ModelWrapper – predict
# ===========================================================================


class TestModelWrapperPredict:
    def test_predict_no_model_raises(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = None
        wrapper.model_adapter = None
        wrapper.dataset_adapter = MagicMock()
        with pytest.raises(RuntimeError, match="No model loaded"):
            wrapper.predict({"Alter [J]": 50})

    def test_predict_no_adapter_raises(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = MagicMock()
        wrapper.model_adapter = None
        wrapper.dataset_adapter = MagicMock()
        with pytest.raises(RuntimeError, match="No model adapter"):
            wrapper.predict({"Alter [J]": 50})

    def test_predict_with_dict(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = MagicMock()
        wrapper.model_adapter = MagicMock()
        wrapper.model_adapter.predict_proba.return_value = np.array([0.75])
        wrapper.dataset_adapter = MagicMock()
        wrapper.dataset_adapter.preprocess.return_value = np.array([[1.0]])

        result = wrapper.predict({"Alter [J]": 50}, clip=True)
        assert result[0] == pytest.approx(0.75)

    def test_predict_with_array_input(self):
        """When input is already an array, skip preprocessing."""
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = MagicMock()
        wrapper.model_adapter = MagicMock()
        wrapper.model_adapter.predict_proba.return_value = np.array([[0.3, 0.7]])
        wrapper.dataset_adapter = MagicMock()

        result = wrapper.predict(np.array([[1.0, 2.0]]), clip=True)
        # should extract column 1 from 2D output
        assert result[0] == pytest.approx(0.7)

    def test_predict_no_clip(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = MagicMock()
        wrapper.model_adapter = MagicMock()
        wrapper.model_adapter.predict_proba.return_value = np.array([0.001])
        wrapper.dataset_adapter = MagicMock()
        wrapper.dataset_adapter.preprocess.return_value = np.array([[1.0]])

        result = wrapper.predict({"x": 1}, clip=False)
        assert result[0] == pytest.approx(0.001)


# ===========================================================================
# ModelWrapper – predict_with_confidence
# ===========================================================================


class TestPredictWithConfidence:
    def test_basic(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = MagicMock()
        wrapper.model_adapter = MagicMock()
        wrapper.model_adapter.predict_proba.return_value = np.array([0.6])
        wrapper.dataset_adapter = MagicMock()
        wrapper.dataset_adapter.preprocess.return_value = np.array([[1.0]])

        result = wrapper.predict_with_confidence({"x": 1})
        assert "prediction" in result
        assert "confidence_interval" in result
        assert "uncertainty" in result
        assert "confidence_level" in result
        lower, upper = result["confidence_interval"]
        assert lower <= result["prediction"] <= upper

    def test_no_model_raises(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = None
        wrapper.dataset_adapter = MagicMock()
        with pytest.raises(RuntimeError, match="No model loaded"):
            wrapper.predict_with_confidence({"x": 1})

    def test_high_prediction_has_lower_uncertainty(self):
        """Predictions closer to 0 or 1 should have lower uncertainty factor."""
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = MagicMock()
        wrapper.model_adapter = MagicMock()
        wrapper.dataset_adapter = MagicMock()
        wrapper.dataset_adapter.preprocess.return_value = np.array([[1.0]])

        # High prediction
        wrapper.model_adapter.predict_proba.return_value = np.array([0.95])
        high_result = wrapper.predict_with_confidence({"x": 1})

        # Middle prediction
        wrapper.model_adapter.predict_proba.return_value = np.array([0.5])
        mid_result = wrapper.predict_with_confidence({"x": 1})

        # Mid-range should have higher uncertainty
        assert mid_result["uncertainty"] >= high_result["uncertainty"]


# ===========================================================================
# ModelWrapper – helper methods
# ===========================================================================


class TestModelWrapperHelpers:
    def test_is_loaded(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.model = None
        assert wrapper.is_loaded() is False
        wrapper.model = MagicMock()
        assert wrapper.is_loaded() is True

    def test_load_alias(self):
        """load() is alias for load_model()."""
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.load_model = MagicMock()
        wrapper.load()
        wrapper.load_model.assert_called_once()

    def test_get_feature_names(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.dataset_adapter = MagicMock()
        wrapper.dataset_adapter.get_feature_names.return_value = ["a", "b"]
        assert wrapper.get_feature_names() == ["a", "b"]

    def test_prepare_input(self):
        wrapper = ModelWrapper.__new__(ModelWrapper)
        wrapper.dataset_adapter = MagicMock()
        wrapper.dataset_adapter.preprocess.return_value = np.array([[1.0]])
        result = wrapper.prepare_input({"x": 1})
        np.testing.assert_array_equal(result, [[1.0]])
