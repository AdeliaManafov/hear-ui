"""Tests for predict batch helper functions."""

import pytest
from app.api.routes.predict_batch import (
    _to_bool,
    _parse_interval_to_years,
    _normalize_header,
)


class TestToBool:
    """Test _to_bool helper function."""

    def test_true_values(self):
        """Test true value parsing."""
        true_vals = ["ja", "yes", "vorhanden", "true", "1", "y", "JA", "YES"]
        for val in true_vals:
            assert _to_bool(val) is True, f"Expected True for '{val}'"

    def test_false_values(self):
        """Test false value parsing."""
        false_vals = ["nein", "no", "kein", "false", "0", "n", "NEIN", "NO"]
        for val in false_vals:
            assert _to_bool(val) is False, f"Expected False for '{val}'"

    def test_none_values(self):
        """Test None/empty value parsing."""
        none_vals = [None, "", "nan", "none"]
        for val in none_vals:
            result = _to_bool(val)
            assert result is None or result is False, f"Expected None or False for '{val}'"

    def test_unknown_value_returns_none(self):
        """Test unknown value returns None."""
        assert _to_bool("maybe") is None
        assert _to_bool("unknown") is None


class TestParseIntervalToYears:
    """Test _parse_interval_to_years helper function."""

    def test_interval_mappings(self):
        """Test standard interval mappings."""
        assert _parse_interval_to_years("< 1 y") == 0.5
        assert _parse_interval_to_years("1-2 y") == 1.5
        assert _parse_interval_to_years("2-5 y") == 3.5
        assert _parse_interval_to_years("5-10 y") == 7.5
        assert _parse_interval_to_years("10-20 y") == 15.0
        assert _parse_interval_to_years("> 20 y") == 25.0

    def test_none_input(self):
        """Test None input returns None."""
        assert _parse_interval_to_years(None) is None

    def test_empty_values(self):
        """Test empty/unknown values return None."""
        assert _parse_interval_to_years("") is None
        assert _parse_interval_to_years("nan") is None
        assert _parse_interval_to_years("nicht erhoben") is None
        assert _parse_interval_to_years("unbekannt") is None
        assert _parse_interval_to_years("unbekannt/ka") is None

    def test_numeric_string(self):
        """Test numeric string is parsed."""
        assert _parse_interval_to_years("5") == 5.0
        assert _parse_interval_to_years("10.5") == 10.5

    def test_invalid_string_returns_none(self):
        """Test invalid string returns None."""
        assert _parse_interval_to_years("invalid") is None


class TestNormalizeHeader:
    """Test _normalize_header helper function."""

    def test_basic_normalization(self):
        """Test basic header normalization."""
        assert _normalize_header("Age") == "age"
        assert _normalize_header("  Age  ") == "age"
        assert _normalize_header("ALTER") == "alter"

    def test_bom_removal(self):
        """Test BOM character removal."""
        assert _normalize_header("\ufeffAge") == "age"
        assert _normalize_header("\ufeff\ufeffTest") == "test"

    def test_none_input(self):
        """Test None input returns empty string."""
        assert _normalize_header(None) == ""

    def test_preserves_special_chars(self):
        """Test special characters are preserved."""
        assert _normalize_header("Alter [J]") == "alter [j]"
        assert _normalize_header("Primäre Sprache") == "primäre sprache"
