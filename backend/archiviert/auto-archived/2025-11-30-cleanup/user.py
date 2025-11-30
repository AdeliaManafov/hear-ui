from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


# ------------------------------------------------------------
# Gemeinsame Felder für alle User-Modelle
# ------------------------------------------------------------
class UserBase(SQLModel):
    email: str = Field(index=True, nullable=False, unique=True)
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


# ------------------------------------------------------------
# Datenbankmodell (Tabelle)
# ------------------------------------------------------------
class User(UserBase, table=True):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    hashed_password: str


# ------------------------------------------------------------
# Eingabe beim Erstellen eines Users (z. B. Registrierung)
# ------------------------------------------------------------
class UserCreate(UserBase):
    password: str


# ------------------------------------------------------------
# Eingabe beim Aktualisieren eines Users
# ------------------------------------------------------------
class UserUpdate(UserBase):
    password: str | None = None


# ------------------------------------------------------------
# Öffentliches User-Modell (ohne Passwort)
# ------------------------------------------------------------
class UserPublic(SQLModel):
    id: UUID
    email: str
    full_name: str | None = None
    is_active: bool
    is_superuser: bool


# ------------------------------------------------------------
# Passwort-Update-Modell (z. B. wenn User sein Passwort ändert)
# ------------------------------------------------------------
class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# ------------------------------------------------------------
# Modell für Benutzerregistrierung
# ------------------------------------------------------------
class UserRegister(SQLModel):
    email: str
    full_name: str | None = None
    password: str


# ------------------------------------------------------------
# Mehrere Benutzer (z. B. GET /users/)
# ------------------------------------------------------------
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# ------------------------------------------------------------
# Modell für das Aktualisieren eigener User-Daten (Profil bearbeiten)
# ------------------------------------------------------------
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    password: str | None = None
