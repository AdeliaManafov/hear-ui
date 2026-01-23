"""Tests for SHAP explainer module."""

from unittest.mock import MagicMock, patch

import numpy as np


class TestShapExplainerInit:
    """Test ShapExplainer initialization."""

    def test_init_without_shap_installed(self):
        """Test initialization when SHAP is not available."""
        with patch.dict("sys.modules", {"shap": None}):
            # Force reimport
            import importlib

            import app.core.shap_explainer as se

            importlib.reload(se)

            mock_model = MagicMock()
            explainer = se.ShapExplainer(mock_model)
            # Should not crash, just log warning

    def test_init_extracts_pipeline_components(self):
        """Test that init extracts preprocessor and final estimator from pipeline."""

        # Create mock pipeline with named_steps
        mock_preprocessor = MagicMock()
        mock_preprocessor.get_feature_names_out.return_value = [
            "feature_1",
            "feature_2",
        ]

        mock_estimator = MagicMock()
        mock_estimator.coef_ = np.array([[0.5, 0.3]])

        mock_pipeline = MagicMock()
        mock_pipeline.named_steps = {"preprocessor": mock_preprocessor}
        mock_pipeline.steps = [
            ("preprocessor", mock_preprocessor),
            ("classifier", mock_estimator),
        ]

        # Mock shap import in the module
        mock_shap = MagicMock()
        mock_shap.LinearExplainer.return_value = MagicMock()

        with patch.dict("sys.modules", {"shap": mock_shap}):
            with patch(
                "app.core.shap_explainer.ShapExplainer._init_transformed_explainer"
            ):
                with patch("app.core.shap_explainer.ShapExplainer._init_raw_explainer"):
                    # Force reimport to pick up the mock
                    import importlib

                    import app.core.shap_explainer as se

                    importlib.reload(se)

                    explainer = se.ShapExplainer(mock_pipeline)

                    # Verify components extracted
                    assert explainer._preprocessor == mock_preprocessor
                    assert explainer._final_estimator == mock_estimator

    def test_init_with_simple_model(self):
        """Test initialization with simple estimator (no pipeline)."""

        # Create mock model without named_steps attribute
        mock_model = MagicMock(spec=["predict", "predict_proba"])

        # Mock shap import
        mock_shap = MagicMock()
        mock_shap.KernelExplainer.return_value = MagicMock()

        with patch.dict("sys.modules", {"shap": mock_shap}):
            with patch(
                "app.core.shap_explainer.ShapExplainer._init_transformed_explainer"
            ):
                with patch("app.core.shap_explainer.ShapExplainer._init_raw_explainer"):
                    # Force reimport
                    import importlib

                    import app.core.shap_explainer as se

                    importlib.reload(se)

                    explainer = se.ShapExplainer(
                        mock_model, feature_names=["a", "b", "c"]
                    )

                    assert explainer.feature_names == ["a", "b", "c"]
                    assert explainer._final_estimator == mock_model


class TestShapExplainerMethods:
    """Test ShapExplainer methods."""

    def test_extract_feature_names_from_preprocessor(self):
        """Test feature name extraction from preprocessor."""
        from app.core.shap_explainer import ShapExplainer

        # Create an explainer instance without full init
        mock_model = MagicMock(spec=["predict"])

        with patch("app.core.shap_explainer.ShapExplainer._init_transformed_explainer"):
            with patch("app.core.shap_explainer.ShapExplainer._init_raw_explainer"):
                explainer = ShapExplainer(mock_model)

                # Set up mock preprocessor
                mock_preprocessor = MagicMock()
                mock_preprocessor.get_feature_names_out.return_value = [
                    "feat_1",
                    "feat_2",
                ]
                explainer._preprocessor = mock_preprocessor
                explainer.feature_names = None

                # Call extraction method
                names = explainer._extract_feature_names()

                assert names == ["feat_1", "feat_2"]

    def test_extract_feature_names_from_model(self):
        """Test feature name extraction from model.feature_names_in_."""
        from app.core.shap_explainer import ShapExplainer

        mock_model = MagicMock(spec=["predict", "feature_names_in_"])
        mock_model.feature_names_in_ = np.array(["col_a", "col_b"])

        with patch("app.core.shap_explainer.ShapExplainer._init_transformed_explainer"):
            with patch("app.core.shap_explainer.ShapExplainer._init_raw_explainer"):
                explainer = ShapExplainer(mock_model)
                explainer._preprocessor = None  # No preprocessor
                explainer.feature_names = None

                names = explainer._extract_feature_names()

                assert names == ["col_a", "col_b"]

    def test_get_top_features_empty_explanation(self):
        """Test get_top_features with empty explanation."""
        from app.core.shap_explainer import ShapExplainer

        mock_model = MagicMock(spec=["predict"])

        with patch("app.core.shap_explainer.ShapExplainer._init_transformed_explainer"):
            with patch("app.core.shap_explainer.ShapExplainer._init_raw_explainer"):
                explainer = ShapExplainer(mock_model)
                explainer.explainer = None  # Force empty explanation
                explainer._shap = None

        sample = np.array([[1, 2, 3]])
        result = explainer.get_top_features(sample, top_k=3)

        assert result == []

    def test_explain_returns_dict_structure(self):
        """Test explain returns correct dict structure."""
        from app.core.shap_explainer import ShapExplainer

        mock_model = MagicMock(spec=["predict"])

        with patch("app.core.shap_explainer.ShapExplainer._init_transformed_explainer"):
            with patch("app.core.shap_explainer.ShapExplainer._init_raw_explainer"):
                explainer = ShapExplainer(mock_model)
                explainer._shap = None  # No SHAP available

        sample = np.array([[1, 2, 3]])
        result = explainer.explain(sample)

        assert "feature_importance" in result
        assert "shap_values" in result
        assert "base_value" in result


class TestShapExplainerPlot:
    """Test SHAP plot generation."""

    # Note: Plot generation test removed - requires matplotlib which is optional
    pass
