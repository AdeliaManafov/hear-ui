# Projekt-Dokumentation (Index)

Dieses Verzeichnis enthält die projektbezogenen Dokumente für das HEAR‑Projekt. Ziel: ein klarer Einstiegspunkt, der die wichtigsten Dokumente bündelt und veraltete/duplizierte Dateien archiviert.

Wichtige, aktive Dokumente

- `development.md` — Anleitung zum lokalen Entwickeln (Docker Compose, lokale Server, Logs, .env, pre-commit).
- `deployment.md` — Anleitung für die Produktion: Traefik, DNS, Remote-Server und CI/CD‑Hinweise.
- `ci-cd.md` — Empfehlungen und Beispiele für GitHub Actions (Lint, Tests, Build & Push).
- `SECURITY.md` — Sicherheitsrichtlinie und Vulnerability‑Reporting.
- `assignment-status.md` — Projektaufgabe, aktueller Status, To‑Do und empfohlene nächste Schritte (laufend gepflegt).

Bereichsspezifische READMEs

- `../backend/README.md` — Backend-spezifische Hinweise (Migrations, Tests, Entwicklungs-Workflows).
- `../backend/README-DEPS.md` — Hinweise zur Verwaltung und Sperrung von Python‑Dependencies.
- `../backend/SCRIPTS.md` — Kurzbeschreibung der vorhandenen Backend‑Skripte.
- `../frontend/README.md` — Frontend‑Entwicklung (Vite, npm, Playwright, Generate Client).

Archiv (duplizierte oder lange Vorlagen)

In `docs/archived/` liegen ältere, sehr ausführliche oder template‑basierte Dateien, die zur Referenz erhalten bleiben, aber nicht mehr aktiv gepflegt werden sollten. Beispiele:

- `sprint_plan_and_tech.md` — frühere Sprint‑Pläne / Tech‑Notizen (verschoben)
- `TODO.md` — historisches TODO (zusammengeführt in `assignment-status.md`, verschoben)
- `release-notes.md` — ausführliche Changelog/Template (verschoben)

Vorgehen bei Aktualisierungen

- Wenn du ein Doc änderst, aktualisiere kurz den Index hier. Bei größeren Änderungen: erstelle bitte eine separate, kurze Zusammenfassung im `assignment-status.md`.
- Wenn du unsicher bist, ob ein Doc noch aktiv ist: verschiebe es in `docs/archived/` statt zu löschen — so bleibt die Historie erhalten.

---

Wenn du möchtest, kann ich jetzt bei Bedarf die archivierten Dateien per Pull‑Request oder Commit löschen bzw. weitere Dateien konsolidieren (z. B. TODO → assignment‑status zusammenführen). Sag kurz, ob das Vorgehen so passt.
