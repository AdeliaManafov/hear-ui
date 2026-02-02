"""Cochlear Implant dataset adapter implementation.

This is the concrete adapter for the CI use case, implementing the
DatasetAdapter interface with CI-specific preprocessing logic.
"""

from typing import Any

import numpy as np

from .model_adapter import DatasetAdapter
from .preprocessor import EXPECTED_FEATURES, preprocess_patient_data


class CochlearImplantDatasetAdapter(DatasetAdapter):
    """Dataset adapter for Cochlear Implant outcome prediction.

    This adapter wraps the existing CI-specific preprocessing logic
    and makes it conform to the generic DatasetAdapter interface.
    """

    def preprocess(self, raw_input: dict) -> np.ndarray:
        """Preprocess CI patient data into 68-feature array.

        Args:
            raw_input: Dictionary with patient data (German or English keys)

        Returns:
            Preprocessed feature array (shape: (1, 68))
        """
        return preprocess_patient_data(raw_input)

    def get_feature_names(self) -> list[str]:
        """Get the 68 CI-specific feature names.

        Returns:
            List of feature names in model input order
        """
        return list(EXPECTED_FEATURES)

    def get_feature_schema(self) -> dict[str, Any]:
        """Get the CI-specific feature schema.

        Returns:
            Dictionary describing CI features, types, and metadata
        """
        # This is a simplified schema; in production, load from features.yaml
        return {
            "dataset_name": "cochlear_implant_outcome",
            "description": "Cochlear implant outcome prediction features",
            "n_features": 68,
            "features": [
                {
                    "name": "Alter [J]",
                    "type": "numeric",
                    "aliases": ["age", "alter"],
                    "default": 50,
                    "description": "Patient age in years",
                },
                {
                    "name": "Geschlecht",
                    "type": "categorical",
                    "aliases": ["gender"],
                    "values": ["m", "w", "d"],
                    "description": "Patient gender",
                },
                {
                    "name": "Behandlung/OP.CI Implantation",
                    "type": "categorical",
                    "aliases": ["implant_type", "ci_type"],
                    "description": "Type of cochlear implant",
                },
                # Add other features as needed...
            ],
        }

    def validate_input(self, raw_input: dict) -> tuple[bool, str | None]:
        """Validate CI patient data.

        Args:
            raw_input: Dictionary with patient data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic validation: check for required fields
        age = (
            raw_input.get("Alter [J]") or raw_input.get("age") or raw_input.get("alter")
        )

        if age is not None:
            try:
                age_val = float(age)
                if age_val < 0 or age_val > 120:
                    return False, "Age must be between 0 and 120 years"
            except (ValueError, TypeError):
                return False, "Age must be a valid number"

        return True, None
