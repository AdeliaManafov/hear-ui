#!/usr/bin/env python3
"""Small utility to inspect the serialized model at MODEL_PATH.

Run:
    python backend/scripts/check_model.py

It will try joblib then pickle, print model type and attributes to help decide next steps.
"""
import os
import sys
import pickle

MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "..", "backend", "app", "models", "logreg_best_model.pkl"),
)
# The above default path mirrors earlier code but may not match your layout; set MODEL_PATH env var if needed.

try:
    import joblib
except Exception:
    joblib = None


def load_model(path):
    if not os.path.exists(path):
        print(f"Model file not found: {path}")
        sys.exit(2)
    if joblib is not None:
        try:
            m = joblib.load(path)
            print("Loaded model with joblib")
            return m
        except Exception:
            pass
    with open(path, "rb") as f:
        m = pickle.load(f)
        print("Loaded model with pickle")
        return m


def main():
    print(f"Inspecting model at: {MODEL_PATH}")
    model = load_model(MODEL_PATH)
    print("Model type:", type(model))
    # Common sklearn attrs
    for attr in ("n_features_in_", "feature_names_in_", "coef_", "classes_"):
        if hasattr(model, attr):
            print(f"- {attr}:", getattr(model, attr))
    # If it's a pipeline, inspect steps
    try:
        from sklearn.pipeline import Pipeline

        if isinstance(model, Pipeline):
            print("This is a Pipeline. Steps:")
            for name, step in model.steps:
                print(f"  - {name}: {type(step)}")
    except Exception:
        pass

    print("\nRecommendation:")
    print("- If the model expects many features, save a Pipeline that includes preprocessing, e.g.:\n  joblib.dump(pipeline, 'logreg_best_pipeline.pkl')\n  and place it in backend/app/models/ or set MODEL_PATH to it.")
    print("- If you only have an estimator trained for 3 features, replace the model file with that estimator so it matches your `preprocess_patient_data` output.")


if __name__ == '__main__':
    main()
