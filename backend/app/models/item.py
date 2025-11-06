from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import UUID, uuid4

class Item(SQLModel, table=True):  # <--- WICHTIG!
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    owner_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
