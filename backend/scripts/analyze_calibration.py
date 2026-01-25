#!/usr/bin/env python3
"""Calibration analysis script for HEAR-UI model.

This script:
1. Analyzes preprocessor defaults and their impact
2. Loads sample patients and generates predictions
3. Creates calibration plots (if ground truth available)
4. Shows prediction distribution
5. Identifies which defaults are most influential
"""

import sys
from pathlib import Path

# Add backend to path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available, skipping plots")

import numpy as np
import pandas as pd

try:
    from sklearn.calibration import calibration_curve
    from sklearn.metrics import brier_score_loss
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: sklearn not available, skipping calibration metrics")

from app.core.model_wrapper import ModelWrapper
from app.core.preprocessor import EXPECTED_FEATURES, preprocess_patient_data


def analyze_preprocessor_defaults():
    """Extract and document all defaults from preprocessor."""
    print("=" * 80)
    print("PREPROCESSOR DEFAULTS ANALYSIS")
    print("=" * 80)
    
    defaults = {
        "PID": 0.0,
        "Alter [J]": 50.0,
        "Seiten": 1.0,
        "abstand": 365.0,
        "outcome_measurments.pre.measure.": 0.0,
        "All symptom fields": "0.0 (binary)",
        "Geschlecht": "w (female, one-hot)",
        "One-hot categories": "0.0 for all (no category selected)",
    }
    
    print("\nKey defaults that create baseline probability:")
    for key, value in defaults.items():
        print(f"  {key:45} = {value}")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("  - Age default (50) may bias predictions for younger/older patients")
    print("  - abstand default (365) assumes ~1 year follow-up")
    print("  - Pre-op score default (0) may inflate predictions")
    print("  - Many one-hot defaults mean 'unknown' category, which has learned coefficients")
    print()


def load_sample_data(csv_path: Path) -> pd.DataFrame:
    """Load sample patients CSV."""
    try:
        df = pd.read_csv(csv_path)
        print(f"\n✓ Loaded {len(df)} sample patients from {csv_path.name}")
        return df
    except FileNotFoundError:
        print(f"\n✗ Sample data not found: {csv_path}")
        return pd.DataFrame()


def analyze_prediction_distribution(wrapper: ModelWrapper, df: pd.DataFrame):
    """Generate predictions and analyze distribution."""
    print("\n" + "=" * 80)
    print("PREDICTION DISTRIBUTION ANALYSIS")
    print("=" * 80)
    
    predictions = []
    for idx, row in df.iterrows():
        patient_dict = row.to_dict()
        try:
            pred = wrapper.predict(patient_dict)
            pred_val = float(pred[0]) if hasattr(pred, '__len__') else float(pred)
            predictions.append(pred_val)
        except Exception as e:
            print(f"  Warning: Patient {idx} failed prediction: {e}")
            predictions.append(None)
    
    predictions = [p for p in predictions if p is not None]
    
    if not predictions:
        print("\n✗ No valid predictions generated")
        return None
    
    predictions = np.array(predictions)
    
    print(f"\nPredictions for {len(predictions)} patients:")
    print(f"  Min:     {predictions.min():.4f}")
    print(f"  Max:     {predictions.max():.4f}")
    print(f"  Mean:    {predictions.mean():.4f}")
    print(f"  Median:  {np.median(predictions):.4f}")
    print(f"  Std:     {predictions.std():.4f}")
    
    print("\nDistribution buckets:")
    buckets = [
        (0.0, 0.2, "Very low"),
        (0.2, 0.4, "Low"),
        (0.4, 0.6, "Medium"),
        (0.6, 0.8, "High"),
        (0.8, 1.0, "Very high"),
    ]
    for low, high, label in buckets:
        count = ((predictions >= low) & (predictions < high)).sum()
        if label == "Very high":  # include exact 1.0
            count = (predictions >= low).sum()
        pct = 100 * count / len(predictions)
        print(f"  [{low:.1f}-{high:.1f}] {label:12} : {count:3} ({pct:5.1f}%)")
    
    exact_one = (predictions == 1.0).sum()
    below_022 = (predictions < 0.22).sum()
    print(f"\n⚠️  Exact 1.0 values: {exact_one} ({100*exact_one/len(predictions):.1f}%)")
    print(f"⚠️  Below 0.22:       {below_022} ({100*below_022/len(predictions):.1f}%)")
    
    return predictions


def create_calibration_plot(predictions: np.ndarray, true_labels: np.ndarray = None):
    """Create calibration plot if ground truth available."""
    print("\n" + "=" * 80)
    print("CALIBRATION PLOT")
    print("=" * 80)
    
    if not HAS_SKLEARN or not HAS_MATPLOTLIB:
        print("\n⚠️  matplotlib or sklearn not available - skipping plot generation")
        if true_labels is not None:
            print(f"    Predictions available for {len(predictions)} samples")
            print(f"    True positive rate: {true_labels.mean():.1%}")
        return
    
    if true_labels is None:
        print("\n⚠️  No ground truth labels available - cannot create calibration curve")
        print("    To generate calibration plots, provide actual outcome labels")
        print("    (e.g., success=1, failure=0 based on post-op scores)")
        return
    
    # Create calibration curve
    prob_true, prob_pred = calibration_curve(
        true_labels, predictions, n_bins=10, strategy='uniform'
    )
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Calibration curve
    ax1.plot([0, 1], [0, 1], 'k--', label='Perfect calibration')
    ax1.plot(prob_pred, prob_true, 's-', label='Model calibration', markersize=8)
    ax1.set_xlabel('Mean predicted probability', fontsize=12)
    ax1.set_ylabel('Fraction of positives', fontsize=12)
    ax1.set_title('Calibration Curve (Reliability Diagram)', fontsize=14)
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Prediction histogram
    ax2.hist(predictions, bins=20, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Predicted probability', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    ax2.set_title('Prediction Distribution', fontsize=14)
    ax2.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = backend_root / "scripts" / "calibration_analysis.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Calibration plot saved to: {output_path}")
    
    # Calculate calibration metrics
    brier = brier_score_loss(true_labels, predictions)
    print(f"\nBrier Score: {brier:.4f} (lower is better, perfect = 0.0)")


def test_default_impact(wrapper: ModelWrapper):
    """Test how different default values affect predictions."""
    print("\n" + "=" * 80)
    print("DEFAULT VALUE IMPACT TEST")
    print("=" * 80)
    
    # Baseline: completely empty input (all defaults)
    baseline = wrapper.predict({})
    baseline_val = float(baseline[0]) if hasattr(baseline, '__len__') else float(baseline)
    print(f"\nBaseline (all defaults):     {baseline_val:.4f}")
    
    # Test varying key defaults
    tests = [
        ({"Alter [J]": 20}, "Age = 20 (vs default 50)"),
        ({"Alter [J]": 70}, "Age = 70 (vs default 50)"),
        ({"abstand": 90}, "Abstand = 90 (vs default 365)"),
        ({"abstand": 730}, "Abstand = 730 (vs default 365)"),
        ({"outcome_measurments.pre.measure.": 30}, "Pre-op score = 30 (vs default 0)"),
        ({"Geschlecht": "m"}, "Gender = male (vs default female)"),
        ({"Seiten": "R"}, "Side = right (vs default left)"),
    ]
    
    print("\nImpact of changing individual defaults:")
    for patient_dict, description in tests:
        pred = wrapper.predict(patient_dict)
        pred_val = float(pred[0]) if hasattr(pred, '__len__') else float(pred)
        delta = pred_val - baseline_val
        sign = "+" if delta >= 0 else ""
        print(f"  {description:40} → {pred_val:.4f} ({sign}{delta:.4f})")


def main():
    """Run complete calibration analysis."""
    print("\n" + "=" * 80)
    print("HEAR-UI MODEL CALIBRATION & DEFAULT ANALYSIS")
    print("=" * 80)
    
    # 1. Analyze defaults
    analyze_preprocessor_defaults()
    
    # 2. Load model
    print("\nLoading model...")
    wrapper = ModelWrapper()
    if not wrapper.is_loaded():
        print("✗ Model failed to load. Cannot continue analysis.")
        return 1
    print("✓ Model loaded successfully")
    
    # 3. Test default impact
    test_default_impact(wrapper)
    
    # 4. Load sample data
    sample_csv = backend_root.parent / "patientsData" / "sample_patients.csv"
    df = load_sample_data(sample_csv)
    
    if df.empty:
        print("\n⚠️  No sample data available. Skipping distribution analysis.")
        return 0
    
    # 5. Analyze prediction distribution
    predictions = analyze_prediction_distribution(wrapper, df)
    
    # 6. Create calibration plot (if ground truth available)
    # Note: sample_patients.csv has post24 and post12 measures - we can derive labels
    if predictions is not None and 'outcome_measurments.post24.measure.' in df.columns:
        print("\n" + "=" * 80)
        print("GENERATING GROUND TRUTH LABELS")
        print("=" * 80)
        
        # Define success: post24 score > pre score (or use threshold)
        df['pre_score'] = df.get('outcome_measurments.pre.measure.', 0)
        df['post24_score'] = df.get('outcome_measurments.post24.measure.', 0)
        
        # Success = improvement (post > pre)
        df['success'] = (df['post24_score'] > df['pre_score']).astype(int)
        
        # Filter valid rows (where we have predictions and labels)
        valid_mask = ~df['post24_score'].isna() & ~df['pre_score'].isna()
        valid_predictions = predictions[:sum(valid_mask)]
        true_labels = df.loc[valid_mask, 'success'].values[:len(valid_predictions)]
        
        if len(valid_predictions) > 0:
            print(f"\n✓ Using post24 > pre as success criterion")
            print(f"  Total valid samples: {len(valid_predictions)}")
            print(f"  Success rate: {true_labels.mean():.1%}")
            create_calibration_plot(valid_predictions, true_labels)
        else:
            create_calibration_plot(predictions, None)
    else:
        create_calibration_plot(predictions, None)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nKey findings:")
    print("  1. Check prediction distribution - are many predictions at 1.0?")
    print("  2. Check calibration curve - does it match diagonal?")
    print("  3. Review defaults - do they create unrealistic baseline (0.22)?")
    print("\nRecommendations:")
    print("  • Consider CalibratedClassifierCV for better probability estimates")
    print("  • Review and adjust preprocessor defaults based on clinical input")
    print("  • Add confidence intervals to predictions")
    print("  • Document which fields are optional vs required\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
