from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class PatientBase(SQLModel):
    """Store the raw input features for a patient as JSON."""

    input_features: dict[str, Any] | None = Field(default=None, sa_column=sa.Column(sa.JSON()))


class Patient(PatientBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PatientCreate(PatientBase):
    pass
