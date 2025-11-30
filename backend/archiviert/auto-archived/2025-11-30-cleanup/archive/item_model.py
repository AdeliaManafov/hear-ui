from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


# ------------------------------------------------------------
# Basisdaten eines Items (e.g. medizinische Datei, Patientendaten usw.)
# (Archived: removed from active domain)
# ------------------------------------------------------------
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# ------------------------------------------------------------
# Datenbankmodell (tatsächliche Tabelle)
# ------------------------------------------------------------
class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    owner_id: UUID


# ------------------------------------------------------------
# Zum Erstellen eines neuen Items (POST)
# ------------------------------------------------------------
class ItemCreate(ItemBase):
    owner_id: UUID


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
