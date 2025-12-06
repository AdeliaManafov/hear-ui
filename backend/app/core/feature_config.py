"""Feature configuration loader.

Loads `app/config/features.yaml` (YAML) and exposes helper functions to get
feature label mappings, categories and metadata. If the file is missing or
malformed, the loader returns empty structures and callers should fall back to
hard-coded defaults.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional
import threading

import yaml

_CACHE: Dict[str, Any] = {}
_LOCK = threading.Lock()


def _default_config_path() -> Path:
    # package: backend/app/core -> config is at backend/app/config/features.yaml
    return Path(__file__).resolve().parents[1] / "config" / "features.yaml"


def load_feature_config(path: Optional[str | Path] = None) -> Dict[str, Any]:
    """Load and return parsed feature configuration.

    Returns a dict with keys: `mapping` (name->label), `categories` (cat->list
    of names), and `metadata` (name->full metadata dict). If loading fails an
    empty dict is returned.
    """
    global _CACHE
    key = str(path or _default_config_path())

    with _LOCK:
        if key in _CACHE:
            return _CACHE[key]

        p = Path(path) if path else _default_config_path()
        if not p.exists():
            _CACHE[key] = {}
            return _CACHE[key]

        try:
            with p.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            features = data.get("features", []) if isinstance(data, dict) else []

            mapping: Dict[str, str] = {}
            categories: Dict[str, list] = {}
            metadata: Dict[str, dict] = {}

            for f in features:
                name = f.get("name")
                if not name:
                    continue
                label = f.get("label") or name
                mapping[name] = label
                cat = f.get("category") or "Uncategorized"
                categories.setdefault(cat, []).append(name)
                metadata[name] = f

            _CACHE[key] = {"mapping": mapping, "categories": categories, "metadata": metadata}
            return _CACHE[key]

        except Exception:
            # Don't raise here — callers will fall back to hard-coded defaults.
            _CACHE[key] = {}
            return _CACHE[key]


def refresh_feature_config(path: Optional[str | Path] = None) -> Dict[str, Any]:
    """Clear cache and reload configuration from disk."""
    global _CACHE
    key = str(path or _default_config_path())
    with _LOCK:
        if key in _CACHE:
            del _CACHE[key]
    return load_feature_config(path)


__all__ = ["load_feature_config", "refresh_feature_config"]
