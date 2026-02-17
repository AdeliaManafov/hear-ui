"""Configuration-based dataset adapter for maximum flexibility.

This module provides a fully configurable dataset adapter that eliminates
hardcoded domain knowledge by reading feature specifications from JSON/YAML
configuration files.

Key advantages over hardcoded adapters:
- Model is easily swappable (just change config file)
- No code changes needed for new features/encodings
- Configuration is version-controlled and auditable
- Supports arbitrary datasets without code modifications

Example usage:
    >>> from app.core.config_based_adapter import load_dataset_adapter_from_config
    >>> adapter = load_dataset_adapter_from_config("config/random_forest_features.json")
    >>> X = adapter.preprocess({"Alter [J]": 45, "Geschlecht": "w"})
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

from .model_adapter import DatasetAdapter

logger = logging.getLogger(__name__)


class ConfigBasedDatasetAdapter(DatasetAdapter):
    """Dataset adapter driven by feature configuration.

    Supports:
    - Numeric features with type conversion and bounds
    - Binary features with configurable positive value mappings
    - Categorical features with label encoding or one-hot encoding
    - Flexible aliasing (e.g., "age" → "Alter [J]")
    - Default values for missing features
    """

    def __init__(self, feature_config: dict[str, Any]):
        """Initialize adapter with feature configuration.

        Args:
            feature_config: Dictionary with 'features' list defining each feature
        """
        self.config = feature_config
        self.features = feature_config.get("features", [])
        self.feature_names = [f["name"] for f in self.features]

        # Build alias lookup for fast resolution
        self.alias_map: dict[str, str] = {}
        for feature in self.features:
            canonical_name = feature["name"]
            self.alias_map[canonical_name] = canonical_name
            for alias in feature.get("aliases", []):
                self.alias_map[alias] = canonical_name

        logger.info(
            f"Initialized ConfigBasedDatasetAdapter: "
            f"{len(self.features)} features, "
            f"{len(self.alias_map)} aliases"
        )

    def preprocess(self, raw_input: dict) -> np.ndarray:
        """Preprocess raw input using configuration-defined rules.

        Args:
            raw_input: Dictionary with patient/sample data

        Returns:
            Preprocessed feature array (shape: (1, n_features))
        """
        values = []

        for feature in self.features:
            name = feature["name"]
            feature_type = feature["type"]
            default = feature.get("default", 0.0)

            # Resolve value: try canonical name, then aliases
            value = raw_input.get(name)
            if value is None:
                for alias in feature.get("aliases", []):
                    if alias in raw_input:
                        value = raw_input[alias]
                        break

            # Use default if still None
            if value is None:
                value = default

            # Apply type-specific preprocessing
            if feature_type == "numeric":
                processed_value = self._process_numeric(value, feature)
            elif feature_type == "binary":
                processed_value = self._process_binary(value, feature)
            elif feature_type == "categorical":
                processed_value = self._process_categorical(value, feature)
            else:
                logger.warning(f"Unknown feature type '{feature_type}' for {name}")
                processed_value = float(value) if value is not None else 0.0

            values.append(processed_value)

        # Shape: (1, n_features)
        return np.array(values, dtype=np.float32).reshape(1, -1)

    def _process_numeric(self, value: Any, feature: dict) -> float:
        """Process numeric feature with bounds checking."""
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            logger.warning(
                f"Invalid numeric value '{value}' for {feature['name']}, "
                f"using default {feature.get('default', 0.0)}"
            )
            return float(feature.get("default", 0.0))

        # Apply bounds if specified
        min_val = feature.get("min")
        max_val = feature.get("max")
        if min_val is not None:
            numeric_value = max(numeric_value, min_val)
        if max_val is not None:
            numeric_value = min(numeric_value, max_val)

        return numeric_value

    def _process_binary(self, value: Any, feature: dict) -> float:
        """Process binary feature (0 or 1)."""
        if value is None:
            return float(feature.get("default", 0))

        # Check against positive value mappings
        positive_values = feature.get("positive_values", ["ja", "yes", "1", "true"])
        if isinstance(value, str):
            return 1.0 if value.lower().strip() in positive_values else 0.0
        else:
            # Truthy/falsy evaluation
            return 1.0 if value else 0.0

    def _process_categorical(self, value: Any, feature: dict) -> float:
        """Process categorical feature using label encoding."""
        encoding_type = feature.get("encoding", "label")

        if encoding_type == "label":
            # Label encoding: map category → integer
            mapping = feature.get("mapping", {})
            default = feature.get("default", 0)

            if value is None:
                return float(default)

            value_str = str(value).strip()
            encoded = mapping.get(value_str, default)
            return float(encoded)

        elif encoding_type == "onehot":
            # One-hot encoding would expand to multiple columns
            # For simplicity in this implementation, we fall back to label
            logger.warning(
                f"One-hot encoding not fully supported yet for {feature['name']}, "
                "using label encoding"
            )
            mapping = feature.get("mapping", {})
            default = feature.get("default", 0)
            value_str = str(value).strip() if value is not None else ""
            return float(mapping.get(value_str, default))

        else:
            logger.warning(f"Unknown encoding '{encoding_type}' for {feature['name']}")
            return float(feature.get("default", 0))

    def get_feature_names(self) -> list[str]:
        """Return list of feature names in order."""
        return self.feature_names

    def get_feature_schema(self) -> dict[str, Any]:
        """Return full feature configuration."""
        return self.config

    def validate_input(self, raw_input: dict) -> tuple[bool, str | None]:
        """Validate input against schema (optional strict validation).

        Args:
            raw_input: Dictionary with input features

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic validation: check if any recognized keys present
        recognized_keys = set(self.alias_map.keys())
        input_keys = set(raw_input.keys())

        if not input_keys & recognized_keys:
            return (
                False,
                f"No recognized features found. Expected one of: {list(recognized_keys)[:10]}...",
            )

        return True, None


def load_dataset_adapter_from_config(
    config_path: str | Path,
) -> ConfigBasedDatasetAdapter:
    """Load a dataset adapter from a JSON configuration file.

    Args:
        config_path: Path to JSON configuration file

    Returns:
        ConfigBasedDatasetAdapter instance

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config file is invalid
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}") from e

    # Validate required keys
    if "features" not in config:
        raise ValueError(f"Configuration must contain 'features' key: {config_path}")

    logger.info(f"Loaded dataset adapter config from {config_path}")
    return ConfigBasedDatasetAdapter(config)


def load_dataset_adapter_from_model_name(model_name: str) -> ConfigBasedDatasetAdapter:
    """Load dataset adapter by model name (convention-based lookup).

    Looks for config file at: app/config/{model_name}_features.json

    Args:
        model_name: Model identifier (e.g., "random_forest_final")

    Returns:
        ConfigBasedDatasetAdapter instance

    Example:
        >>> adapter = load_dataset_adapter_from_model_name("random_forest_final")
    """
    # Try to find config file relative to this module
    base_dir = Path(__file__).parent.parent / "config"
    config_path = base_dir / f"{model_name}_features.json"

    return load_dataset_adapter_from_config(config_path)
