
import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier

# Create model
np.random.seed(42)
X = np.random.randn(100, 3)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# Create background data
background_data = np.random.randn(20, 3)

# Initialize explainer
explainer = shap.TreeExplainer(model, data=background_data)

# Explain
sample = np.array([[1.0, 2.0, 3.0]])
shap_values = explainer.shap_values(sample)

print(f"Type of shap_values: {type(shap_values)}")
if isinstance(shap_values, list):
    print(f"List length: {len(shap_values)}")
    print(f"Element shape: {shap_values[0].shape}")
else:
    print(f"Array shape: {shap_values.shape}")
    print(f"Array ndim: {shap_values.ndim}")

# Check Explanation object API
try:
    explanation = explainer(sample)
    print(f"\nExplanation object values shape: {explanation.values.shape}")
except Exception as e:
    print(f"\nExplanation object API failed: {e}")
