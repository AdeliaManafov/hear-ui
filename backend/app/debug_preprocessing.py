#!/usr/bin/env python3
"""Debug script to compare preprocessing between endpoints."""

import sys
from uuid import UUID

import numpy as np
from sqlmodel import Session, create_engine

# Setup
from app import crud
from app.core.model_wrapper import ModelWrapper

# Database connection
DATABASE_URL = "postgresql://postgres:changethis@localhost:5434/hear_db"
engine = create_engine(DATABASE_URL)

# Load model
wrapper = ModelWrapper()
wrapper.load_model()

# Get patient
patient_id = UUID("5741fcf2-e234-4ffe-b2df-4f441ed81e4e")

with Session(engine) as session:
    patient = crud.get_patient(session, patient_id)
    if not patient:
        print("Patient not found!")
        sys.exit(1)

    input_features = patient.input_features or {}
    print(f"Patient has {len(input_features)} features")
    print(f"Sample keys: {list(input_features.keys())[:10]}")

    # Test /predict path (dict -> prepare_input -> model)
    print("\n=== /predict path ===")
    preprocessed_predict = wrapper.prepare_input(input_features)
    print(f"Preprocessed shape: {preprocessed_predict.shape}")
    print(f"First 10 values: {preprocessed_predict[0, :10]}")
    prediction_predict = wrapper.predict(input_features)
    print(
        f"Prediction: {prediction_predict[0] if hasattr(prediction_predict, '__len__') else prediction_predict}"
    )

    # Test /explainer path (dict -> prepare_input -> model)
    print("\n=== /explainer path (direct) ===")
    preprocessed_explainer = wrapper.prepare_input(input_features)
    print(f"Preprocessed shape: {preprocessed_explainer.shape}")
    print(f"First 10 values: {preprocessed_explainer[0, :10]}")
    prediction_explainer = wrapper.predict(preprocessed_explainer)
    print(
        f"Prediction: {prediction_explainer[0] if hasattr(prediction_explainer, '__len__') else prediction_explainer}"
    )

    # Check if arrays are identical
    print("\n=== Comparison ===")
    arrays_equal = np.array_equal(preprocessed_predict, preprocessed_explainer)
    print(f"Arrays equal: {arrays_equal}")
    if not arrays_equal:
        diff = preprocessed_predict - preprocessed_explainer
        print(f"Max difference: {np.max(np.abs(diff))}")
        print(f"Non-zero differences: {np.count_nonzero(diff)}")
