"""Feature catalog loader for labels, locales, and metadata."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
import json


def _config_dir() -> Path:
    base = Path(__file__).resolve().parent.parent
    return base / "config"


def _definitions_path() -> Path:
    return _config_dir() / "feature_definitions.json"


def _locales_dir() -> Path:
    return _config_dir() / "feature_locales"


def _section_locales_dir() -> Path:
    return _config_dir() / "section_locales"


def _normalize_locale(locale: str) -> str:
    return (locale or "en").split("-")[0].lower()


@lru_cache(maxsize=1)
def load_feature_definitions() -> list[dict[str, Any]]:
    path = _definitions_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    features = data.get("features") if isinstance(data, dict) else None
    if not isinstance(features, list):
        return []
    cleaned: list[dict[str, Any]] = []
    for entry in features:
        if not isinstance(entry, dict):
            continue
        raw = entry.get("raw")
        normalized = entry.get("normalized")
        description = entry.get("description")
        options = entry.get("options")
        section = entry.get("section")
        input_type = entry.get("input_type")
        feature_type = entry.get("type")
        multiple = entry.get("multiple")
        other_field = entry.get("other_field")
        ui_only = entry.get("ui_only")
        if not raw or not normalized:
            continue
        cleaned_entry = {
            "raw": raw,
            "normalized": normalized,
            "description": description or normalized,
        }
        if isinstance(options, list):
            cleaned_entry["options"] = options
        if isinstance(section, str):
            cleaned_entry["section"] = section
        if isinstance(input_type, str):
            cleaned_entry["input_type"] = input_type
        if isinstance(feature_type, str):
            cleaned_entry["type"] = feature_type
        if isinstance(multiple, bool):
            cleaned_entry["multiple"] = multiple
        if isinstance(other_field, str):
            cleaned_entry["other_field"] = other_field
        if isinstance(ui_only, bool):
            cleaned_entry["ui_only"] = ui_only
        cleaned.append(cleaned_entry)
    return cleaned


@lru_cache(maxsize=1)
def _definitions_index() -> dict[str, dict[str, Any]]:
    by_raw: dict[str, dict[str, Any]] = {}
    for entry in load_feature_definitions():
        by_raw[entry["raw"]] = entry
    return by_raw


@lru_cache(maxsize=8)
def load_feature_locales(locale: str) -> dict[str, str]:
    lang = _normalize_locale(locale)
    path = _locales_dir() / f"{lang}.json"
    if not path.exists() and lang != "en":
        path = _locales_dir() / "en.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {str(k): str(v) for k, v in data.items()} if isinstance(data, dict) else {}


@lru_cache(maxsize=8)
def load_section_locales(locale: str) -> dict[str, str]:
    lang = _normalize_locale(locale)
    path = _section_locales_dir() / f"{lang}.json"
    if not path.exists() and lang != "en":
        path = _section_locales_dir() / "en.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {str(k): str(v) for k, v in data.items()} if isinstance(data, dict) else {}


def build_raw_label_map(locale: str) -> dict[str, str]:
    """Return mapping of raw feature names to localized labels."""
    labels = load_feature_locales(locale)
    by_raw = _definitions_index()
    mapped: dict[str, str] = {}
    for raw, entry in by_raw.items():
        normalized = entry.get("normalized") or raw
        mapped[raw] = labels.get(normalized, entry.get("description") or normalized)
    return mapped
