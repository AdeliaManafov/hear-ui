# backend/app/api

Dieser Ordner enthält die API-spezifischen Module und Router für die Anwendung.

Inhalt & Hinweis:
- Einzelne Endpunkt-Gruppen liegen typischerweise in separaten Dateien oder Subpaketen.
- Verwende vorhandene Abhängigkeiten und `deps.py`-Module, um gemeinsame Abhängigkeiten (DB, Auth) zu injizieren.

Tipp: Änderungen an den API-Schemata erfordern ggf. ein Update des OpenAPI-Schemas, welches vom Frontend-Client genutzt wird.

Siehe `backend/README.md` für lokale Entwicklung und Test-Anleitungen.
