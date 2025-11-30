"""
Archived authentication routes.

The login/password related endpoints were intentionally removed from the
public API surface. This module now exposes an empty router so the
application import path remains stable but the endpoints do not appear
in the OpenAPI docs or route table.
"""

from fastapi import APIRouter

router = APIRouter(tags=["login"])

# No route definitions here — endpoints removed/archived.
