#!/usr/bin/env python3
"""Test SHAP explanation with varied data."""

import numpy as np
from app.core.model_wrapper import ModelWrapper
from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF
from app.core.shap_explainer import ShapExplainer

wrapper = ModelWrapper()

# Test data with more variety
test_input = {
    'Alter [J]': 45,
    'Geschlecht': 'w',
    'Seiten': 'L',
    'Symptome präoperativ.Tinnitus...': 'Vorhanden',
    'Symptome präoperativ.Schwindel...': 'Stark',
    'outcome_measurments.pre.measure.': 30,
    'abstand': 1000,
}

preprocessed = wrapper.prepare_input(test_input)
print(f'Preprocessed shape: {preprocessed.shape}')
print(f'Preprocessed values: {preprocessed.flatten()[:10]}')

shap_explainer = ShapExplainer(
    model=wrapper.model,
    feature_names=EXPECTED_FEATURES_RF,
    use_transformed=True,
)

result = shap_explainer.explain(preprocessed, return_plot=False)
fi = result.get('feature_importance', {})

positive = sum(1 for v in fi.values() if v > 0)
negative = sum(1 for v in fi.values() if v < 0)
print(f'\nTotal: {len(fi)}, positive: {positive}, negative: {negative}')

sorted_fi = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)[:15]
print('\nTop 15 features:')
for name, val in sorted_fi:
    sign = '+' if val > 0 else '-' if val < 0 else ' '
    print(f'  {sign}{abs(val):.4f}  {name}')
