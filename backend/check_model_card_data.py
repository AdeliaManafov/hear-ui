import os
import traceback
from app.models.model_card.model_card import load_model_card

def print_ok(k, v):
    print(f"{k}: {v}")

def check():
    print("=== Prüfe ModelCard-Daten ===")
    mc = load_model_card()

    # ----- Basic fields -----
    print_ok("Model name", mc.name)
    print_ok("Version", mc.version)
    print_ok("Last updated", mc.last_updated)
    print_ok("Model type", mc.model_type)
    print_ok("Model path exists", os.path.exists(mc.model_path) if mc.model_path else False)
    print_ok("Number of features", len(mc.features))

    # ----- Check SHAP / top features metadata -----
    if mc.metadata and "top_shap_features" in mc.metadata:
        print_ok("Top SHAP features vorhanden", True)
        for f in mc.metadata["top_shap_features"]:
            print(f"  {f['feature']}: importance={f['importance']}, value={f.get('value', 'n/a')}")
    else:
        print_ok("Top SHAP features vorhanden", False)

    # ----- Check EXPECTED_FEATURES availability -----
    try:
        from app.core.preprocessor import EXPECTED_FEATURES
        print_ok("EXPECTED_FEATURES importierbar", True)
        print_ok("Number of EXPECTED_FEATURES", len(EXPECTED_FEATURES))
        print_ok("Sample features", EXPECTED_FEATURES[:5])
    except Exception:
        print_ok("EXPECTED_FEATURES importierbar", False)
        traceback.print_exc()

    # ----- Manual fields -----
    print_ok("Metrics filled", mc.metrics is not None and any([
        mc.metrics.accuracy, mc.metrics.f1_score, mc.metrics.roc_auc
    ]))
    print_ok("Intended use", mc.intended_use)
    print_ok("Not intended for", mc.not_intended_for)
    print_ok("Limitations", mc.limitations)
    print_ok("Recommendations", mc.recommendations)

if __name__ == "__main__":
    check()