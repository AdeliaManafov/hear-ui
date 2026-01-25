from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:  # noqa: ARG001
    """Initialize the database for local/test runs.

    In production migrations (Alembic) should be used. For tests and local
    development we create any missing tables automatically so test fixtures
    that rely on the DB schema can run.
    """
    from sqlmodel import SQLModel

    # Ensure all models have been imported (app.models should be imported
    # elsewhere before this is called).
    # In test/local runs we may need to drop & recreate tables to ensure the
    # schema matches current models; guard this behind the TESTING flag so
    # production/staging runs don't accidentally drop data.
    from app.core.config import settings

    if getattr(settings, "TESTING", False):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    else:
        SQLModel.metadata.create_all(engine)
