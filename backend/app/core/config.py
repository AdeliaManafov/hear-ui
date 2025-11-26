import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    Field,
    computed_field,
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
    POSTGRES_SERVER: str = Field(..., env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

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
            f"{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

    # 📧 E-Mail Einstellungen (aus .env)
    # For MVP we allow this to be optional so the app can start without SMTP config.
    EMAILS_FROM_EMAIL: EmailStr | None = Field(None, env="EMAILS_FROM_EMAIL")
    FIRST_SUPERUSER: EmailStr = Field(..., env="FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = Field(..., env="FIRST_SUPERUSER_PASSWORD")

    # ⚙️ Sicherheit
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    # Testing flag to enable destructive schema operations in local/test runs
    TESTING: bool = Field(False, env="TESTING")


# Instanz erstellen
settings = Settings()

