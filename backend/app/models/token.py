from typing import Optional
from pydantic import BaseModel


# ------------------------------------------------------------
# Token (JWT Access Token)
# ------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


# ------------------------------------------------------------
# Token Payload (Dekodierte JWT-Daten)
# ------------------------------------------------------------
class TokenPayload(BaseModel):
    sub: Optional[str] = None


# ------------------------------------------------------------
# Neues Passwort für Passwort-Reset
# ------------------------------------------------------------
class NewPassword(BaseModel):
    token: str
    new_password: str
