from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash.

    The original JWT helper was archived — this module now only provides
    password hashing utilities used by `crud` and user management.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Return the bcrypt hash for `password`.

    This keeps the active code small while the full token helpers are
    preserved in `archiviert/backend_auth/security.py`.
    """
    return pwd_context.hash(password)
