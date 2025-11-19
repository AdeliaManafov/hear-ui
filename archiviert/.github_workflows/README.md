# Archivierte GitHub Workflows

Diese Dateien wurden am 2025-11-19 archiviert, um CI‑Laufzeiten und Komplexität für das MVP zu reduzieren.

Was ist hier:

- `playwright.yml` — Original Playwright E2E workflow.
- `generate-client.yml` — Original workflow zur automatischen Generierung des Frontend‑Clients.

Warum archiviert:

- Playwright E2E‑Jobs sind zeit‑ und ressourcenintensiv. Für das frühe MVP werden sie nicht automatisch in CI ausgeführt.
- Die automatische Client‑Generierung kann PRs komplizieren und war für das MVP nicht nötig; die generierten Dateien wurden statt dessen ebenfalls archiviert.

Wie wiederherstellen:

1. Kopiere die gewünschte Workflowdatei zurück nach `.github/workflows/`:

```bash
git mv archiviert/.github_workflows/playwright.yml .github/workflows/playwright.yml
git add .github/workflows/playwright.yml
git commit -m "Restore Playwright workflow"
git push
```

2. Optional: Wenn die Client‑Generierung wieder aktiviert wird, stelle sicher, dass notwendige Secrets und Runner‑Ressourcen verfügbar sind.

Hinweis: Die Inhalte bleiben im Git‑Verlauf erhalten; diese Archivkopie ist vor allem zur schnellen Wiederherstellung gedacht.