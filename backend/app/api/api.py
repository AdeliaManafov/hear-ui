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
# Die Sub-Router definieren bereits ihre eigenen Prefixes (z.B. router = APIRouter(prefix="/utils")),
# daher hier keine doppelte Version-Teilpräfixe angeben. Die globale Version wird in app.include_router
# durch settings.API_V1_STR gesetzt.
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(items.router)
api_router.include_router(utils.router)
api_router.include_router(predict.router)

# Private-Router nur lokal verfügbar
if settings.ENVIRONMENT == "local" and private:
    # Der private Router definiert bereits sein eigenes Prefix ("/private").
    # Wir fügen hier keinen zusätzlichen Version-/Pfadpräfix hinzu,
    # da die globale API-Version in app.main mittels settings.API_V1_STR gesetzt wird.
    api_router.include_router(private.router)
