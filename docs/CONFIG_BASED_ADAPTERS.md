# Configuration-Based Dataset Adapters

## Overview

Instead of hardcoding feature engineering logic in Python classes, we now support **configuration-based dataset adapters** that define all feature specifications in JSON files.

## Benefits

✅ **Easy Model Swapping**: Change models without modifying code  
✅ **Auditable**: Feature definitions are version-controlled and reviewable  
✅ **No Code Changes**: Add/modify features by editing JSON, not Python  
✅ **Domain-Agnostic**: Works for any dataset/domain  
✅ **Reduces Bugs**: Single source of truth for feature specifications

## Quick Start

### 1. Define Features in JSON

Create a configuration file (e.g., `app/config/my_model_features.json`):

```json
{
  "model_name": "my_model",
  "features": [
    {
      "name": "age",
      "type": "numeric",
      "aliases": ["Alter", "Age [Y]"],
      "default": 50.0,
      "min": 0,
      "max": 120
    },
    {
      "name": "gender",
      "type": "categorical",
      "encoding": "label",
      "aliases": ["Geschlecht", "sex"],
      "mapping": {"male": 0, "female": 1, "diverse": 2},
      "default": 1
    },
    {
      "name": "has_symptom",
      "type": "binary",
      "aliases": ["symptom", "symptom_present"],
      "default": 0,
      "positive_values": ["yes", "ja", "1", "true"]
    }
  ]
}
```

### 2. Use Config-Based Adapter

```python
from app.core.model_wrapper import ModelWrapper

# Option A: Load via config file path
wrapper = ModelWrapper.from_config("app/config/random_forest_features.json")

# Option B: Manually create adapter
from app.core.config_based_adapter import load_dataset_adapter_from_config

adapter = load_dataset_adapter_from_config("app/config/random_forest_features.json")
wrapper = ModelWrapper(dataset_adapter=adapter)

# Use it
prediction = wrapper.predict({"age": 45, "gender": "female", "has_symptom": "yes"})
```

### 3. Swap Models

To use a different model with different features:

1. Create new config file: `app/config/new_model_features.json`
2. Set environment variables:
   ```bash
   export MODEL_PATH=/path/to/new_model.pkl
   export FEATURES_CONFIG=/path/to/new_model_features.json
   ```
3. No code changes needed!

## Feature Types

### Numeric Features

```json
{
  "name": "age",
  "type": "numeric",
  "aliases": ["Alter", "Age [Y]"],
  "default": 50.0,
  "min": 0,
  "max": 120
}
```

- **Type conversion**: Automatically converts to float
- **Bounds checking**: Clips values to [min, max] range
- **Aliases**: Multiple keys map to same feature

### Binary Features

```json
{
  "name": "has_tinnitus",
  "type": "binary",
  "aliases": ["tinnitus", "Tinnitus vorhanden"],
  "default": 0,
  "positive_values": ["yes", "ja", "1", "true", "vorhanden"]
}
```

- **Output**: 0.0 or 1.0
- **Positive values**: Configurable list of strings that map to 1.0
- **Case-insensitive**: "YES", "yes", "Yes" all work

### Categorical Features (Label Encoding)

```json
{
  "name": "diagnosis",
  "type": "categorical",
  "encoding": "label",
  "aliases": ["Diagnose", "diagnosis_type"],
  "mapping": {
    "Type A": 0,
    "Type B": 1,
    "Type C": 2,
    "Unknown": 3
  },
  "default": 3
}
```

- **Label encoding**: Maps categories to integers
- **Mapping**: Explicit category → integer dictionary
- **Unknown categories**: Fall back to default value

## Comparison: Hardcoded vs Config-Based

### ❌ Old Approach (Hardcoded)

```python
# rf_dataset_adapter.py (305 lines of hardcoded logic)
EXPECTED_FEATURES_RF = [
    "Geschlecht", "Alter [J]", ...  # 39 hardcoded features
]

CATEGORICAL_ENCODINGS = {
    "Geschlecht": {"m": 0, "w": 1, "d": 2},
    "Seiten": {"L": 0, "R": 1},
}

class RandomForestDatasetAdapter(DatasetAdapter):
    def preprocess(self, raw_input: dict) -> np.ndarray:
        features = {}
        features["Alter [J]"] = _safe_float(
            raw_input.get("Alter [J]", raw_input.get("alter", raw_input.get("age", 50))),
            50.0,
        )
        # ... 250 more lines of hardcoded logic
```

**Problems:**
- Code changes required for new features
- Domain knowledge scattered across Python files
- Difficult to audit feature specifications
- Hard to swap models

### ✅ New Approach (Config-Based)

```python
# Load adapter from config
wrapper = ModelWrapper.from_config("config/random_forest_features.json")
prediction = wrapper.predict(raw_patient_data)
```

**Benefits:**
- Single JSON file defines all features
- No Python code changes needed
- Easy to review and audit
- Model swapping = change config file

## Migration Guide

### Step 1: Export Existing Features to JSON

```python
# migration_script.py
import json
from app.core.rf_dataset_adapter import EXPECTED_FEATURES_RF, CATEGORICAL_ENCODINGS

# Convert to config format
config = {
    "model_name": "random_forest_final",
    "features": []
}

for feature_name in EXPECTED_FEATURES_RF:
    if feature_name in CATEGORICAL_ENCODINGS:
        config["features"].append({
            "name": feature_name,
            "type": "categorical",
            "encoding": "label",
            "mapping": CATEGORICAL_ENCODINGS[feature_name],
            "default": 0
        })
    else:
        config["features"].append({
            "name": feature_name,
            "type": "numeric",
            "default": 0.0
        })

# Save config
with open("config/random_forest_features.json", "w") as f:
    json.dump(config, indent=2)
```

### Step 2: Test Equivalence

```python
# Verify both adapters produce same output
hardcoded_adapter = RandomForestDatasetAdapter()
config_adapter = load_dataset_adapter_from_config("config/random_forest_features.json")

sample_input = {"Alter [J]": 45, "Geschlecht": "w", ...}

X_hardcoded = hardcoded_adapter.preprocess(sample_input)
X_config = config_adapter.preprocess(sample_input)

assert np.allclose(X_hardcoded, X_config), "Adapters should produce identical output"
```

### Step 3: Switch to Config-Based Adapter

```python
# OLD: app/main.py
model_wrapper = ModelWrapper()  # Uses hardcoded RandomForestDatasetAdapter

# NEW: app/main.py
model_wrapper = ModelWrapper.from_config("app/config/random_forest_features.json")
```

## Example: Adding a New Model

### Scenario: Switch from Random Forest to XGBoost

1. **Train new model with different features**
   ```python
   # Training script outputs: xgboost_model.pkl (50 features instead of 39)
   ```

2. **Create feature config**
   ```json
   // config/xgboost_features.json
   {
     "model_name": "xgboost_model",
     "features": [
       {"name": "age", "type": "numeric", "default": 50},
       {"name": "gender", "type": "categorical", "encoding": "label", "mapping": {"m": 0, "f": 1}},
       // ... 48 more features
     ]
   }
   ```

3. **Deploy with environment variables**
   ```bash
   export MODEL_PATH=/models/xgboost_model.pkl
   export FEATURES_CONFIG=/config/xgboost_features.json
   ```

4. **Update initialization code** (one-line change)
   ```python
   # app/main.py
   config_path = os.getenv("FEATURES_CONFIG", "app/config/random_forest_features.json")
   model_wrapper = ModelWrapper.from_config(config_path)
   ```

**Result**: Model swapped without changing feature engineering code!

## Testing

Run comprehensive test suite:

```bash
cd backend
pytest app/tests/test_config_based_adapter.py -v
```

Tests cover:
- ✅ Loading from config files
- ✅ Alias resolution
- ✅ Default value handling
- ✅ Binary feature encoding
- ✅ Categorical label encoding
- ✅ Numeric bounds checking
- ✅ Input validation
- ✅ Equivalence with hardcoded adapters

## Best Practices

### ✅ DO

- Use descriptive feature names that match training data
- Define comprehensive aliases for multilingual support
- Set sensible defaults for missing features
- Document feature sources and transformations in config
- Version control your feature configs
- Test config changes with existing test data

### ❌ DON'T

- Hardcode feature logic in Python classes anymore
- Mix feature definitions across multiple files
- Use ambiguous feature names without aliases
- Skip validation of config files before deployment
- Change feature order without retraining model

## Architecture Benefits

This config-based approach fulfills the **extensibility requirements**:

1. ✅ **Arbitrary XAI methods**: ExplainerInterface + Factory pattern
2. ✅ **Arbitrary model frameworks**: ModelAdapter (sklearn, PyTorch, TensorFlow, ONNX)
3. ✅ **Easy model swapping**: MODEL_PATH env var + config-based adapters
4. ✅ **Dataset flexibility**: Features defined in JSON, not hardcoded in Python

**Result**: True plug-and-play architecture for medical AI experimentation!

## Related Files

- `app/core/config_based_adapter.py` - ConfigBasedDatasetAdapter implementation
- `app/config/random_forest_features.json` - RF model feature config
- `app/tests/test_config_based_adapter.py` - Test suite
- `app/core/model_wrapper.py` - ModelWrapper.from_config() factory method

## Support

For questions or issues with config-based adapters, see:
- Test examples: `app/tests/test_config_based_adapter.py`
- Reference implementation: `app/core/config_based_adapter.py`
- Feature schema: `app/config/random_forest_features.json`
