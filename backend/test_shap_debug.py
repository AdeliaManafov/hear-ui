"""Quick SHAP explainer debug script."""
import numpy as np
from app.main import app
from app.core.shap_explainer import ShapExplainer
from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF

wrapper = app.state.model_wrapper
print(f"Model loaded: {wrapper.is_loaded()}")
print(f"Model type: {type(wrapper.model)}")

# Test with some patient data
test_input = {
    "Alter [J]": 55,
    "Geschlecht": "w",
    "Primäre Sprache": "Deutsch",
}

# Get preprocessed data
preprocessed = wrapper.prepare_input(test_input)
print(f"Preprocessed shape: {preprocessed.shape}")

# Initialize SHAP explainer
shap_explainer = ShapExplainer(
    model=wrapper.model,
    feature_names=EXPECTED_FEATURES_RF,
    use_transformed=True,
)

# Compute SHAP values
explanation = shap_explainer.explain(preprocessed, return_plot=False)

fi = explanation.get("feature_importance", {})
print(f"\nFeature importance count: {len(fi)}")
print(f"Positive values: {sum(1 for v in fi.values() if v > 0)}")
print(f"Negative values: {sum(1 for v in fi.values() if v < 0)}")
print(f"Zero values: {sum(1 for v in fi.values() if v == 0)}")

# Sort and show top 15
sorted_fi = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)[:15]
print("\nTop 15 features by absolute importance:")
for name, val in sorted_fi:
    sign = "+" if val > 0 else ("-" if val < 0 else " ")
    print(f"  {sign}{abs(val):.4f}  {name}")
