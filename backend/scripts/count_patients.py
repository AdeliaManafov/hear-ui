#!/usr/bin/env python3
"""Count patients in the configured database.

Usage:
  cd backend
  python scripts/count_patients.py

The script reads the database URL from the app settings (see `app.core.config.settings`) or
from the `DATABASE_URL` environment variable if set.
"""
import os
import sys
from sqlalchemy import create_engine, text, func
from sqlmodel import Session

def get_database_url():
    # Prefer explicit DATABASE_URL env var for overrides (useful in CI)
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url

    # Import lazily to avoid import-time side effects when run outside the project
    try:
        from app.core.config import settings
    except Exception as e:
        print(f"Could not import app settings: {e}", file=sys.stderr)
        sys.exit(2)

    return str(settings.SQLALCHEMY_DATABASE_URI)


def main():
    db_url = get_database_url()
    print(f"Using database: {db_url}")

    try:
        engine = create_engine(db_url)
    except Exception as e:
        print(f"Failed to create engine: {e}", file=sys.stderr)
        sys.exit(3)

    try:
        with Session(engine) as session:
            # Try to count from `patient` table — use plain SQL to be resilient
            try:
                result = session.exec(text("SELECT COUNT(*) FROM patient;"))
                count = result.one()[0]
            except Exception:
                # Fallback: try to use SQLModel/ORM if table name differs
                try:
                    from app.models import Patient
                    result = session.exec(func.count().select().select_from(Patient))
                    count = result.one()
                except Exception as e:
                    print(f"Could not count patients: {e}", file=sys.stderr)
                    sys.exit(4)

            print(f"Patient count: {count}")
    except Exception as e:
        print(f"Database query failed: {e}", file=sys.stderr)
        sys.exit(5)


if __name__ == "__main__":
    main()
