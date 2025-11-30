# HEAR‑Projekt — MVP, Features & Zeitplan

Kurzbeschreibung:
Eine Webanwendung zur Unterstützung ärztlicher Entscheidungen bei Cochlea‑Implantaten. Die Anwendung liefert eine Vorhersage zur Erfolgswahrscheinlichkeit, erklärt die Vorhersage (z. B. mit SHAP) und ermöglicht klinisches Feedback.

## Wichtigste Befehle (kurz)

Hier sind die wichtigsten Kommandos für Entwicklung, Demo und Betrieb. Weiter unten im Dokument noch einmal komplett in Kontext vorhanden.

- **`cd hear-ui`**
- **`docker compose up -d --build`**
- **`docker compose down`**
- **`docker compose logs --follow --tail 200 backend`**
- **`curl -v http://localhost:8000/api/v1/utils/health-check/`**
- **`PGPASSWORD=change_me psql -h localhost -p 5433 -U postgres -d app`**
- **`docker compose exec backend alembic upgrade head`**
- **`docker cp mydata.csv hear-ui-db-1:/tmp/mydata.csv`**
- **`docker exec -it hear-ui-db-1 psql -U postgres -d app -c "\copy patients FROM '/tmp/mydata.csv' WITH (FORMAT csv, HEADER true)"`**


---

## Inhaltsverzeichnis

- [Ziel des Projekts](#ziel-des-projekts)
- [Kurzüberblick / MVP](#kurzuberblick-mvp)
- [Komponenten](#komponenten)
- [Werkzeuge - Übersicht](#werkzeuge-uebersicht)
- [API-Endpunkte](#api-endpunkte-übersicht)
- [Zeitplan](#zeitplan)
- [Demo](#how-to-demo)
- [Aktueller System-Status](#system-status)
- [Aktueller Projektstand](#aktueller-projektstand-stand-30112025)

---

<a id="ziel-des-projekts"></a>
## Ziel des Projekts

Ziel ist ein schnell einsatzfähiges MVP für klinische Unterstützung: Eingabe → Vorhersage → Erklärung. 

Persistenz von Feedback und erweiterte Features folgen schrittweise.

---

<a id="kurzuberblick-mvp"></a>
## Kurzüberblick / MVP (konkret)

Für das MVP konzentrieren wir uns auf einen klaren End-to-End-Flow:

  - Frontend: Formular zum Eingeben einer Person (Patientendaten).
  - Backend: 
      - Predict‑Endpoint (POST /api/v1/predict) → gibt Wahrscheinlichkeit + Label zurück.
      - SHAP‑Erklärungen → strukturierte SHAP‑Werte (JSON) oder base64‑Plot.
      - Feedback‑Endpoint (POST /api/v1/feedback) → persistiert Feedback in Postgres.
  - Datenpersistenz: Postgres speichert Feedback + ggf. Patienten/Tabelle. CSV‑Import nur fürs initiale Seeding möglich.
  - Reproduzierbarkeit: komplette Umgebung per docker-compose.

=> Ziel: Damit können wir bereits echte Ergebnisse zeigen, auch wenn noch nicht alle Features ausgebaut sind.

**Zusammenfassung:**

  Der minimale Funktionsumfang enthält:
      - ein valides Eingabeformular im Frontend
      
      - einen funktionierenden Predict-Endpoint
      
      - eine einfache Erklärung (z. B. SHAP-Ranking oder Barplot)
      
      - eine Feedback-Tabelle mit Storage in PostgreSQL
      
      - ein reproduzierbares Setup über Docker-Compose

---

<a id="komponenten"></a>
## Komponenten (Kurz)

- Frontend: Eingabe, Ergebnisanzeige, Visualisierung, Feedback‑UI
- Backend: API, Modell‑Wrapper, Erklärungs‑Pipeline, Persistenz
- Datenbank: PostgreSQL für Feedback und Logs (Pseudonymisierung beachten)
- DevOps: Containerisierung, CI for tests & linting

---

<a id="werkzeuge-uebersicht"></a>
## Werkzeuge - Übersicht

<!-- Frontend: hellblau -->
<h3 style="background:#e6f7ff;padding:6px;border-left:6px solid #66b3ff">Frontend</h3>
<table>
  <thead>
    <tr style="background:#f0f8ff">
      <th>Tool</th>
      <th>Was es macht</th>
      <th>Warum wir es wählen</th>
      <th>Im Repo?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Vue 3 (konkrete Verison aus Vue.js)</td>
      <td>Frontend-JavaScript-Framework</td>
      <td>einfach zu lernen + unterstützt Komponenten, die die Darstellung von Vorhersagen, SHAP-Visualisierungen oder Feedback-Buttons modular machen + gut kombinierbar mit FastAPI über RESTful APIs</td>
      <td>Ja — das Frontend verwendet Vue 3 (siehe <code>frontend/package.json</code>)</td>
    </tr>
    <tr>
      <td>TypeScript</td>
      <td>Statische Typisierung für JS</td>
      <td>Wartbarkeit, frühere Fehlererkennung</td>
      <td>Ja — wird weiterverwendet</td>
    </tr>
    <tr>
      <td>Vite</td>
      <td>Build-Tool und Entwicklungsserver speziell für Frameworks wie Vue 3</td>
      <td>schnelleres Frontend-Development + einfache Integration mit Vue 3 + Produktion-ready (können die App einfach bauen und in Docker deployen)</td>
      <td>Ja — <code>frontend/package.json</code></td>
    </tr>
    <tr>
      <td>pnpm</td>
      <td>Paketmanager für JavaScript/TypeScript</td>
      <td>leichtgewichtiger, schnellerer und platzsparender für größere Projekte + wir verwenden pnpm in diesem Projekt</td>
      <td>Ja — `frontend/pnpm-lock.yaml` wurde erstellt und ist committed (pnpm ist das bevorzugte Tool für das Frontend).</td>
    </tr>
    <tr>
      <td>UI‑Library</td>
      <td>Komponenten‑Bibliothek für Vue + vorgefertigte, getestete Komponenten (Buttons, Inputs, Tabellen, Dialoge, Formulare, Layouts, Themes)</td>
      <td>Schneller Aufbau von konsistenten, zugänglichen UI‑Elementen</td>
      <td>Ja — im Frontend ist <code>@chakra-ui/react</code> als UI‑Bibliothek installiert (React‑UI).</td>
    </tr>
    <tr>
      <td>Playwright</td>
      <td>End-to-End (E2E) Testing-Framework, das Browser automatisiert steuert, um Webanwendungen zu testen (öffnet echte Browser und führt Aktionen wie ein echter Nutzer aus)</td>
      <td>App hat ein Frontend (React) + Backend (FastAPI)</td>
      <td>Ja — <code>@playwright/test</code> ist in <code>frontend/package.json</code> aufgeführt und es gibt eine <code>playwright.config.ts</code>.</td>
    </tr>
    <tr>
      <td>Vitest</td>
      <td>Testing-Framework für JavaScript/TypeScript (speziell für Vite-Projekte + Vue 3)</td>
      <td>schnell + kann zusammen mit Playwright für End-to-End-Tests genutzt werden</td>
      <td>Ja — Vitest ist als Frontend‑Unit‑Test‑Runner hinzugefügt.</td>
    </tr>
  </tbody>
</table>

<!-- Backend: hellgrün -->
<h3 style="background:#f0fff0;padding:6px;border-left:6px solid #6fdc6f">Backend und DB</h3>
<table>
  <thead>
    <tr style="background:#f7fff7">
      <th>Tool</th>
      <th>Was es macht</th>
      <th>Warum wir es wählen</th>
      <th>Im Repo?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>FastAPI</td>
      <td>Web‑Framework für APIs (Pydantic)</td>
      <td>OpenAPI, gute Performance, schnell entwickelbar</td>
      <td>Ja — Backend‑Projekt mit FastAPI ist vorhanden (siehe <code>backend/pyproject.toml</code>).</td>
    </tr>
    <tr>
      <td>PDM (Python Dependency Manager)</td>
      <td>Tool, um Python-Projekte zu verwalten + sorgt dafür, dass Entwicklungsumgebung stabil ist</td>
      <td>Wir haben ein FastAPI-Backend, Datenbank-Module (PostgreSQL, SQLModel), Testing-Frameworks → hilft sicherzustellen, dass alle diese Pakete in der richtigen Version verfügbar sind.</td>
      <td>Ja — genutzt in Docs/ run commands</td>
    </tr>
    <tr>
      <td>SQLModel</td>
      <td>Biblitohek für Datenbankenanbindung</td>
      <td>SQLModel: moderner Hybrid vs. SQLAlchemy (mehr manuell machen, für komplexere features), in SQLModel ist schon alles definiert, was man typischerweise in FastAPI-Projekten braucht. SQLModel = SQLAlchemy + Pydantic (bequemere Typen/Validierung in FastAPI)</td>
      <td>Ja — <code>backend/pyproject.toml</code></td>
    </tr>
    <td>Alembic</td>
      <td>saubere Verwaltung und Weiterentwicklung der Datenbank für spätere Zeit</td>
      <td>Datenbankverwaltung reproduzierbar, versioniert und weniger fehleranfällig → ohne Alembic würde im MVP zwar starten können, spätere Anpassungen/ neue features könnten aber schnell zum Problem werden</td>
      <td>Ja — Alembic ist im Backend eingerichtet. Die Compose/Container‑Runs verwenden die Datei <code>backend/alembic.ini</code> (diese wird ins Image kopiert und vom Startskript verwendet). Die Entwickler‑Referenz wurde nach <code>backend/app/alembic.ini.example</code> verschoben.</td>
    </tr>
    <tr>
      <td>Postgres</td>
      <td>Daten speichern und abrufen</td>
      <td>speichern der Nutzerdaten, Feedbacks + persistente Daten für Modell-Erklärungen (wenn zb SHAP-Ergebnisse langfristig speichern) + Unterstützung für Webanwendung (Backend ruft DB ab, Frontend zeigt Daten an, REST-API greift auf die DB zu)</td>
      <td>Ja — DB‑Treiber (<code>psycopg</code>, <code>asyncpg</code>) sind als Abhängigkeiten im Backend gelistet; <code>docker-compose.yml</code> enthält einen Postgres‑Dienst.</td>
    </tr>
    <tr>
      <td>Adminer?</td>
      <td>Web‑GUI für Datenbanken; schnell Tabellen/Zeilen prüfen; SQL‑Queries ausführen oder Debugging von Daten</td>
      <td>Für Debug/Demo; zum visuellen Prüfen nutzen</td>
      <td>Im Browser: http://localhost:8080</td>
    </tr>
  </tbody>
</table>

<!-- Models & Explainability: gelb -->
<h3 style="background:#fff7e6;padding:6px;border-left:6px solid #ffcc66">Modelle und Explainability</h3>
<table>
  <thead>
    <tr style="background:#fffaf0">
      <th>Tool / Typ</th>
      <th>Was es macht</th>
      <th>Warum wir es wählen</th>
      <th>Im Repo?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SHAP</td>
      <td>Framework zur Erklärung von Modellvorhersagen, sowohl lokal (einzelner Patient) als auch global (alle Patienten)</td>
      <td>klinisch verständliche Feature‑Ranglisten + Ärzte können nachvollziehen, warum die KI eine Operation empfiehlt oder nicht</td>
      <td>Ja — <code>shap</code> wurde als Backend‑Dependency hinzugefügt und der Predict‑Endpoint nutzt SHAP (mit Fallback, falls die Laufzeitumgebung SHAP nicht verfügbar ist).<br/>
      Hinweis: <strong>NumPy ist Pflicht</strong> für SHAP und das Modell‑Handling, weil:<ul>
        <li>Modelle Input‑Daten als NumPy‑Arrays erwarten.</li>
        <li>SHAP intern NumPy verwendet und ohne NumPy nicht funktioniert.</li>
        <li>Viele Datenvorbereitungsschritte (Skalierung, Vektorisierung) NumPy nutzen.</li>
      </ul>
      Status: <em>NumPy wurde bereits installiert</em> (falls die Laufzeitumgebung diese Abhängigkeit hat, nutzt der Endpoint echte SHAP‑Erklärungen; andernfalls greift der vorhandene Fallback).</td>
    </tr>
  </tbody>
</table>

<!-- Tests & Quality: rosa -->
<h3 style="background:#fff0f6;padding:6px;border-left:6px solid #ff99cc">Verbesserung der Code‑Qualität + Tests</h3>
<table>
  <thead>
    <tr style="background:#fff8fb">
      <th>Tool</th>
      <th>Was es macht</th>
      <th>Warum wir es wählen</th>
      <th>Im Repo?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Ruff (Backend: Python, FastAPI)</td>
      <td>überprüft Python-Code automatisch auf Stil-, Syntax- und Qualitätsprobleme</td>
      <td>hilft, die Codequalität und Lesbarkeit zu verbessern + automatisiert die Überprüfung in CI/CD-Pipelines</td>
      <td>Ja — <code>ruff</code> ist als Dev‑Dependency im Backend‑Projekt konfiguriert (<code>backend/pyproject.toml</code>).</td>
    </tr>
    <tr>
      <td>Eslint (Frontend: Vue.js, TypeScript)</td>
      <td>JavaScript/TypeScript-Linter für Frontend-Code (zB Vue.js)</td>
      <td>überprüft JavaScript/TypeScript-Code auf Syntax- und Stilprobleme</td>
      <td>Ja — ESLint ist konfiguriert; siehe <code>frontend/.eslintrc.cjs</code> und <code>frontend/package.json</code>.</td>
    </tr>
    <tr>
      <td>Unit‑Test</td>
      <td>einzelne Funktionen/Methoden isoliert prüfen (zB Datenvalidierung, kleine Utils, Modell‑Preprocessing)</td>
      <td>Tool: Pytest (Backend), Vitest (Frontend components)</td>
      <td>Ja — <code>pytest</code> ist als Dev‑Dependency im Backend vorhanden; Vitest ist im Frontend eingerichtet.</td>
    </tr>
    <tr>
      <td>Integrationstests</td>
      <td>mehrere Komponenten zusammen testen (zB DB + API + Modell‑Wrapper)</td>
      <td>Tool: Pytest with testcontainers or local docker postgres</td>
      <td>Teilweise — Backend hat Test‑Dependencies (pytest); <code>testcontainers</code> ist nicht offensichtlich in den Abhängigkeiten.</td>
    </tr>
    <tr>
      <td>End‑to‑End</td>
      <td>kompletter Nutzer‑Flow (Frontend + Backend + DB) aus Sicht des Nutzers testen</td>
      <td>Tool: Playwright (cross‑browser), ideal für Demo‑Regressionen</td>
      <td>Ja — Playwright ist im Frontend konfiguriert (<code>@playwright/test</code>, <code>playwright.config.ts</code>).</td>
    </tr>
    <tr>
      <td>pytest</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

<!-- DevOps & CI: grau -->
<h3 style="background:#f7f7f7;padding:6px;border-left:6px solid #cfcfcf">DevOps & CI</h3>
<table>
  <thead>
    <tr style="background:#fafafa">
      <th>Tool</th>
      <th>Was es macht</th>
      <th>Warum wir es wählen</th>
      <th>Im Repo?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Docker-Container mittels docker‑compose</td>
      <td>Verpackt alle Projektkomponenten (Backend, Frontend, Datenbank) in isolierte Container und docker-compose orchestriert diese Container lokal oder auf Servern</td>
      <td>Jeder Entwickler/ CI-Server nutzt exakt dieselbe Umgebung</td>
      <td>Ja — <code>docker-compose.yml</code></td>
    </tr>
    <tr>
      <td>GitHub Actions</td>
      <td>Automatisiert Abläufe wie Linting, Unit-Tests, Integrationstests und Build-Prozesse und wird bei Pull Requests oder Releases automatisch ausgeführt</td>
      <td>Qualitätssicherung: Prüft, dass Code vor dem Merge oder Deployment fehlerfrei ist + Automatisierung: Entwickler müssen Tests oder Builds nicht manuell starten</td>
      <td>Ja — <code>.github/workflows/</code></td>
    </tr>
  </tbody>
</table>

---

<a id="zeitplan"></a>
## Zeitplan (Milestones)

| Meilenstein | Datum | Kurzbeschreibung |
|---|---:|---|
| Setup Meeting | 2025‑10‑29 |  |
| MS1 (MVP) | 2025‑11‑14 | |
| MS2 (Prototype 1) | 2025‑11‑26 |H1 – Backend: Predict + Feedback (Sprint ist stark backend-fokussiert, um den MVP-Flow fertigzustellen)|
| MS3 (Prototype 2) | 2025‑12‑19 |H2 – Model & Explainability(SHAP) - sobald wir das Modell erhalten|
| MS4 (Release Prep) | 2026‑01‑23|H3 – Frontend- & DevOps-Erweiterungen|
| Final Deliverable | 2026‑02‑27 | Abgabe aller Artefakte |

---

<a id="how-to-demo"></a>
## Demo (Skript + Beispielausgaben)

Verwende die folgenden Befehle während der Präsentation, um den kompletten Ablauf zu demonstrieren: Dienste starten, Gesundheitscheck, einzelne Vorhersage, Ergebnis persistieren, Feedback anlegen und wieder auslesen. Alle Befehle gehen davon aus, dass das Backend unter `http://localhost:8000` erreichbar ist.

- Speichere das folgende Skript als `demo.sh` und mache es ausführbar (`chmod +x demo.sh`). Es führt die Sequenz aus und gibt die wichtigsten Ergebnisse aus.

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:8000}

echo "1) Gesundheitscheck"
curl -sS "$BASE_URL/api/v1/utils/health-check/" | jq

echo "\n2) Einzelne Vorhersage (nicht persistiert)"
curl -sS -X POST "$BASE_URL/api/v1/predict/" \
  -H "Content-Type: application/json" \
  -d '{"age":55, "hearing_loss_duration":12.5, "implant_type":"type_b"}' | jq

echo "\n3) Einzelne Vorhersage (persist=true) — Ergebnis wird persistiert, falls DB/Migrationen vorhanden sind"
curl -sS -X POST "$BASE_URL/api/v1/predict/?persist=true" \
  -H "Content-Type: application/json" \
  -d '{"age":55, "hearing_loss_duration":12.5, "implant_type":"type_b"}' | jq

echo "\n4) Feedback erstellen (ID speichern)"
RESP=$(curl -sS -X POST "$BASE_URL/api/v1/feedback/" \
  -H "Content-Type: application/json" \
  -d '{"input_features": {"age": 55}, "prediction": 0.23, "accepted": true}')
echo "$RESP" | jq
ID=$(echo "$RESP" | jq -r '.id')
echo "Gespeicherte Feedback-ID: $ID"

echo "\n5) Feedback nach ID lesen"
curl -sS "$BASE_URL/api/v1/feedback/$ID" | jq

echo "\nDemo-Skript beendet. Falls etwas fehlschlägt, prüfe die Logs: docker compose logs -f backend"
```

Beispielausgaben (aus einem lokalen Lauf):

- Gesundheitscheck

```json
{ "status": "ok" }
```

- Vorhersage (einzelner Aufruf)

```json
{
  "prediction": 0.26499999999999996,
  "explanation": {
    "age": -0.030000000000000027,
    "hearing_loss_duration": -0.14999999999999997,
    "implant_type": 0.024999999999999967
  }
}
```

- Feedback erstellen (Antwort)

```json
{
  "id": "e7c6cadb-05bf-4c3b-986e-dc2881845251",
  "input_features": {"age": 55},
  "prediction": 0.23,
  "accepted": true,
  "explanation": null,
  "comment": null,
  "user_email": null,
  "created_at": "2025-11-19T16:54:38.825949"
}
```

Gespeicherte Feedback‑IDs für den Offline‑Fallback (falls die Demo‑DB nicht beschreibbar ist):

- `e7c6cadb-05bf-4c3b-986e-dc2881845251`

Falls die Demo‑Umgebung ausfällt, Fallback‑Schritte:

- Dienste neu starten:

```bash
docker compose up --build -d
docker compose logs -f backend
```

- Schnelle manuelle Prüfungen:

```bash
curl -sS http://localhost:8000/api/v1/utils/health-check/ | jq
curl -sS -X POST http://localhost:8000/api/v1/predict/ -H "Content-Type: application/json" -d '{"age":55,"hearing_loss_duration":12.5,"implant_type":"type_b"}' | jq
```

---

<a id="system-status"></a>
## Aktueller System-Status
Docker läuft im Kontext colima. 

Docker Compose wurde ausgeführt; folgende Services sind erreichbar:
  - Frontend: http://localhost:5173

  - Adminer (DB GUI): http://localhost:8080

  - Backend-API: http://localhost:8000

      - Health: http://localhost:8000/api/v1/utils/health-check/

      - Liste Patienten über die API (wenn Backend läuft): curl http://localhost:8000/api/v1/patients/

      - Docs (Swagger): http://localhost:8000/docs

  - Postgres (Hostzugriff): localhost:5433 → DB app, User postgres (Standard‑Passwort im Repo: change_me oder aus .env)

prestart-Container lief durch (führt Migrationen / initial data aus) und hat sich beendet.

**→ Kurzbefehle:**

| Aktion | Befehl |
|--------|--------|
| Compose starten | `cd hear-ui && docker compose up -d --build` |
| Compose stoppen | `docker compose down` |
| Logs prüfen | `docker compose logs --follow --tail 200 backend` |
| Health testen | `curl -v http://localhost:8000/api/v1/utils/health-check/` |
| Migrationen | `docker compose exec backend alembic upgrade head` |
| CSV importieren | `docker cp mydata.csv hear-ui-db-1:/tmp/mydata.csv` |

---

## API-Endpunkte (Übersicht)

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `POST` | `/api/v1/predict/` | Direkte Vorhersage |
| `POST` | `/api/v1/patients/upload` | CSV-Upload |
| `GET` | `/api/v1/patients/` | Patientenliste |
| `GET` | `/api/v1/patients/{id}` | Patient-Details |
| `GET` | `/api/v1/patients/{id}/predict` | Vorhersage für Patient |
| `GET` | `/api/v1/patients/{id}/explainer` | SHAP-Erklärung für Patient |
| `GET` | `/api/v1/patients/{id}/validate` | Patientendaten validieren |
| `POST` | `/api/v1/explainer/explain` | Direkte SHAP-Erklärung |
| `POST` | `/api/v1/feedback/` | Feedback erstellen |
| `GET` | `/api/v1/feedback/{id}` | Feedback lesen |
| `GET` | `/api/v1/utils/health-check/` | Gesundheitscheck |
| `GET` | `/api/v1/utils/model-info/` | Modell-Informationen |
| `GET` | `/api/v1/utils/feature-names/` | Feature-Namen |
| `GET` | `/api/v1/utils/feature-categories/` | Feature-Kategorien |

---

 ## Aktueller Projektstand (Stand: 30.11.2025)

      Kurz zusammengefasst: Das Backend (API, Modellintegration, SHAP-Erklärungen, Feedback-Persistenz) ist implementiert und lokal in Containern lauffähig; es existiert eine umfangreiche Test‑ und Dokumentationsbasis. Das Frontend ist in Arbeit.

      **Test-Status:**
      - ✅ 164 Tests bestanden (100%)
      - ⏭️ 2 Tests übersprungen
      - 📊 82% Code-Coverage

      **Patientendaten:**
      - 33 Patienten in der Datenbank (davon 17 mit vollständigen Daten für SHAP)
      - 5 echte Patienten aus `Dummy Data_Cochlear Implant.csv` importiert
      - Vorhersage-Bereich: 22.1% - 100.0%

      Erledigtes (wichtigste Punkte):
      - Backend-API mit Endpunkten für Prediction, SHAP-Explanations, Feedback und Health (`/api/v1/...`) ist implementiert.
      - ML‑Pipeline geladen: `logreg_best_model.pkl` (LogisticRegression mit 68 Features nach One-Hot-Encoding).
      - SHAP Explainability (Koeffizient-basiert) ist integriert; synthetische Background-Samples vorhanden.
      - Feedback‑Persistenz in PostgreSQL und Alembic‑Migrationen sind eingerichtet.
      - Docker‑Compose Setup mit Backend, Frontend, Postgres und Adminer ist vorhanden; `demo.sh` automatisiert eine einfache End‑to‑End‑Demonstration.
      - Tests: Backend‑Unit‑ und Integrationstests (Pytest) sind vorhanden und wurden ausgeführt (164 Tests); Test‑Scripts für Batch‑Verarbeitung liegen bei.
      - Linter/Qualitätswerkzeuge (Ruff, ESLint) und erste CI/Workflow‑Konfigurationen sind vorhanden.
      - Pydantic V2 Migration abgeschlossen.
      - FastAPI Lifespan Events implementiert (keine Deprecation-Warnungen).

      Offene Aufgaben / Nächste Schritte (priorisiert):
      1. Frontend‑MVP fertigstellen: UI‑Formular, Anzeige der Vorhersage, SHAP‑Visualisierungen (Top‑5 Balken), Feedback‑UI.
      2. Feature‑Name‑Mapping: Technische Feature‑Bezeichnungen (`cat__...`, `num__...`) für Anwender in verständliche Labels übersetzen (Backend‑Endpoint oder Frontend‑Mapping-Datei).
      3. E2E‑Tests ergänzen: Playwright‑Szenarien, die Formular → Predict → SHAP → Feedback prüfen, und in CI integrieren.
      4. Integrationstests mit DB: Robustere Tests (z. B. Testcontainers oder CI Postgres) sicherstellen, dass Feedback persistiert wird.
      5. SHAP Background vergrößern: Aktuell kleines Background‑Sample (5 echte / 100 synthetische); Ziel: 50–100 echte, vollständige Patienten für stabilere Erklärungen.
      6. Modell‑Kalibrierung prüfen/aktivieren: Sicherstellen, dass `logreg_calibrated.pkl` in der Produktionskonfiguration verwendet und getestet wird.
      7. Security & Privacy: Authentifizierung (JWT), TLS/HTTPS, Pseudonymisierung‑Policy dokumentieren und ggf. implementieren (Feedback‑Endpoint derzeit offen).
      8. Monitoring & Logging: Metriken (Prometheus/Grafana), Request‑Logs, Alerts für Model‑Drift und Fehler einrichten.
      9. CI/CD vervollständigen: Workflows so konfigurieren, dass Lint, Tests, Alembic‑Migrations und optional E2E laufen.
      10. Dokumentation & Readme: README kürzen / strukturieren (Quick‑Start, MVP‑Scope prominent) — bereits teilweise erledigt; abschließende Review und Link‑Badges ergänzen.



      ---

1. Backend per Docker Compose starten: **docker compose up --build**

          → startet alle in docker-compose.yml definierten Services und führt sie im Hintergrund aus. Alles lokal erreichbar.
          → Docker läuft in Colima.
          → **Frontend öffnen:** http://localhost:5173 — UI demonstrieren (Eingabeformular → Vorhersage).
          → **API Docs:** http://localhost:8000/docs (Swagger) — Endpunkte zeigen (Predict, Feedback, Health).
          → **Health-Check:** curl -sS http://localhost:8000/api/v1/utils/health-check/ | jq — Belegt, dass Backend läuft. (Erwartet: {"status":"ok"} und Swagger‑UI erreichbar)
          → **Live‑API-Call:** Ein curl-Beispiel zur Vorhersage zeigen (zeigt Input → Output + SHAP).
          → **DB‑GUI (Adminer):** http://localhost:8080 — gespeicherte Feedback‑Einträge/Tabellen zeigen.
          → **Logs & Migrationen:** docker compose logs -f backend + evtl. alembic upgrade head — Debug/State sichtbar machen.
          → **Fallbacks demonstrieren: Falls Live‑Demo scheitert: Screencast/Video oder gespeicherte curl-Responses zeigen.

---

## Demo für MS1 — Exakte Patient‑IDs & How‑to‑Run (kurz)

Die folgenden Befehle sind für die Live‑Demo vorbereitet. Ersetze dabei `<PATIENT_ID>` immer durch die echte UUID.

### Wichtige Patient‑IDs (mit gefüllten `input_features`, nutzbar für SHAP)

**Echte Patienten aus CSV (ID 1-5):**
- `9c4408e6-2aef-44c1-ae95-dd409141f647` (Patient 1 - prälingual, 97.3%)
- `86bab602-7ffc-4663-aced-567905bed3bd` (Patient 2 - postlingual, 100%)
- `2b7414f6-471a-4bf8-8998-1385543a40b3` (Patient 3 - prälingual/syndromal, 22.1%)
- `21bfdee0-4207-4ac2-925d-b557f14ab39e` (Patient 4 - perilingual, 81.1%)
- `a9e0736c-05fb-490b-940b-b275be3158e3` (Patient 5 - prälingual, 97.3%)

**Test-Patienten mit vollständigen Daten:**
- `0b2cbc1c-d3bf-4da6-bb18-1ffd93705754`
- `e2813011-fc6d-4f3f-a115-9effacca28ed`
- `4f016e66-3bd2-4bcf-a7ff-70ee35002903`

```bash
# Alle Patienten-IDs aus Dummy Data_Cochlear Implant.csv
curl -sS "http://localhost:8000/api/v1/patients/" | jq -r '.[].id'

# Ganze Patientenliste aus Dummy Data_Cochlear Implant.csv
curl -sS "http://localhost:8000/api/v1/patients/" | jq
```


### Kurze Ablauf‑Anleitung 

1) Dienste starten

```bash
cd /Users/adeliamanafov/hearUI_project/hear-ui
docker compose up -d --build

# Laufende Container zeigen
docker compose ps
# Erwartung: backend, db (postgres) und adminer sind Up.
```

2) Health‑Check & API‑Docs

```bash
curl -sS http://localhost:8000/api/v1/utils/health-check/ | jq
# Swagger: open http://localhost:8000/docs
```

3) Alembic (falls Migrationen manuell nötig) via Container

Alembic führt die neuesten Datenbank-Migrationen aus

  - Ziel-Datenbank ist PostgreSQL
  - PostgreSQL unterstützt, dass Schema-Änderungen (CREATE TABLE, ALTER TABLE, DROP etc.) in einer Transaktion laufen.

```bash
docker compose exec backend alembic upgrade head
```

4) Schnelle ad‑hoc‑Vorhersage (spontane/ sofortige Vorhersage)

  - nur zurückgegeben, aber nicht automatisch gespeichert

```bash
curl -sS -X POST "http://localhost:8000/api/v1/predict/" \
  -H "Content-Type: application/json" \
  -d '{"age":55, "hearing_loss_duration":12.5, "implant_type":"type_b"}' | jq
```

Erwartet: JSON mit `prediction` (float) und `explanation` (Objekt oder `{}`, da erkläreungen extra in shap.py erzeugt werden als in Punkt 5).

5) Persistierte Vorhersage + Feedback (Beispiel)

  - Vorhersage wird zusätzlich in der Datenbank abgelegt, zusammen mit den Input-Daten, dem Zeitpunkt und ggf. der SHAP-Erklärung.

```bash
curl -sS -X POST "http://localhost:8000/api/v1/predict/?persist=true" \
  -H "Content-Type: application/json" \
  -d '{"age":55, "hearing_loss_duration":12.5, "implant_type":"type_b"}' | jq

RESP=$(curl -sS -X POST "http://localhost:8000/api/v1/feedback/" \
  -H "Content-Type: application/json" \
  -d '{"input_features": {"age": 55}, "prediction": 0.23, "accepted": true}')
echo "$RESP" | jq
ID=$(echo "$RESP" | jq -r '.id')
curl -sS "http://localhost:8000/api/v1/feedback/$ID" | jq
```

6) Patientenliste + Validate (SHAP‑geeignete Patienten auswählen)

```bash
curl -sS "http://localhost:8000/api/v1/patients/" | jq
curl -sS "http://localhost:8000/api/v1/patients/<PATIENT_ID>/validate" | jq
```

`validate` sollte `{"ok": true, "missing_features": []}` zurückgeben — dann ist der Patient SHAP‑geeignet.

7) SHAP-Erklärung für einen gespeicherten Patienten

```bash
curl -sS "http://localhost:8000/api/v1/patients/<PATIENT_ID>/explainer" | jq
```

Erwartet: `200 OK` und ein JSON mit `prediction`, `feature_importance`, `shap_values`, `top_features`.

8) Ad‑hoc SHAP (nur mit vollständiger JSON‑Datei)

```bash
curl -sS -X POST "http://localhost:8000/api/v1/explainer/explain" \
  -H "Content-Type: application/json" \
  -d '{"age": 45, "gender": "w", "primary_language": "Deutsch", "hearing_loss_onset": "postlingual"}' | jq
```

Hinweis: Ad‑hoc SHAP erfordert alle Pflichtfelder; nutze patient‑based SHAP (`/patients/{id}/explainer`) wenn möglich.

9) Logs & Live‑Debug

```bash
docker compose logs --follow --tail 200 backend
```

Typische Ursachen für Fehler (kurz):

- `Model not loaded` → Modelldatei fehlt oder Wrapper nicht geladen (`logreg_best_pipeline.pkl` / `logreg_calibrated.pkl`).
- `ValueError` beim Casten (z. B. `invalid literal for int()`): Mapping verschoben → `validate` und `input_features` prüfen.
- SHAP/NumPy ImportError: fehlende Abhängigkeiten.

10) Adminer / DB‑Zugriff

- Adminer (DB GUI): [http://localhost:8080](http://localhost:8080)

Host‑psql (wenn nötig):

```bash
PGPASSWORD=change_me psql -h localhost -p 5433 -U postgres -d app
```

  Formular ausfüllen (empfohlen, weil Adminer als Container im selben Docker‑Netz läuft):
  
    - System: PostgreSQL
    - Server: db
    - Username: postgres
    - Password: changeme_secure_password_here
    - Database (optional): hear_db (Adminer läuft in einem anderen Container, verbindet also über das Docker‑Netzwerk — dort ist der DB‑Host db (der Compose‑Dienstname).)
    
  Tabellenliste und Migration Status:

    docker compose exec db psql -U postgres -d hear_db -c "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;"

    docker compose exec db psql -U postgres -d hear_db -c "SELECT * FROM alembic_version;"

    => Was sieht man: Patient, Feedback, Vorhersage und Alembic-Version – Migrationen wurden angewendet.

  API und Datenbank sind synchronisiert – 33 Patienten (5 echte aus CSV + 28 Test-Patienten).



11) Fallback‑Artefakte (falls Live‑Demo scheitert)

Lege im Repo `docs/demo-fallback/` an und speichere dort:

- `predict_response.json` — Beispielantwort der Predict‑API
- `patient_shap_response.json` — Beispiel SHAP‑Antwort (für eine der obigen IDs)
- `feedback_response.json` — Beispiel für gespeichertes Feedback

```bash
# Predict live
curl -sS -X POST "http://localhost:8000/api/v1/predict/" \
  -H "Content-Type: application/json" \
  -d '{"Alter [J]": 45, "Geschlecht": "w", "Primäre Sprache": "Deutsch"}' | jq . > docs/demo-fallback/predict_response.json

# Patient SHAP-Erklärung (ersetze <PATIENT_ID>)
curl -sS "http://localhost:8000/api/v1/patients/<PATIENT_ID>/explainer" | jq . > docs/demo-fallback/patient_shap_response.json

# Feedback: create and save
RESP=$(curl -sS -X POST "http://localhost:8000/api/v1/feedback/" -H "Content-Type: application/json" -d '{"input_features":{"Alter [J]":55},"prediction":0.85,"accepted":true}')
echo "$RESP" | jq . > docs/demo-fallback/feedback_response.json
```

---