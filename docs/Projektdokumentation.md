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
- [Zeitplan](#zeitplan)
- [Demo](#how-to-demo)
- [Aktueller System-Status](#system-status)

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
      <td>Ja — Alembic ist im Backend eingerichtet (siehe <code>backend/alembic.ini</code> und <code>backend/app/alembic/</code>).</td>
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

      - Compose hochfahren / neu bauen: cd hear-ui + docker compose up -d --build
      - Compose stoppen: docker compose down
      - Logs prüfen: docker compose logs --follow --tail 200 backend + docker compose logs --tail 200 frontend
      - Health testen: curl -v http://localhost:8000/api/v1/utils/health-check/
      - Alembic (Migrationen ausführen, im Container oder dev env): docker compose exec backend alembic upgrade head + # oder lokal im dev env: alembic upgrade head
      - CSV in Postgres importieren: docker cp mydata.csv hear-ui-db-1:/tmp/mydata.csv + docker exec -it hear-ui-db-1 psql -U postgres -d app -c "\copy patients FROM '/tmp/mydata.csv' WITH (FORMAT csv, HEADER true)"