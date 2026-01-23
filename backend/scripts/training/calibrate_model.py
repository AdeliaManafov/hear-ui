"""Calibrate an already trained model using Isotonic Regression.

This fixes overconfident/underconfident predictions.
"""

import joblib
import numpy as np
import pandas as pd
import sys
from pathlib import Path
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

# Add backend to path to import CalibratedRegressor
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.core.calibrated_regressor import CalibratedRegressor


def calibrate_model(
    model_path: str,
    training_csv: str,
    output_path: str = None,
    method: str = 'isotonic',
    test_size: float = 0.3
):
    """Calibrate a trained model.
    
    Args:
        model_path: Path to trained pipeline
        training_csv: Path to training data with 'Erfolg' column
        output_path: Where to save calibrated model
        method: 'isotonic' or 'sigmoid' (Platt scaling)
        test_size: Fraction to use for calibration
    """
    print("🔧 MODEL CALIBRATION")
    print("="*70)
    
    # Load model
    print("\n📂 Loading model...")
    pipeline = joblib.load(model_path)
    print(f"   [OK] Loaded: {Path(model_path).name}")
    
    # Load data
    print("\n📂 Loading training data...")
    df = pd.read_csv(training_csv)
    y = df['Erfolg'].values
    X = df.drop(columns=['Erfolg'])
    print(f"   [OK] Loaded {len(df)} patients")
    print(f"   [STATS] Success rate: {y.mean():.1%}")
    
    # Split for calibration
    print(f"\n🔀 Splitting data (calibration set: {test_size:.0%})...")
    X_train, X_cal, y_train, y_cal = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Check if model needs wrapping for CalibratedClassifierCV
    print(f"\n⚙️  Calibrating with {method.upper()} method...")
    print("   (This may take a minute...)")
    
    # For regressors, we need a custom wrapper
    try:
        # Try direct calibration (works for classifiers)
        calibrated = CalibratedClassifierCV(
            pipeline,
            method=method,
            cv='prefit'  # Use already fitted model
        )
        calibrated.fit(X_cal, y_cal)
    except Exception as e:
        print(f"   [WARN]  Direct calibration failed: {e}")
        print("   🔄 Using alternative approach for regressors...")
        
        # For regressors: use isotonic regression manually
        from sklearn.isotonic import IsotonicRegression
        
        # Get predictions from base model
        base_preds = np.clip(pipeline.predict(X_cal), 0, 1)
        
        # Fit isotonic regression to map predictions → true probabilities
        iso_reg = IsotonicRegression(out_of_bounds='clip')
        iso_reg.fit(base_preds, y_cal)
        
        # Create calibrated wrapper
        calibrated = CalibratedRegressor(pipeline, iso_reg)
    
    print("   [OK] Calibration complete!")
    
    # Evaluate improvement
    print("\n[STATS] Evaluating improvement...")
    
    # Before calibration
    try:
        y_pred_before = np.clip(pipeline.predict(X_cal), 0, 1)
    except AttributeError:
        y_pred_before = pipeline.predict_proba(X_cal)[:, 1]
    
    # After calibration
    try:
        y_pred_after = calibrated.predict(X_cal)
    except AttributeError:
        y_pred_after = calibrated.predict_proba(X_cal)[:, 1]
    
    from sklearn.calibration import calibration_curve
    from sklearn.metrics import brier_score_loss
    
    # Before
    brier_before = brier_score_loss(y_cal, y_pred_before)
    frac_pos_before, mean_pred_before = calibration_curve(y_cal, y_pred_before, n_bins=5)
    ece_before = np.mean(np.abs(frac_pos_before - mean_pred_before))
    
    # After
    brier_after = brier_score_loss(y_cal, y_pred_after)
    frac_pos_after, mean_pred_after = calibration_curve(y_cal, y_pred_after, n_bins=5)
    ece_after = np.mean(np.abs(frac_pos_after - mean_pred_after))
    
    print("\n" + "="*70)
    print("BEFORE vs AFTER CALIBRATION".center(70))
    print("="*70)
    print(f"{'Metric':<30} | Before    | After     | Change")
    print("-"*70)
    print(f"{'Brier Score (lower=better)':<30} | {brier_before:8.4f}  | {brier_after:8.4f}  | {brier_after-brier_before:+.4f}")
    print(f"{'ECE (lower=better)':<30} | {ece_before:8.4f}  | {ece_after:8.4f}  | {ece_after-ece_before:+.4f}")
    
    improvement = (ece_before - ece_after) / ece_before * 100
    print(f"\n🎯 Calibration Improvement: {improvement:+.1f}%")
    
    if ece_after < 0.05:
        print("[OK] EXZELLENT! Kalibrierung ist perfekt.")
    elif ece_after < 0.1:
        print("[OK] GUT! Kalibrierung ist zuverlässig.")
    elif ece_after < ece_before:
        print("[WARN]  BESSER, aber noch Raum für Verbesserung.")
    else:
        print("[FAIL] Kalibrierung hat nicht geholfen. Mehr Daten nötig.")
    
    # Save
    if output_path is None:
        output_path = model_path.replace('.pkl', '_calibrated.pkl')
    
    print(f"\n💾 Saving calibrated model...")
    joblib.dump(calibrated, output_path)
    print(f"   [OK] Saved to: {output_path}")
    
    print("\n" + "="*70)
    print("[SUCCESS] CALIBRATION COMPLETE!")
    print("="*70)
    print(f"\n📝 To use the calibrated model:")
    print(f"   1. Update MODEL_PATH in model_wrapper.py:")
    print(f"      MODEL_PATH = '{output_path}'")
    print(f"   2. Restart backend")
    print(f"   3. Test predictions - they should be more reliable now!")
    
    return calibrated


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python calibrate_model.py <model_path> <training_csv> [output_path] [method]")
        print("\nExample:")
        print("  python backend/scripts/calibrate_model.py \\")
        print("         backend/app/models/logreg_best_pipeline.pkl \\")
        print("         data/test_patients_synthetic.csv \\")
        print("         backend/app/models/logreg_calibrated.pkl \\")
        print("         isotonic")
        print("\nMethod: 'isotonic' (default) or 'sigmoid'")
        sys.exit(1)
    
    model_path = sys.argv[1]
    training_csv = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    method = sys.argv[4] if len(sys.argv) > 4 else 'isotonic'
    
    calibrate_model(model_path, training_csv, output_path, method)
