from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


# ------------------------------------------------------------
# Basisdaten eines Items (z. B. medizinische Datei, Patientendaten usw.)
# ------------------------------------------------------------
class ItemBase(SQLModel):
    title: str
    description: Optional[str] = None


# ------------------------------------------------------------
# Datenbankmodell (tatsächliche Tabelle)
# ------------------------------------------------------------
class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    owner_id: UUID = Field(foreign_key="user.id")


# ------------------------------------------------------------
# Zum Erstellen eines neuen Items (POST)
# ------------------------------------------------------------
class ItemCreate(ItemBase):
    pass


# ------------------------------------------------------------
# Zum Updaten eines bestehenden Items (PATCH)
# ------------------------------------------------------------
class ItemUpdate(ItemBase):
    pass


# ------------------------------------------------------------
# Zum Anzeigen eines einzelnen Items (Response)
# ------------------------------------------------------------
class ItemPublic(ItemBase):
    id: UUID
    owner_id: UUID


# ------------------------------------------------------------
# Zum Anzeigen einer Liste von Items
# ------------------------------------------------------------
class ItemsPublic(SQLModel):
    items: list[ItemPublic]


# ------------------------------------------------------------
# Für einfache Textnachrichten (z. B. API-Response)
# ------------------------------------------------------------
class Message(SQLModel):
    message: str
