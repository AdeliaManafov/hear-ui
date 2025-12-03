# Model Configuration and Deployment Guide

## Model Path Configuration

### Environment Variable: `MODEL_PATH`

The backend loads the ML model from a configurable path specified by the `MODEL_PATH` environment variable.

**Default:** `app/models/logreg_best_model.pkl`

**Usage:**
```bash
# Local development
export MODEL_PATH=/path/to/your/model.pkl

# Docker
docker run -e MODEL_PATH=/app/models/custom_model.pkl ...

# Docker Compose
environment:
  - MODEL_PATH=/app/models/custom_model.pkl
```

### Supported Model Formats

The `ModelWrapper` supports models saved with:
1. **joblib** (recommended): `joblib.dump(model, 'model.pkl')`
2. **pickle** (fallback): `pickle.dump(model, file)`

### Best Practices for Production

#### 1. Use Pipeline Objects

**Recommended:** Save a complete `sklearn.pipeline.Pipeline` that includes preprocessing:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Create pipeline
pipeline = Pipeline([
    ('preprocessor', your_preprocessor),
    ('classifier', LogisticRegression())
])

# Train
pipeline.fit(X_train, y_train)

# Save with joblib (preferred over pickle)
joblib.dump(pipeline, 'logreg_best_pipeline.pkl')
```

**Why?** A pipeline ensures preprocessing and model are versioned together, reducing feature mismatch errors.

#### 2. Feature Compatibility

The current model expects **68 features** after preprocessing (see `app/core/preprocessor.py` for the complete list).

**Critical:** If you update the model or preprocessing:
- Update `EXPECTED_FEATURES` in `preprocessor.py`
- Ensure the model's `n_features_in_` matches
- Test with `ModelWrapper.prepare_input()` before deployment

#### 3. Model Versioning

For production deployments:

```bash
# Tag models with version/date
MODEL_PATH=/app/models/logreg_v1.2_2025-12-03.pkl

# Or use volume mounts for external model storage
docker run -v /data/models:/models \
  -e MODEL_PATH=/models/production_model.pkl \
  backend:latest
```

#### 4. Model Updates Without Redeployment

**Option A: Volume Mount** (Docker)
```yaml
# docker-compose.yml
services:
  backend:
    volumes:
      - ./models:/app/models:ro  # read-only mount
    environment:
      - MODEL_PATH=/app/models/current_model.pkl
```

Update the model by replacing the file; restart the backend container.

**Option B: Cloud Storage** (S3, GCS, Azure Blob)
```python
# In model_wrapper.py, add download logic:
import boto3

if MODEL_PATH.startswith('s3://'):
    s3 = boto3.client('s3')
    bucket, key = parse_s3_path(MODEL_PATH)
    s3.download_file(bucket, key, '/tmp/model.pkl')
    MODEL_PATH = '/tmp/model.pkl'
```

#### 5. Validation on Startup

The backend validates model loading during startup (`main.py` lifespan):

```python
# main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model_wrapper.load()
        app.state.model_wrapper = model_wrapper
    except FileNotFoundError:
        logger.error("Model file not found: %s", MODEL_PATH)
        # App continues but prediction endpoints will fail
```

**Recommendation:** Add health checks that verify model is loaded:
```python
@router.get("/health-check/")
def health_check():
    model_ok = model_wrapper.is_loaded()
    return {
        "status": "ok" if model_ok else "degraded",
        "model_loaded": model_ok
    }
```

### Troubleshooting

#### Error: `Model file not found`
- Check `MODEL_PATH` is set correctly
- Verify file exists in container: `docker exec backend ls -la /app/models/`
- Check volume mounts in `docker-compose.yml`

#### Error: `Feature shape mismatch`
- Model expects different number of features than preprocessor provides
- Solution: Ensure model was trained with same preprocessing pipeline
- Use `model.n_features_in_` to check expected count

#### Error: `Module not found` or pickle errors
- Model was saved with different Python/library versions
- Solution: Re-train and save model in same environment as backend
- Use `joblib` (more robust across versions) instead of `pickle`

## SHAP Configuration

### Background Data for SHAP

**Environment Variable:** `SHAP_BACKGROUND_FILE`

**Default:** `app/models/background_sample.csv`

SHAP explainers require background/reference data. You can:

1. **Use synthetic data** (default): `app/core/background_data.py` generates representative samples
2. **Provide real data**: Set `SHAP_BACKGROUND_FILE` to a CSV with real patient examples

```bash
export SHAP_BACKGROUND_FILE=/app/data/background_patients.csv
```

**Format:** CSV with same columns as training data (German column names).

### SHAP Dependencies

SHAP requires:
- `shap>=0.41.0`
- `matplotlib>=3.7.0` (for plots)
- `numpy`, `pandas`, `scikit-learn`

All are included in `requirements.txt` and installed in CI.

### Disabling SHAP (Fallback Mode)

If SHAP is unavailable or fails, the explainer falls back to:
1. Coefficient-based importance (for linear models)
2. Empty explanations with error logged

Test this with:
```python
# In tests, mock SHAP failure
with patch('app.core.shap_explainer.shap', None):
    # Explainer should still return structure
```

## Testing with Real Models

### Local Testing

```bash
cd backend

# Set model path
export MODEL_PATH=app/models/logreg_best_model.pkl

# Run tests
pytest app/api/tests/

# Test with coverage
pytest --cov=app --cov-report=html
```

### CI Testing

GitHub Actions workflow installs all dependencies including SHAP:

```yaml
# .github/workflows/test-backend.yml
- name: Install dependencies
  run: |
    pip install -r backend/requirements.txt
    pip install shap matplotlib scikit-learn
```

### Integration Testing

Test model loading in container:

```bash
docker-compose build backend
docker-compose run --rm backend python -c "
from app.core.model_wrapper import ModelWrapper
wrapper = ModelWrapper()
wrapper.load()
print(f'Model loaded: {wrapper.is_loaded()}')
print(f'Model type: {type(wrapper.model)}')
"
```

## Security Considerations

1. **Model File Permissions**: In production, mount models as read-only
2. **Path Traversal**: `MODEL_PATH` should be validated/sanitized if user-configurable
3. **Model Provenance**: Track model versions, training dates, and validation metrics
4. **Audit Trail**: Log model loads and updates for compliance

## Performance Optimization

### Model Loading
- Model is loaded once at startup (singleton pattern)
- Use `joblib` for faster loading of large models
- Consider model compression for deployment

### Prediction Performance
- Batch predictions are more efficient than single predictions
- Use `/patients/upload` endpoint for bulk processing
- Consider caching frequent predictions (with expiry)

### SHAP Performance
- SHAP can be slow for complex models
- Use smaller background datasets (50-100 samples)
- Consider pre-computing SHAP values for common patient profiles
- Use `TreeExplainer` (fastest) for tree-based models
- Use `LinearExplainer` for linear models (fast and exact)
- Avoid `KernelExplainer` in production (slow)

## Monitoring

### Metrics to Track

1. **Model Health**
   - Model load success/failure rate
   - Prediction endpoint response time
   - Prediction error rate

2. **Model Performance**
   - Prediction distribution (detect drift)
   - Feature value distributions
   - Feedback accept/reject ratio

3. **System Health**
   - Memory usage (SHAP can be memory-intensive)
   - CPU usage during predictions
   - Database connection pool status

### Example Monitoring Setup

```python
# Add to main.py
from prometheus_client import Counter, Histogram

prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration')

@router.post("/predict/")
def predict(...):
    with prediction_duration.time():
        result = model_wrapper.predict(...)
    prediction_counter.inc()
    return result
```

## Migration Guide

### Updating to New Model Version

1. Train and validate new model
2. Save as pipeline with `joblib.dump()`
3. Test locally:
   ```bash
   export MODEL_PATH=/path/to/new_model.pkl
   pytest app/api/tests/test_predict.py
   ```
4. Update `MODEL_PATH` in deployment config
5. Rolling deployment:
   - Deploy to staging first
   - Run integration tests
   - Compare predictions between old/new model
   - Gradual rollout with monitoring

### Updating Preprocessing

If you change `preprocessor.py`:

1. Update `EXPECTED_FEATURES` list
2. Retrain model with new preprocessing
3. Update tests in `test_predict_batch.py`
4. Deploy preprocessing and model together
5. Update API documentation for any new input fields

## Additional Resources

- [scikit-learn Pipeline documentation](https://scikit-learn.org/stable/modules/compose.html)
- [SHAP documentation](https://shap.readthedocs.io/)
- [FastAPI deployment best practices](https://fastapi.tiangolo.com/deployment/)
- Backend README: `backend/README.md`
- Dependency management: `backend/README-DEPS.md`
