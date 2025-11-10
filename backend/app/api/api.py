# app/api/api.py

from fastapi import APIRouter
from app.api.routes import items, login, users, utils, predict
from app.core.config import settings

# Optionaler Import des privaten Routers nur, wenn Datei existiert
try:
    from app.api.routes import private
except ImportError:
    private = None

api_router = APIRouter()

# Sub-Router einbinden
api_router.include_router(login.router, prefix="/api/v1/login", tags=["login"])
api_router.include_router(users.router, prefix="/api/v1/users", tags=["users"])
api_router.include_router(items.router, prefix="/api/v1/items", tags=["items"])
api_router.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])
api_router.include_router(predict.router, prefix="/api/v1/predict", tags=["prediction"])

# Private-Router nur lokal verfügbar
if settings.ENVIRONMENT == "local" and private:
    api_router.include_router(private.router, prefix="/api/v1/private", tags=["private"])
