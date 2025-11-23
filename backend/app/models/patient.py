"""Patient model based on real clinical data structure."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Gender(str, Enum):
    MALE = "m"
    FEMALE = "w"
    DIVERS = "d"


class PatientBase(BaseModel):
    """Base patient data matching the Excel structure."""
    
    # Demographics
    age: int = Field(..., alias="Alter [J]", description="Age in years")
    gender: str = Field(..., alias="Geschlecht", description="Gender (m/w/d)")
    
    # Language
    primary_language: str = Field(..., alias="Primäre Sprache", description="Primary language")
    
    # Medical History
    hearing_loss_onset: str = Field(..., alias="Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...", description="Onset of hearing loss")
    hearing_loss_duration: float | None = Field(None, description="Duration of hearing loss in years (for compatibility)")
    hearing_loss_cause: str = Field(..., alias="Diagnose.Höranamnese.Ursache....Ursache...", description="Cause of hearing loss")
    
    # Pre-op Symptoms (Binary/Categorical)
    tinnitus: str = Field("nein", alias="Symptome präoperativ.Tinnitus...", description="Pre-op Tinnitus")
    vertigo: str = Field("nein", alias="Symptome präoperativ.Schwindel...", description="Pre-op Vertigo")
    
    # Implant
    implant_type: str = Field(..., alias="Behandlung/OP.CI Implantation", description="CI Implant Type/Date")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Alter [J]": 45,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
                "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
                "Symptome präoperativ.Tinnitus...": "ja",
                "Behandlung/OP.CI Implantation": "Cochlear Nucleus"
            }
        }


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase):
    id: int = Field(..., alias="ID")
