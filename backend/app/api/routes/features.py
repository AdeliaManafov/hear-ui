"""Feature metadata and locale routes."""

from typing import Any

from fastapi import APIRouter, Query

from app.core.feature_catalog import (
    build_raw_label_map,
    load_feature_definitions,
    load_feature_locales,
    load_section_locales,
)

router = APIRouter(prefix="/features", tags=["features"])


def _normalize_locale(locale: str) -> str:
    return (locale or "en").split("-")[0].lower()


@router.get("/definitions")
def get_feature_definitions() -> dict[str, Any]:
    """Return feature list with raw names, normalized keys, and descriptions."""
    features = load_feature_definitions()
    section_order: list[str] = []
    try:
        seen: set[str] = set()
        for entry in features:
            section = entry.get("section") or "Weitere"
            if section in seen:
                continue
            seen.add(section)
            section_order.append(section)
    except Exception:
        section_order = []
    return {"features": features, "section_order": section_order}


@router.get("/locales/{locale}")
def get_feature_locales(locale: str) -> dict[str, Any]:
    """Return localized labels keyed by normalized feature name."""
    lang = _normalize_locale(locale)
    return {
        "language": lang,
        "labels": load_feature_locales(lang),
        "sections": load_section_locales(lang),
    }


@router.get("/labels")
def get_feature_labels(lang: str = Query(default="en")) -> dict[str, Any]:
    """Return localized labels keyed by raw feature name."""
    language = _normalize_locale(lang)
    return {"language": language, "labels": build_raw_label_map(language)}
