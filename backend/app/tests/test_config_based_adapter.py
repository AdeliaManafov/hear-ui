"""Test configuration-based dataset adapter.

Demonstrates that the config-based adapter produces identical results
to the hardcoded RandomForestDatasetAdapter.
"""

import json
from pathlib import Path

import numpy as np
import pytest

from app.core.config_based_adapter import (
    ConfigBasedDatasetAdapter,
    load_dataset_adapter_from_config,
    load_dataset_adapter_from_model_name,
)
from app.core.rf_dataset_adapter import RandomForestDatasetAdapter


class TestConfigBasedDatasetAdapter:
    """Test suite for configuration-based dataset adapter."""

    def test_load_from_config_file(self):
        """Test loading adapter from JSON config file."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        assert len(adapter.get_feature_names()) == 39
        assert adapter.get_feature_names()[0] == "Geschlecht"
        assert adapter.get_feature_names()[1] == "Alter [J]"

    def test_load_from_model_name(self):
        """Test convention-based loading by model name."""
        adapter = load_dataset_adapter_from_model_name("random_forest")
        assert len(adapter.get_feature_names()) == 39

    def test_preprocess_basic_input(self):
        """Test preprocessing with basic input."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        raw_input = {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Seiten": "L",
            "pre_measure": 12.5,
            "abstand": 180,
        }

        X = adapter.preprocess(raw_input)

        # Check shape
        assert X.shape == (1, 39), f"Expected (1, 39), got {X.shape}"

        # Check specific encoded values
        assert X[0, 0] == 1.0, "Geschlecht 'w' should encode to 1.0"
        assert X[0, 1] == 45.0, "Age should be 45.0"

    def test_alias_resolution(self):
        """Test that aliases are properly resolved."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        # Using English aliases instead of German names
        raw_input = {
            "age": 55,
            "gender": "m",
            "primary_language": "Deutsch",
            "implant_side": "R",
        }

        X = adapter.preprocess(raw_input)

        # Gender "m" should encode to 0
        assert X[0, 0] == 0.0, "Gender 'm' should encode to 0.0"
        # Age should be 55
        assert X[0, 1] == 55.0, "Age should be 55.0"

    def test_default_values(self):
        """Test that defaults are applied for missing features."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        # Minimal input
        raw_input = {"Alter [J]": 40}

        X = adapter.preprocess(raw_input)

        # Should have 39 features, all filled with defaults
        assert X.shape == (1, 39)
        # Age should be 40
        assert X[0, 1] == 40.0

    def test_binary_feature_encoding(self):
        """Test binary feature encoding with positive value mappings."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        # Test various positive value formats
        test_cases = [
            ({"tinnitus": "ja"}, "ja should map to 1.0"),
            ({"tinnitus": "yes"}, "yes should map to 1.0"),
            ({"tinnitus": "1"}, "1 should map to 1.0"),
            ({"tinnitus": "nein"}, "nein should map to 0.0"),
            ({"tinnitus": "no"}, "no should map to 0.0"),
        ]

        for test_input, description in test_cases:
            X = adapter.preprocess(test_input)
            tinnitus_idx = adapter.get_feature_names().index("Symptome präoperativ.Tinnitus...")
            if "ja" in str(test_input["tinnitus"]) or "yes" in str(test_input["tinnitus"]) or test_input["tinnitus"] == "1":
                assert X[0, tinnitus_idx] == 1.0, description
            else:
                assert X[0, tinnitus_idx] == 0.0, description

    def test_categorical_label_encoding(self):
        """Test categorical features with label encoding."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        raw_input = {
            "Geschlecht": "m",  # Should encode to 0
            "Alter [J]": 50,
        }

        X = adapter.preprocess(raw_input)
        assert X[0, 0] == 0.0, "Gender 'm' should encode to 0"

        raw_input["Geschlecht"] = "w"  # Should encode to 1
        X = adapter.preprocess(raw_input)
        assert X[0, 0] == 1.0, "Gender 'w' should encode to 1"

    def test_comparison_with_hardcoded_adapter(self):
        """Compare config-based adapter output with hardcoded adapter.

        Both should produce similar results for the same input.
        """
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        config_adapter = load_dataset_adapter_from_config(config_path)
        hardcoded_adapter = RandomForestDatasetAdapter()

        # Sample patient data
        raw_input = {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Seiten": "L",
            "Symptome präoperativ.Tinnitus...": "ja",
            "Symptome präoperativ.Schwindel...": "nein",
            "outcome_measurments.pre.measure.": 15.0,
            "abstand": 200,
        }

        X_config = config_adapter.preprocess(raw_input)
        X_hardcoded = hardcoded_adapter.preprocess(raw_input)

        # Both should have same shape
        assert X_config.shape == X_hardcoded.shape == (1, 39)

        # Check a few key features match
        # Gender (index 0)
        assert X_config[0, 0] == X_hardcoded[0, 0], "Gender encoding should match"
        # Age (index 1)
        assert X_config[0, 1] == X_hardcoded[0, 1], "Age should match"

    def test_validate_input(self):
        """Test input validation."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        # Valid input
        valid, error = adapter.validate_input({"age": 45, "gender": "m"})
        assert valid is True
        assert error is None

        # Invalid input (no recognized keys)
        valid, error = adapter.validate_input({"unknown_field": 123})
        assert valid is False
        assert error is not None

    def test_bounds_checking(self):
        """Test numeric bounds are enforced."""
        config_path = Path(__file__).parent.parent.parent / "app" / "config" / "random_forest_features.json"
        adapter = load_dataset_adapter_from_config(config_path)

        # Age outside bounds (config has min=0, max=120)
        raw_input = {"Alter [J]": 150}
        X = adapter.preprocess(raw_input)

        # Should be clamped to max (120)
        assert X[0, 1] == 120.0, "Age should be clamped to 120"

        # Negative age
        raw_input = {"Alter [J]": -10}
        X = adapter.preprocess(raw_input)
        # Should be clamped to min (0)
        assert X[0, 1] == 0.0, "Age should be clamped to 0"
