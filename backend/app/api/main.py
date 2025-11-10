# app/main.py

from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title="HEAR Backend")

# Alle Endpoints registrieren
app.include_router(api_router)
