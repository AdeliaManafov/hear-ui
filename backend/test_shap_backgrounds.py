#!/usr/bin/env python3
"""Test SHAP TreeExplainer with different background strategies."""

import numpy as np
import shap
from app.core.model_wrapper import ModelWrapper
from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF

wrapper = ModelWrapper()
model = wrapper.model

# Test data
test_input = {
    'Alter [J]': 45,
    'Geschlecht': 'w',
    'Seiten': 'L',
    'Symptome präoperativ.Tinnitus...': 'Vorhanden',
    'outcome_measurments.pre.measure.': 30,
    'abstand': 1000,
}

preprocessed = wrapper.prepare_input(test_input)
print(f'Preprocessed: {preprocessed.flatten()[:10]}')

# Test 1: TreeExplainer without background (path-dependent)
print("\n=== Test 1: TreeExplainer without background ===")
try:
    explainer1 = shap.TreeExplainer(model)
    shap_values1 = explainer1.shap_values(preprocessed)
    print(f"Raw shape: {type(shap_values1)}")
    if isinstance(shap_values1, list):
        print(f"List len: {len(shap_values1)}, shapes: {[s.shape for s in shap_values1]}")
        vals1 = shap_values1[1][0] if len(shap_values1) > 1 else shap_values1[0][0]
    elif hasattr(shap_values1, 'ndim'):
        print(f"Array shape: {shap_values1.shape}")
        if shap_values1.ndim == 3:
            vals1 = shap_values1[0, :, 1] if shap_values1.shape[2] > 1 else shap_values1[0, :, 0]
        elif shap_values1.ndim == 2:
            vals1 = shap_values1[0]
        else:
            vals1 = shap_values1
    else:
        vals1 = np.array(shap_values1).flatten()
    
    pos1 = sum(1 for v in vals1 if float(v) > 0)
    neg1 = sum(1 for v in vals1 if float(v) < 0)
    print(f"Total: {len(vals1)}, positive: {pos1}, negative: {neg1}")
    sorted1 = sorted(zip(EXPECTED_FEATURES_RF, vals1), key=lambda x: abs(float(x[1])), reverse=True)[:10]
    for name, val in sorted1:
        val = float(val)
        sign = '+' if val > 0 else '-' if val < 0 else ' '
        print(f"  {sign}{abs(val):.4f}  {name}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()

# Test 2: TreeExplainer with zeros background
print("\n=== Test 2: TreeExplainer with zeros background ===")
try:
    background = np.zeros((1, 39))
    explainer2 = shap.TreeExplainer(model, data=background)
    shap_values2 = explainer2.shap_values(preprocessed)
    if isinstance(shap_values2, list):
        vals2 = shap_values2[1][0] if len(shap_values2) > 1 else shap_values2[0][0]
    else:
        vals2 = shap_values2[0] if shap_values2.ndim == 2 else shap_values2
    
    pos2 = sum(1 for v in vals2 if v > 0)
    neg2 = sum(1 for v in vals2 if v < 0)
    print(f"Total: {len(vals2)}, positive: {pos2}, negative: {neg2}")
    sorted2 = sorted(zip(EXPECTED_FEATURES_RF, vals2), key=lambda x: abs(x[1]), reverse=True)[:10]
    for name, val in sorted2:
        sign = '+' if val > 0 else '-' if val < 0 else ' '
        print(f"  {sign}{abs(val):.4f}  {name}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Compare with model's global feature_importances_
print("\n=== Test 3: Global feature_importances_ ===")
importances = model.feature_importances_
sorted3 = sorted(zip(EXPECTED_FEATURES_RF, importances), key=lambda x: x[1], reverse=True)[:10]
for name, val in sorted3:
    print(f"  {val:.4f}  {name}")
