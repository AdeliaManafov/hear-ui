"""Small debug script to verify SHAP explanations for the saved pipeline.

Usage:
    python backend/scripts/debug_shap.py

This script will load `backend/app/models/logreg_best_pipeline.pkl`, build a
representative DataFrame using `model.feature_names_in_` (filling sensible
defaults), run a SHAP explainer (generic, then TreeExplainer fallback) and
save a numeric summary and a bar plot PNG.
"""

from pathlib import Path
import sys
import json

try:
    import joblib
    import pandas as pd
    import numpy as np
except Exception as e:
    print("Missing dependency:", e)
    sys.exit(1)

OUT = Path(__file__).parent.parent / "debug_shap_output"
OUT.mkdir(parents=True, exist_ok=True)
MODEL_PATH = Path(__file__).parent.parent / "app" / "models" / "logreg_best_pipeline.pkl"

if not MODEL_PATH.exists():
    print("Model file not found:", MODEL_PATH)
    sys.exit(1)

print("Loading model from", MODEL_PATH)
model = joblib.load(MODEL_PATH)
print("Model loaded. Type:", type(model))

# Build sample row using model.feature_names_in_ if available
fnames = getattr(model, "feature_names_in_", None)
if fnames is None:
    # fallback: try to infer from pipeline
    try:
        fnames = list(model.named_steps["preprocessor"].transformers_[0][2])
    except Exception:
        fnames = ["f0", "f1", "f2"]

row = {}
for f in fnames:
    low = f.lower()
    if "alter" in low or "age" in low:
        row[f] = 55
    elif "geschlecht" in low or "gender" in low:
        row[f] = "weiblich"
    elif "sprache" in low:
        row[f] = "de"
    elif "dauer" in low or "beginn" in low or "hör" in low:
        row[f] = 12
    elif "ursache" in low or "cause" in low:
        row[f] = "unklar"
    elif "tinnitus" in low:
        row[f] = False
    elif "implant" in low:
        row[f] = "type_b"
    else:
        row[f] = 0

df = pd.DataFrame([row])
print("Sample input:\n", df.T)

# Predict
try:
    if hasattr(model, "predict_proba"):
        pred = model.predict_proba(df)[:, 1]
    else:
        pred = model.predict(df)
    print("Prediction:", pred)
except Exception as e:
    print("Prediction failed:", e)

# SHAP
try:
    import shap

    print("Attempting shap.Explainer...")
    expl = shap.Explainer(model, df)
    vals = expl(df)
    # numeric summary
    try:
        arr = vals.values[0]
    except Exception:
        arr = vals[0]
    names = list(df.columns)
    summary = {n: float(v) for n, v in zip(names, arr)}
    print("SHAP numeric summary:", json.dumps(summary, indent=2, ensure_ascii=False))
    # plot
    try:
        import matplotlib.pyplot as plt

        shap.plots.bar(vals[0], show=False)
        out_png = OUT / "shap_bar.png"
        plt.savefig(out_png, bbox_inches="tight")
        plt.close()
        print("Saved SHAP bar plot to", out_png)
    except Exception as e:
        print("Failed to save SHAP plot:", e)

except Exception as e:
    print("shap.Explainer failed:", e)
    # Try TreeExplainer on final estimator
    try:
        final = model.steps[-1][1] if hasattr(model, "steps") else model
        if hasattr(final, "feature_importances_"):
            print("Attempting TreeExplainer on final estimator...")
            try:
                pre = getattr(model, "named_steps", {}).get("preprocessor")
                if pre is not None:
                    X_trans = pre.transform(df)
                    try:
                        fn = pre.get_feature_names_out()
                    except Exception:
                        fn = list(df.columns)
                else:
                    X_trans = df.values
                    fn = list(df.columns)

                import matplotlib.pyplot as plt
                import numpy as _np

                contrib = {fn[i]: float(final.feature_importances_[i] * float(X_trans[0, i])) for i in range(len(final.feature_importances_))}
                print("Feature-importance based contribs:", json.dumps(contrib, indent=2, ensure_ascii=False))

                # simple bar plot
                names = list(contrib.keys())
                vals = [contrib[n] for n in names]
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.barh(names, vals)
                ax.set_xlabel("Contribution")
                plt.tight_layout()
                out_png = OUT / "shap_tree_contribs.png"
                fig.savefig(out_png)
                plt.close()
                print("Saved feature-importance contrib plot to", out_png)
            except Exception as e2:
                print("TreeExplainer fallback failed:", e2)
    except Exception:
        print("No tree-based final estimator available or fallback failed.")

print("Done.")
