"""Tests for app.core.model_adapter – ModelAdapter, SklearnModelAdapter, DatasetAdapter, GenericDatasetAdapter."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest

from app.core.model_adapter import (
    DatasetAdapter,
    GenericDatasetAdapter,
    ModelAdapter,
    SklearnModelAdapter,
)

# ===========================================================================
# ModelAdapter (ABC) – ensure contract
# ===========================================================================


class TestModelAdapterABC:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            ModelAdapter(MagicMock())

    def test_default_feature_importance_is_none(self):
        """Concrete subclass inherits default get_feature_importance."""

        class Dummy(ModelAdapter):
            def predict(self, X):
                return X

            def predict_proba(self, X):
                return X

            def get_model_type(self):
                return "dummy"

        d = Dummy(MagicMock())
        assert d.get_feature_importance() is None

    def test_default_get_coefficients_is_none(self):
        class Dummy(ModelAdapter):
            def predict(self, X):
                return X

            def predict_proba(self, X):
                return X

            def get_model_type(self):
                return "dummy"

        d = Dummy(MagicMock())
        assert d.get_coefficients() is None


# ===========================================================================
# SklearnModelAdapter
# ===========================================================================


class TestSklearnModelAdapterPredict:
    def test_predict_delegates(self):
        model = MagicMock()
        model.predict.return_value = np.array([1, 0])
        adapter = SklearnModelAdapter(model)
        result = adapter.predict(np.array([[1, 2]]))
        np.testing.assert_array_equal(result, [1, 0])
        model.predict.assert_called_once()

    def test_get_model_type(self):
        assert SklearnModelAdapter(MagicMock()).get_model_type() == "sklearn"


class TestSklearnModelAdapterPredictProba:
    def test_predict_proba_binary(self):
        model = MagicMock()
        model.predict_proba.return_value = np.array([[0.3, 0.7], [0.6, 0.4]])
        adapter = SklearnModelAdapter(model)
        result = adapter.predict_proba(np.array([[1], [2]]))
        np.testing.assert_array_almost_equal(result, [0.7, 0.4])

    def test_predict_proba_multiclass(self):
        model = MagicMock()
        model.predict_proba.return_value = np.array([[0.1, 0.2, 0.7]])
        adapter = SklearnModelAdapter(model)
        result = adapter.predict_proba(np.array([[1]]))
        np.testing.assert_array_almost_equal(result, [[0.1, 0.2, 0.7]])

    def test_predict_proba_decision_function_fallback(self):
        model = MagicMock()
        del model.predict_proba  # no predict_proba
        model.decision_function.return_value = np.array([0.0])
        adapter = SklearnModelAdapter(model)
        result = adapter.predict_proba(np.array([[1]]))
        # sigmoid(0) = 0.5
        np.testing.assert_array_almost_equal(result, [0.5])

    def test_predict_proba_fallback_to_predict(self):
        model = MagicMock()
        del model.predict_proba
        del model.decision_function
        model.predict.return_value = np.array([1.0])
        adapter = SklearnModelAdapter(model)
        result = adapter.predict_proba(np.array([[1]]))
        np.testing.assert_array_almost_equal(result, [1.0])


class TestSklearnModelAdapterCoefficients:
    def test_get_coefficients_2d(self):
        model = MagicMock()
        model.coef_ = np.array([[0.1, 0.2, 0.3]])
        adapter = SklearnModelAdapter(model)
        coef = adapter.get_coefficients()
        np.testing.assert_array_equal(coef, [0.1, 0.2, 0.3])

    def test_get_coefficients_1d(self):
        model = MagicMock()
        model.coef_ = np.array([0.5, -0.5])
        adapter = SklearnModelAdapter(model)
        coef = adapter.get_coefficients()
        np.testing.assert_array_equal(coef, [0.5, -0.5])

    def test_get_coefficients_pipeline(self):
        final = MagicMock()
        final.coef_ = np.array([[0.4, 0.6]])
        model = MagicMock()
        del model.coef_
        model.steps = [("scaler", MagicMock()), ("clf", final)]
        adapter = SklearnModelAdapter(model)
        coef = adapter.get_coefficients()
        np.testing.assert_array_equal(coef, [0.4, 0.6])

    def test_get_coefficients_none(self):
        model = MagicMock()
        del model.coef_
        del model.steps
        adapter = SklearnModelAdapter(model)
        assert adapter.get_coefficients() is None


class TestSklearnModelAdapterFeatureImportance:
    def test_get_feature_importance_direct(self):
        model = MagicMock()
        model.feature_importances_ = np.array([0.2, 0.5, 0.3])
        adapter = SklearnModelAdapter(model)
        fi = adapter.get_feature_importance()
        np.testing.assert_array_equal(fi, [0.2, 0.5, 0.3])

    def test_get_feature_importance_pipeline(self):
        final = MagicMock()
        final.feature_importances_ = np.array([0.1, 0.9])
        model = MagicMock()
        del model.feature_importances_
        model.steps = [("prep", MagicMock()), ("clf", final)]
        adapter = SklearnModelAdapter(model)
        fi = adapter.get_feature_importance()
        np.testing.assert_array_equal(fi, [0.1, 0.9])

    def test_get_feature_importance_none(self):
        model = MagicMock()
        del model.feature_importances_
        del model.steps
        adapter = SklearnModelAdapter(model)
        assert adapter.get_feature_importance() is None


# ===========================================================================
# DatasetAdapter (ABC)
# ===========================================================================


class TestDatasetAdapterABC:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            DatasetAdapter()

    def test_default_validate_input(self):
        """Default validate_input returns (True, None)."""

        class Dummy(DatasetAdapter):
            def preprocess(self, raw_input):
                return np.zeros((1, 1))

            def get_feature_names(self):
                return ["f"]

            def get_feature_schema(self):
                return {}

        d = Dummy()
        is_valid, err = d.validate_input({"any": "thing"})
        assert is_valid is True
        assert err is None


# ===========================================================================
# GenericDatasetAdapter
# ===========================================================================


class TestGenericDatasetAdapter:
    @pytest.fixture()
    def schema(self):
        return {
            "features": [
                {"name": "age", "type": "numeric", "aliases": ["alter"], "default": 50},
                {
                    "name": "gender",
                    "type": "categorical",
                    "aliases": ["geschlecht"],
                    "default": "unknown",
                },
            ]
        }

    def test_preprocess_extracts_features(self, schema):
        adapter = GenericDatasetAdapter(schema)
        X = adapter.preprocess({"age": 30, "gender": "m"})
        assert X.shape == (1, 2)
        assert float(X[0, 0]) == 30.0

    def test_preprocess_uses_alias(self, schema):
        adapter = GenericDatasetAdapter(schema)
        X = adapter.preprocess({"alter": 25, "geschlecht": "f"})
        assert float(X[0, 0]) == 25.0

    def test_preprocess_uses_defaults(self, schema):
        adapter = GenericDatasetAdapter(schema)
        X = adapter.preprocess({})
        assert float(X[0, 0]) == 50.0  # default

    def test_get_feature_names(self, schema):
        adapter = GenericDatasetAdapter(schema)
        names = adapter.get_feature_names()
        assert names == ["age", "gender"]

    def test_get_feature_schema_returns_schema(self, schema):
        adapter = GenericDatasetAdapter(schema)
        assert adapter.get_feature_schema() is schema

    def test_preprocess_with_preprocessor(self, schema):
        mock_preprocessor = MagicMock()
        mock_preprocessor.transform.return_value = np.array([[0.5, 1.0]])
        adapter = GenericDatasetAdapter(schema, preprocessor=mock_preprocessor)
        X = adapter.preprocess({"age": 30, "gender": "m"})
        np.testing.assert_array_equal(X, [[0.5, 1.0]])
        mock_preprocessor.transform.assert_called_once()
