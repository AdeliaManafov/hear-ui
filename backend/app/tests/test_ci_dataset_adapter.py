"""Tests for app.core.ci_dataset_adapter – CochlearImplantDatasetAdapter."""

from __future__ import annotations

import numpy as np
import pytest

from app.core.ci_dataset_adapter import CochlearImplantDatasetAdapter


class TestCochlearImplantDatasetAdapter:
    @pytest.fixture()
    def adapter(self):
        return CochlearImplantDatasetAdapter()

    # --- preprocess ---
    def test_preprocess_returns_array_like(self, adapter):
        result = adapter.preprocess({"Alter [J]": 50, "Geschlecht": "w"})
        # May return DataFrame or ndarray depending on preprocessor
        assert hasattr(result, "shape")
        assert result.shape[0] == 1

    def test_preprocess_empty_input(self, adapter):
        """Even empty dict should produce valid array-like (defaults)."""
        result = adapter.preprocess({})
        assert hasattr(result, "shape")

    # --- get_feature_names ---
    def test_get_feature_names_returns_list(self, adapter):
        names = adapter.get_feature_names()
        assert isinstance(names, list)
        assert len(names) > 0
        # Should include canonical German names
        assert "Alter [J]" in names

    # --- get_feature_schema ---
    def test_get_feature_schema(self, adapter):
        schema = adapter.get_feature_schema()
        assert isinstance(schema, dict)
        assert "features" in schema
        assert schema["dataset_name"] == "cochlear_implant_outcome"
        assert schema["n_features"] == 68

    # --- validate_input ---
    def test_validate_valid_input(self, adapter):
        ok, err = adapter.validate_input({"Alter [J]": 50})
        assert ok is True
        assert err is None

    def test_validate_age_out_of_range(self, adapter):
        ok, err = adapter.validate_input({"Alter [J]": 150})
        assert ok is False
        assert "between 0 and 120" in err

    def test_validate_age_negative(self, adapter):
        ok, err = adapter.validate_input({"age": -5})
        assert ok is False

    def test_validate_age_invalid_type(self, adapter):
        ok, err = adapter.validate_input({"alter": "not_a_number"})
        assert ok is False
        assert "valid number" in err

    def test_validate_no_age(self, adapter):
        """No age field → passes validation."""
        ok, err = adapter.validate_input({"Geschlecht": "m"})
        assert ok is True

    def test_validate_alias_key(self, adapter):
        ok, err = adapter.validate_input({"age": 30})
        assert ok is True
