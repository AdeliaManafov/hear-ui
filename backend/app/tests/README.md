# backend/app/tests

Tests für das Backend.

Empfohlene Struktur:
- `conftest.py` für gemeinsame Test-Fixtures.
- `test_*.py` Dateien für Unit- und Integrationstests.

Tests ausführen:
- Lokal: `bash ./scripts/test.sh` vom `backend/`-Ordner aus.
- In CI: Pytest-Workflow ist konfiguriert (siehe GitHub Actions im Projekt-Root).

Tipp: Für Integrationstests, die DB oder externe Services benötigen, nutze die Docker-Compose-Test-Umgebung.
