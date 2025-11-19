from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class FeedbackBase(SQLModel):
    input_features: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=sa.Column(sa.JSON())
    )
    prediction: Optional[float] = None
    explanation: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=sa.Column(sa.JSON())
    )
    accepted: Optional[bool] = None
    comment: Optional[str] = None
    user_email: Optional[str] = None


class Feedback(FeedbackBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FeedbackCreate(FeedbackBase):
    pass
