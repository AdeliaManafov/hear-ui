# app/__init__.py
# Re-export commonly used modules for convenience

from app.db import crud  # noqa: F401

__all__ = ["crud"]