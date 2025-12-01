import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    computed_field,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",          # eine Ebene über backend
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 Tage
    FRONTEND_HOST: str = "http://localhost:5173"
    SENTRY_DSN: str | None = None
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str = "Hear-UI"

    # 🔑 Datenbank
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # Accept string values like "5433:5432" from docker port mappings
    POSTGRES_PORT: str = "5432"

    @field_validator("POSTGRES_PORT", mode="before")
    @classmethod
    def normalize_postgres_port(cls, v: Any) -> str:
        """Normalize POSTGRES_PORT from env values.

        Accepts integers, numeric strings, or Docker-style mappings like
        "5433:5432" (returns the container port number, the right-hand side).
        """
        if v is None:
            return "5432"
        if isinstance(v, int):
            return str(v)
        if isinstance(v, str):
            # Handle docker-style port mapping "5433:5432" -> take last part
            if ":" in v:
                v = v.split(":")[-1]
            # Keep only digits
            digits = "".join(ch for ch in v if ch.isdigit())
            return digits if digits else "5432"
        return "5432"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def postgres_port_int(self) -> int:
        """Return POSTGRES_PORT as an integer."""
        return int(self.POSTGRES_PORT)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Use the psycopg (psycopg3) dialect when psycopg[binary] is installed
        # The project depends on psycopg[binary] (psycopg v3). SQLAlchemy will
        # import the appropriate DBAPI for 'psycopg'. Previously this used
        # 'psycopg2' which requires the psycopg2 package; change to 'psycopg'
        # to avoid ModuleNotFoundError when only psycopg v3 is available.
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.postgres_port_int}/{self.POSTGRES_DB}"
        )

    # 📧 E-Mail Einstellungen (aus .env)
    # For MVP we allow this to be optional so the app can start without SMTP config.
    EMAILS_FROM_EMAIL: EmailStr | None = None
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # ⚙️ Sicherheit
    # Note: SECRET_KEY is already defined above with a default
    # Testing flag to enable destructive schema operations in local/test runs
    TESTING: bool = False


# Instanz erstellen
settings = Settings()

