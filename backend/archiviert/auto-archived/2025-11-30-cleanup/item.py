"""Item model (archived but kept for Alembic compatibility)."""

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    title: str
    description: str | None = None


class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    owner_id: UUID


class ItemCreate(ItemBase):
    owner_id: UUID


class ItemUpdate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: UUID
    owner_id: UUID


class ItemsPublic(SQLModel):
    items: list[ItemPublic]


class Message(SQLModel):
    message: str
