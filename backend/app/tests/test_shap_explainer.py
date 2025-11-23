"""Tests for SHAP explainer functionality."""

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.core.shap_explainer import ShapExplainer


@pytest.fixture
def simple_linear_model():
    """Create a simple linear model for testing."""
    # Create synthetic data
    np.random.seed(42)
    X = np.random.randn(100, 3)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # Train model
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    
    return model


@pytest.fixture
def pipeline_model():
    """Create a pipeline model for testing."""
    # Create synthetic data
    np.random.seed(42)
    X = np.random.randn(100, 3)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # Create pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(random_state=42)),
    ])
    
    pipeline.fit(X, y)
    
    return pipeline


def test_shap_explainer_initialization(simple_linear_model):
    """Test SHAP explainer can be initialized."""
    feature_names = ["feature_0", "feature_1", "feature_2"]
    explainer = ShapExplainer(
        model=simple_linear_model,
        feature_names=feature_names,
    )
    
    assert explainer.model is not None
    assert explainer.feature_names == feature_names
    assert explainer.explainer is not None


def test_shap_explainer_explain(simple_linear_model):
    """Test SHAP explainer can generate explanations."""
    feature_names = ["feature_0", "feature_1", "feature_2"]
    explainer = ShapExplainer(
        model=simple_linear_model,
        feature_names=feature_names,
    )
    
    # Create test sample
    sample = np.array([1.0, 2.0, 3.0])
    
    # Get explanation
    result = explainer.explain(sample, return_plot=False)
    
    # Verify structure
    assert "feature_importance" in result
    assert "shap_values" in result
    assert "base_value" in result
    
    # Verify feature importance has correct keys
    assert set(result["feature_importance"].keys()) == set(feature_names)
    
    # Verify SHAP values are numeric
    assert len(result["shap_values"]) == 3
    assert all(isinstance(v, float) for v in result["shap_values"])


def test_shap_explainer_top_features(simple_linear_model):
    """Test SHAP explainer can return top features."""
    feature_names = ["feature_0", "feature_1", "feature_2"]
    explainer = ShapExplainer(
        model=simple_linear_model,
        feature_names=feature_names,
    )
    
    # Create test sample
    sample = np.array([1.0, 2.0, 3.0])
    
    # Get top features
    top_features = explainer.get_top_features(sample, top_k=2)
    
    # Verify structure
    assert len(top_features) == 2
    assert all("feature" in f for f in top_features)
    assert all("importance" in f for f in top_features)
    
    # Verify sorted by absolute importance
    importances = [abs(f["importance"]) for f in top_features]
    assert importances == sorted(importances, reverse=True)


def test_shap_explainer_with_pipeline(pipeline_model):
    """Test SHAP explainer works with sklearn pipelines."""
    feature_names = ["feature_0", "feature_1", "feature_2"]
    
    # Create background data for KernelExplainer
    background = np.random.randn(10, 3)
    
    explainer = ShapExplainer(
        model=pipeline_model,
        background_data=background,
        feature_names=feature_names,
    )
    
    # Create test sample
    sample = np.array([1.0, 2.0, 3.0])
    
    # Get explanation
    result = explainer.explain(sample, return_plot=False)
    
    # Verify structure
    assert "feature_importance" in result
    assert "shap_values" in result
    assert len(result["shap_values"]) == 3


def test_shap_explainer_without_shap_library(simple_linear_model, monkeypatch):
    """Test SHAP explainer gracefully handles missing SHAP library."""
    # Mock shap import to fail
    import sys
    monkeypatch.setitem(sys.modules, "shap", None)
    
    feature_names = ["feature_0", "feature_1", "feature_2"]
    
    # This should not raise an error
    explainer = ShapExplainer(
        model=simple_linear_model,
        feature_names=feature_names,
    )
    
    # Explainer should be None
    assert explainer.explainer is None
    
    # Explain should return empty result
    sample = np.array([1.0, 2.0, 3.0])
    result = explainer.explain(sample)
    
    assert result["feature_importance"] == {}
    assert result["shap_values"] == []


def test_shap_explainer_2d_input(simple_linear_model):
    """Test SHAP explainer handles 2D input correctly."""
    feature_names = ["feature_0", "feature_1", "feature_2"]
    explainer = ShapExplainer(
        model=simple_linear_model,
        feature_names=feature_names,
    )
    
    # Create 2D test sample
    sample = np.array([[1.0, 2.0, 3.0]])
    
    # Get explanation
    result = explainer.explain(sample, return_plot=False)
    
    # Verify structure
    assert "feature_importance" in result
    assert len(result["shap_values"]) == 3
