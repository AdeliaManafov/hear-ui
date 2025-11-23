"""Train a model based on the real clinical data structure.

This script mimics the structure of 'Dummy Data_Cochlear Implant.xlsx'
to train a compatible pipeline.
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def create_dummy_data(n_samples=200):
    """Create synthetic data matching the Excel structure."""
    np.random.seed(42)
    
    data = {
        "Alter [J]": np.random.randint(1, 90, n_samples),
        "Geschlecht": np.random.choice(["m", "w"], n_samples),
        "Primäre Sprache": np.random.choice(["Deutsch", "Englisch", "Andere"], n_samples),
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": np.random.choice(
            ["praelingual", "perilingual", "postlingual"], n_samples
        ),
        "Diagnose.Höranamnese.Ursache....Ursache...": np.random.choice(
            ["Genetisch", "Meningitis", "Unbekannt", "Lärm"], n_samples
        ),
        "Symptome präoperativ.Tinnitus...": np.random.choice(["ja", "nein"], n_samples),
        "Behandlung/OP.CI Implantation": np.random.choice(
            ["Cochlear", "Med-El", "Advanced Bionics"], n_samples
        ),
    }
    
    df = pd.DataFrame(data)
    
    # Simulate outcome (post12 measure)
    # Younger age, postlingual, no meningitis -> better outcome
    base_score = 0.5
    age_factor = (100 - df["Alter [J]"]) / 200.0  # +0.05 to +0.5
    onset_factor = (df["Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..."] == "postlingual").astype(float) * 0.2
    
    noise = np.random.normal(0, 0.1, n_samples)
    
    score = base_score + age_factor + onset_factor + noise
    df["outcome_measurments.post12.measure."] = np.clip(score, 0, 1)
    
    return df


def train_model():
    """Train and export the pipeline."""
    print("Generating synthetic clinical data...")
    df = create_dummy_data()
    
    # Define features
    numeric_features = ["Alter [J]"]
    categorical_features = [
        "Geschlecht",
        "Primäre Sprache",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...",
        "Diagnose.Höranamnese.Ursache....Ursache...",
        "Symptome präoperativ.Tinnitus...",
        "Behandlung/OP.CI Implantation"
    ]
    
    target = "outcome_measurments.post12.measure."
    
    X = df[numeric_features + categorical_features]
    y = df[target]
    
    # Preprocessing
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )
    
    # Model
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    print("Training model...")
    pipeline.fit(X, y)
    
    # Evaluate
    score = pipeline.score(X, y)
    print(f"R² Score on training data: {score:.3f}")
    
    # Export
    output_path = Path(__file__).parent.parent / "app" / "models" / "logreg_best_pipeline.pkl"
    print(f"Exporting to {output_path}...")
    dump(pipeline, output_path)
    print("Done.")


if __name__ == "__main__":
    train_model()
