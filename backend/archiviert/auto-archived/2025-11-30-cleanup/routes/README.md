# backend/app/routes

Sammelt die Router-Module, die die verschiedenen API-Endpunkte an die FastAPI-Anwendung anhängen.

Erwartetes Layout:
- Je ein Modul/Datei pro funktionalem Bereich (z. B. `predict.py`, `auth.py`).
- Zusammensetzung der Router erfolgt meist in `api`- oder `main`-Modulen.

Beim Hinzufügen neuer Routen: Export & Registrierung im Haupt-Router nicht vergessen.
