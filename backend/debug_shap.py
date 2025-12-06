"""Debug SHAP initialization issues."""
import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Set logging to see what's happening
logging.basicConfig(level=logging.DEBUG)

from app.core.shap_explainer import ShapExplainer

# Create model
np.random.seed(42)
X = np.random.randn(100, 3)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# Create background data
background_data = np.random.randn(20, 3)

# Try to initialize
feature_names = ["feature_0", "feature_1", "feature_2"]
explainer = ShapExplainer(
    model=model,
    feature_names=feature_names,
    background_data=background_data,
    use_transformed=False,
)

print(f"\nExplainer object: {explainer.explainer}")
print(f"Model: {explainer.model}")
print(f"Feature names: {explainer.feature_names}")
print(f"Has feature_importances_: {hasattr(model, 'feature_importances_')}")

# Try to get explanation
sample = np.array([1.0, 2.0, 3.0])
result = explainer.explain(sample, return_plot=False)
print(f"\nResult keys: {result.keys()}")
print(f"Feature importance: {result['feature_importance']}")
print(f"SHAP values: {result['shap_values']}")
