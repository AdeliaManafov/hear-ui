"""Test feature configuration consistency with preprocessor EXPECTED_FEATURES.

This test ensures that the feature config in `app/config/features.yaml` stays
in sync with the actual features used by the preprocessor and model. This prevents
drift where the UI might display features that don't match the model's inputs.
"""
import pytest
from app.core.feature_config import load_feature_config
from app.core.preprocessor import EXPECTED_FEATURES


class TestFeatureConfigConsistency:
    """Validate that feature config matches preprocessor expectations."""

    def test_feature_config_loads_successfully(self):
        """Test that feature config YAML loads without errors."""
        config = load_feature_config()
        assert isinstance(config, dict), "Config should be a dictionary"

    def test_feature_config_has_expected_structure(self):
        """Test that loaded config has expected keys."""
        config = load_feature_config()
        
        # Config may be empty if file missing (fallback behavior)
        if config:
            assert "mapping" in config or len(config) == 0
            assert "categories" in config or len(config) == 0
            assert "metadata" in config or len(config) == 0

    def test_feature_config_names_are_documented(self):
        """Test that config feature names are reasonable strings."""
        config = load_feature_config()
        
        if not config or not config.get("metadata"):
            pytest.skip("Feature config not present or empty")
        
        metadata = config["metadata"]
        for name, meta in metadata.items():
            assert isinstance(name, str), f"Feature name should be string: {name}"
            assert len(name) > 0, "Feature name should not be empty"
            assert isinstance(meta, dict), f"Metadata for {name} should be dict"
            assert "label" in meta or "type" in meta, f"Metadata for {name} should have label or type"

    def test_config_features_are_subset_of_expected_or_similar(self):
        """Test that config feature names relate to EXPECTED_FEATURES.
        
        Note: The config may use technical prefixes (num__, cat__, bin__) or
        transformed names that differ from raw EXPECTED_FEATURES. This test
        validates that config entries are reasonable and warns if there's
        significant mismatch.
        """
        config = load_feature_config()
        
        if not config or not config.get("metadata"):
            pytest.skip("Feature config not present or empty")
        
        config_names = set(config["metadata"].keys())
        expected_set = set(EXPECTED_FEATURES)
        
        # Check if there's any overlap or if config uses prefixed versions
        # (e.g., "num__Alter [J]" vs "Alter [J]")
        overlap_direct = config_names & expected_set
        
        # Check for prefix-stripped overlap
        config_stripped = {
            name.replace("num__", "").replace("cat__", "").replace("bin__", "")
            .replace("ord__", "").replace("int__", "")
            for name in config_names
        }
        overlap_stripped = config_stripped & expected_set
        
        # At least some features should match (allowing for prefixing)
        total_overlap = len(overlap_direct) + len(overlap_stripped)
        
        # We expect some relationship, but config might be a subset or use different naming
        # This is a soft check to catch major drift
        if len(config_names) > 0 and len(expected_set) > 0:
            # If config has features but zero overlap, warn
            assert total_overlap > 0 or len(config_names) < 20, (
                f"Feature config names don't overlap with EXPECTED_FEATURES. "
                f"Config has {len(config_names)} features, "
                f"EXPECTED_FEATURES has {len(expected_set)} features. "
                f"Check if feature names in config match preprocessor expectations."
            )

    def test_expected_features_count(self):
        """Sanity check that EXPECTED_FEATURES has expected count (68 for current model)."""
        assert len(EXPECTED_FEATURES) == 68, (
            f"EXPECTED_FEATURES should have 68 entries for current model, "
            f"found {len(EXPECTED_FEATURES)}"
        )

    def test_config_categories_contain_valid_names(self):
        """Test that category lists reference valid feature names."""
        config = load_feature_config()
        
        if not config or not config.get("categories"):
            pytest.skip("Feature categories not present")
        
        categories = config["categories"]
        metadata = config.get("metadata", {})
        
        for category_name, feature_list in categories.items():
            assert isinstance(feature_list, list), f"Category {category_name} should be a list"
            for feature_name in feature_list:
                # Each feature in a category should exist in metadata
                if metadata:
                    assert feature_name in metadata, (
                        f"Feature '{feature_name}' in category '{category_name}' "
                        f"not found in metadata"
                    )
