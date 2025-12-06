"""Export a compatible sklearn pipeline for the HEAR project.

This script creates a simple logistic regression pipeline with preprocessing
that is compatible with sklearn 1.6.1 and can be loaded in the backend.

Usage:
    python scripts/export_pipeline.py
"""

import sys
from pathlib import Path

# Add app to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def create_pipeline():
    """Create a simple pipeline for CI implant success prediction.
    
    Features:
    - age: numeric (scaled)
    - hearing_loss_duration: numeric (scaled)
    - implant_type: categorical (one-hot encoded)
    
    Returns:
        Pipeline: Trained sklearn pipeline
    """
    # Define preprocessing for numeric and categorical features
    numeric_features = ["age", "hearing_loss_duration"]
    categorical_features = ["implant_type"]
    
    # Create preprocessing pipelines
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(
        drop="first",  # Avoid multicollinearity
        sparse_output=False,
        handle_unknown="ignore",
    )
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    
    # Create full pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(random_state=42, max_iter=1000)),
        ]
    )
    
    return pipeline


def create_dummy_training_data():
    """Create dummy training data for demonstration.
    
    Returns:
        tuple: (X, y) where X is feature dict and y is target
    """
    import pandas as pd
    
    # Create synthetic training data
    np.random.seed(42)
    n_samples = 100
    
    data = {
        "age": np.random.randint(30, 80, n_samples),
        "hearing_loss_duration": np.random.uniform(1, 20, n_samples),
        "implant_type": np.random.choice(["type_a", "type_b", "type_c"], n_samples),
    }
    
    X = pd.DataFrame(data)
    
    # Create synthetic target (success probability based on features)
    # Younger age, shorter duration, type_a -> higher success
    y = (
        (X["age"] < 60).astype(int)
        + (X["hearing_loss_duration"] < 10).astype(int)
        + (X["implant_type"] == "type_a").astype(int)
    )
    y = (y >= 2).astype(int)  # Binary classification
    
    return X, y


def main():
    """Main function to create and export pipeline."""
    print("=" * 60)
    print("HEAR Pipeline Export Script")
    print("=" * 60)
    
    # Check sklearn version
    import sklearn
    print(f"\n✓ Using scikit-learn version: {sklearn.__version__}")
    
    # Create pipeline
    print("\n1. Creating pipeline...")
    pipeline = create_pipeline()
    print("   ✓ Pipeline created")
    
    # Create dummy training data
    print("\n2. Creating dummy training data...")
    X, y = create_dummy_training_data()
    print(f"   ✓ Created {len(X)} training samples")
    
    # Train pipeline
    print("\n3. Training pipeline...")
    pipeline.fit(X, y)
    print("   ✓ Pipeline trained")
    
    # Verify pipeline works
    print("\n4. Verifying pipeline...")
    test_sample = {
        "age": 65,
        "hearing_loss_duration": 5.5,
        "implant_type": "type_a",
    }
    import pandas as pd
    test_df = pd.DataFrame([test_sample])
    
    prediction = pipeline.predict_proba(test_df)
    print(f"   ✓ Test prediction: {prediction[0][1]:.3f}")
    
    # Export pipeline
    output_path = Path(__file__).parent.parent / "app" / "models" / "logreg_best_pipeline.pkl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n5. Exporting pipeline to: {output_path}")
    dump(pipeline, output_path)
    print("   ✓ Pipeline exported successfully")
    
    # Print pipeline info
    print("\n" + "=" * 60)
    print("Pipeline Information:")
    print("=" * 60)
    print(f"Input features: {pipeline.feature_names_in_.tolist()}")
    print(f"Number of features after preprocessing: {pipeline.n_features_in_}")
    
    # Get feature names after preprocessing
    preprocessor = pipeline.named_steps["preprocessor"]
    feature_names = (
        preprocessor.transformers_[0][2]  # numeric features
        + preprocessor.transformers_[1][1]
        .get_feature_names_out(preprocessor.transformers_[1][2])
        .tolist()  # categorical features
    )
    print(f"Feature names after preprocessing: {feature_names}")
    
    print("\n✓ Pipeline export complete!")
    print("\nNext steps:")
    print("1. Rebuild backend: docker-compose build backend")
    print("2. Restart containers: docker-compose up -d")
    print("3. Test endpoint: curl http://localhost:8000/api/v1/utils/model-info/")
    print("=" * 60)


if __name__ == "__main__":
    main()
