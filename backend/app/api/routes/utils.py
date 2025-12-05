"""Utility routes for feature names and model metadata."""

from fastapi import APIRouter
from typing import Dict, List, Any

from app.core.model_wrapper import ModelWrapper
from app.core.feature_config import load_feature_config

router = APIRouter(prefix="/utils", tags=["utils"])
model_wrapper = ModelWrapper()


# Try to load an editable feature config from `app/config/features.yaml`.
# If not present or invalid, fall back to the hard-coded mapping below.
_FEATURE_CONFIG = load_feature_config()


@router.get("/health-check/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.get("/model-info/")
def model_info():
    """Get model information and metadata."""
    info = {
        "loaded": model_wrapper.is_loaded(),
        "model_type": str(type(model_wrapper.model)),
    }
    
    if hasattr(model_wrapper.model, 'feature_names_in_'):
        info["feature_names_in_"] = list(model_wrapper.model.feature_names_in_)
    
    if hasattr(model_wrapper.model, 'n_features_in_'):
        info["n_features_in_"] = model_wrapper.model.n_features_in_
        
    return info


@router.get("/feature-names/")
def get_feature_names() -> Dict[str, str]:
    """Get human-readable feature names mapping.
    
    Returns a dictionary mapping technical feature names (after transformation)
    to human-readable German labels suitable for UI display.
    """
    
    # If a feature config file exists and was parsed successfully, use it.
    if _FEATURE_CONFIG and _FEATURE_CONFIG.get("mapping"):
        return _FEATURE_CONFIG["mapping"]

    # Fallback: Mapping from technical names to human-readable German labels
    feature_mapping = {
        # Numeric features
        "num__Alter [J]": "Alter (Jahre)",
        
        # Gender
        "cat__Geschlecht_m": "Geschlecht: Männlich",
        "cat__Geschlecht_w": "Geschlecht: Weiblich",
        
        # Language
        "cat__Primäre Sprache_Deutsch": "Primärsprache: Deutsch",
        "cat__Primäre Sprache_Englisch": "Primärsprache: Englisch",
        "cat__Primäre Sprache_Arabisch": "Primärsprache: Arabisch",
        "cat__Primäre Sprache_Türkisch": "Primärsprache: Türkisch",
        "cat__Primäre Sprache_Andere": "Primärsprache: Andere",
        
        # Onset (Beginn der Hörminderung)
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._postlingual": 
            "Hörverlust: Nach Spracherwerb (postlingual)",
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._praelingual":
            "Hörverlust: Vor Spracherwerb (prälingual)",
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._perilingual":
            "Hörverlust: Rund um Spracherwerb (perilingual)",
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._< 1 y":
            "Hörverlust: Vor 1 Jahr",
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._1-5 y":
            "Hörverlust: 1-5 Jahre",
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._> 20 y":
            "Hörverlust: Über 20 Jahre",
        "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._Unbekannt":
            "Hörverlust: Unbekannt",
        
        # Cause (Ursache)
        "cat__Diagnose.Höranamnese.Ursache....Ursache..._Unbekannt":
            "Ursache: Unbekannt",
        "cat__Diagnose.Höranamnese.Ursache....Ursache..._Genetisch":
            "Ursache: Genetisch",
        "cat__Diagnose.Höranamnese.Ursache....Ursache..._Lärm":
            "Ursache: Lärmbedingt",
        "cat__Diagnose.Höranamnese.Ursache....Ursache..._Meningitis":
            "Ursache: Meningitis",
        "cat__Diagnose.Höranamnese.Ursache....Ursache..._Syndromal":
            "Ursache: Syndromal",
        "cat__Diagnose.Höranamnese.Ursache....Ursache..._Posttraumatisch":
            "Ursache: Posttraumatisch",
        
        # Tinnitus
        "cat__Symptome präoperativ.Tinnitus..._ja":
            "Tinnitus: Ja",
        "cat__Symptome präoperativ.Tinnitus..._nein":
            "Tinnitus: Nein",
        "cat__Symptome präoperativ.Tinnitus..._Vorhanden":
            "Tinnitus: Vorhanden",
        "cat__Symptome präoperativ.Tinnitus..._Kein":
            "Tinnitus: Nicht vorhanden",
        
        # Implant type
        "cat__Behandlung/OP.CI Implantation_Cochlear":
            "Implantat: Cochlear",
        "cat__Behandlung/OP.CI Implantation_Med-El":
            "Implantat: Med-El",
        "cat__Behandlung/OP.CI Implantation_Advanced Bionics":
            "Implantat: Advanced Bionics",
    }
    
    return feature_mapping


@router.get("/feature-categories/")
def get_feature_categories() -> Dict[str, List[str]]:
    """Get features grouped by category for better UI organization.
    
    Returns features organized by logical categories (Demographics, Diagnosis, etc.)
    """
    
    # Prefer config categories when available
    if _FEATURE_CONFIG and _FEATURE_CONFIG.get("categories"):
        return _FEATURE_CONFIG["categories"]

    categories = {
        "Demographische Daten": [
            "num__Alter [J]",
            "cat__Geschlecht_m",
            "cat__Geschlecht_w",
            "cat__Primäre Sprache_Deutsch",
            "cat__Primäre Sprache_Englisch",
            "cat__Primäre Sprache_Arabisch",
            "cat__Primäre Sprache_Türkisch",
            "cat__Primäre Sprache_Andere"
        ],
        "Diagnose - Beginn des Hörverlusts": [
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._postlingual",
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._praelingual",
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._perilingual",
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._< 1 y",
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._1-5 y",
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._> 20 y",
            "cat__Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..._Unbekannt"
        ],
        "Diagnose - Ursache": [
            "cat__Diagnose.Höranamnese.Ursache....Ursache..._Unbekannt",
            "cat__Diagnose.Höranamnese.Ursache....Ursache..._Genetisch",
            "cat__Diagnose.Höranamnese.Ursache....Ursache..._Lärm",
            "cat__Diagnose.Höranamnese.Ursache....Ursache..._Meningitis",
            "cat__Diagnose.Höranamnese.Ursache....Ursache..._Syndromal",
            "cat__Diagnose.Höranamnese.Ursache....Ursache..._Posttraumatisch"
        ],
        "Symptome": [
            "cat__Symptome präoperativ.Tinnitus..._ja",
            "cat__Symptome präoperativ.Tinnitus..._nein",
            "cat__Symptome präoperativ.Tinnitus..._Vorhanden",
            "cat__Symptome präoperativ.Tinnitus..._Kein"
        ],
        "Behandlung": [
            "cat__Behandlung/OP.CI Implantation_Cochlear",
            "cat__Behandlung/OP.CI Implantation_Med-El",
            "cat__Behandlung/OP.CI Implantation_Advanced Bionics"
        ]
    }

    return categories


@router.get("/feature-metadata/")
def get_feature_metadata() -> Dict[str, Dict[str, Any]]:
    """Return full metadata for features (if config provided).

    This returns a mapping `feature_name -> metadata` as provided in the
    YAML config. If no config is available an empty dict is returned.
    """
    if _FEATURE_CONFIG and _FEATURE_CONFIG.get("metadata"):
        return _FEATURE_CONFIG["metadata"]
    return {}
