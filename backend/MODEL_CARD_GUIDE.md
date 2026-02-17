# Model Card Documentation

## Where Does Model Card Information Come From?

The model card content is defined in **`backend/app/models/model_card/model_card.py`**.

### Current Implementation

**File:** [`backend/app/models/model_card/model_card.py`](backend/app/models/model_card/model_card.py)

The `load_model_card()` function (lines 40-152) returns a `ModelCard` object with:

```python
return ModelCard(
    name="HEAR CI Prediction Model",
    version="v1 (draft)",
    last_updated=datetime.now().strftime("%Y-%m-%d"),
    model_type=model_type,  # Auto-detected from wrapper
    model_path=model_path,
    features=features,      # Auto-loaded from EXPECTED_FEATURES
    metrics=ModelMetrics(), # Empty - metrics not displayed
    intended_use=[...],     # ← Edit here
    not_intended_for=[...], # ← Edit here
    limitations=[...],      # ← Edit here
    recommendations=[...],  # ← Edit here
    metadata=metadata,
)
```

### How to Change Model Card Content

#### 1. Intended Use (Lines 136-139)

```python
intended_use=[
    "Support clinicians estimating outcome probability",
    "Decision support tool for cochlear implant planning",
],
```

#### 2. Not Intended For (Lines 140-144)

```python
not_intended_for=[
    "Autonomous clinical decisions",
    "Use outside validated populations",
    "Legal or administrative decisions",
],
```

#### 3. Limitations (Lines 145-149)

```python
limitations=[
    "Model trained on limited dataset (N=137)",
    "Not validated outside training population",
    "Predictions should be interpreted as supportive evidence, not deterministic outcomes",
],
```

**✅ FIXED:** Removed incorrect statement "Performance depends on background dataset used for SHAP" 
- TreeExplainer operates in path-dependent mode and does NOT require a background dataset
- This was factually incorrect and has been removed

#### 4. Recommendations (Lines 150-154)

```python
recommendations=[
    "Use only as support tool",
    "Human medical judgment has priority",
    "Regular evaluation recommended",
],
```

### Metrics Handling

**Current State:** Metrics are **intentionally not displayed** in the model card.

- `metrics=ModelMetrics()` creates an empty metrics object (all values are `None`)
- The Markdown renderer in [`backend/app/api/routes/model_card.py`](backend/app/api/routes/model_card.py) **does not render metrics**
- The frontend [`PredictionsHome.vue`](frontend/src/routes/PredictionsHome.vue) displays the markdown without metrics

**✅ FIXED:** No empty "Model Metrics Recall" divs are shown in the current implementation.

**Legacy Issue:** The unused component [`ModelCard.vue`](frontend/src/components/ModelCard.vue) had a `<metrics-display>` reference that would show empty divs. This component is **not used** in the main UI.

---

## API Endpoints

### GET `/api/v1/model-card`

Returns the model card as plain Markdown text.

**Example:**
```bash
curl http://localhost:8000/api/v1/model-card
```

**Response:**
```markdown
# HEAR CI Prediction Model

**Version:** v1 (draft)
**Model type:** RandomForestClassifier
**Last updated:** 2026-02-17

---

## Intended use
- Support clinicians estimating outcome probability
- Decision support tool for cochlear implant planning

## Not intended for
- Autonomous clinical decisions
- Use outside validated populations
- Legal or administrative decisions

## Limitations
- Model trained on limited dataset (N=137)
- Not validated outside training population
- Predictions should be interpreted as supportive evidence, not deterministic outcomes

## Recommendations
- Use only as support tool
- Human medical judgment has priority
- Regular evaluation recommended

## Features
- **PID**
- **Alter [J]**
- **Geschlecht_m**
...
```

### GET `/api/v1/model-card/markdown`

Legacy endpoint that returns the markdown wrapped in JSON:

```json
{
  "markdown": "# HEAR CI Prediction Model\n\n**Version:** v1..."
}
```

---

## How to Update Model Card Content

### Step 1: Edit the Python File

Edit **`backend/app/models/model_card/model_card.py`**, lines 136-154:

```python
return ModelCard(
    name="HEAR CI Prediction Model",
    version="v1 (draft)",
    # ...
    intended_use=[
        "Your new intended use item 1",
        "Your new intended use item 2",
    ],
    limitations=[
        "Your new limitation 1",
        "Your new limitation 2",
    ],
    # ...
)
```

### Step 2: Rebuild Backend Container

```bash
cd /Users/adeliamanafov/hearUI_project/hear-ui
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml up -d --build backend
```

### Step 3: Verify Changes

```bash
curl http://localhost:8000/api/v1/model-card
```

Or open http://localhost:5173/prediction-home in your browser.

---

## Recent Fixes

### ✅ Fixed: Incorrect SHAP Statement (Feb 17, 2026)

**Issue:** "Performance depends on background dataset used for SHAP" was factually incorrect.

**Root Cause:** TreeExplainer operates in path-dependent mode and does NOT depend on background dataset.

**Fix:** Removed this limitation and replaced with accurate statements:
- "Model trained on limited dataset (N=137)"
- "Not validated outside training population"
- "Predictions should be interpreted as supportive evidence, not deterministic outcomes"

**File Changed:** `backend/app/models/model_card/model_card.py` lines 145-149

### ✅ Fixed: Empty Metrics Display

**Issue:** User reported seeing "Model Metrics Recall" with empty div (programming artifact).

**Root Cause:** Unused component `ModelCard.vue` referenced non-existent `<metrics-display>` component.

**Current State:** Main UI uses markdown rendering (PredictionsHome.vue) which does NOT show metrics. Empty metrics are not displayed.

**No Action Needed:** The current implementation is correct. The unused `ModelCard.vue` component is not imported anywhere.

---

## Versioned Model Cards (Advanced)

For managing multiple model versions with full history, see:
- **Implementation:** [`backend/app/models/model_card/versioned_model_card.py`](backend/app/models/model_card/versioned_model_card.py)
- **Demo:** [`backend/demo_model_card_versions.py`](backend/demo_model_card_versions.py)
- **Tests:** [`backend/app/tests/test_versioned_model_card.py`](backend/app/tests/test_versioned_model_card.py)

Example versioned cards are in `backend/app/config/model_cards/`:
- `v1_logreg_2025-11-15.json` (retired)
- `v2_randomforest_2026-01-20.json` (retired)
- `v3_randomforest_2026-02-17.json` (active)

---

## Summary

| Aspect | Current State | How to Change |
|--------|---------------|---------------|
| **Content Source** | `backend/app/models/model_card/model_card.py` | Edit lines 136-154, rebuild backend |
| **SHAP Statement** | ✅ Removed (was incorrect) | Already fixed |
| **Empty Metrics** | ✅ Not shown | Intentional - metrics object is empty |
| **API Endpoint** | `/api/v1/model-card` | Returns markdown text |
| **Frontend Display** | `PredictionsHome.vue` | Renders markdown, no metrics shown |

**Next Steps:**
1. To change content: Edit `model_card.py` → rebuild backend
2. To add metrics: Populate `ModelMetrics()` and update markdown renderer
3. To version model cards: Use `versioned_model_card.py` system
