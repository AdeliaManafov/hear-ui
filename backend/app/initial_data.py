import logging
from sqlmodel import Session

from app.core.db import engine
from app import crud
from app.models import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# Erstellt initiale Daten in der Datenbank (z. B. Admin-User)
# ------------------------------------------------------------
def init() -> None:
    with Session(engine) as session:
        admin_email = "admin@example.com"
        admin_password = "admin123"  # kurz & kompatibel mit bcrypt

        # Prüfen, ob Admin schon existiert
        existing_user = crud.get_user_by_email(session, admin_email)
        if existing_user:
            logger.info("Admin user already exists, skipping creation.")
            return

        # Admin-User anlegen
        user_in = UserCreate(
            email=admin_email,
            password=admin_password,
            full_name="Admin User",
        )
        crud.create_user(session=session, user_create=user_in)
        session.commit()
        logger.info("Admin user created successfully.")


def main() -> None:
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data setup completed.")


if __name__ == "__main__":
    main()
