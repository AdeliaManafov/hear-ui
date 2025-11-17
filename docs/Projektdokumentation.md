# HEAR‑Projekt — MVP, Features & Zeitplan

Kurzbeschreibung:
Eine Webanwendung zur Unterstützung ärztlicher Entscheidungen bei Cochlea‑Implantaten. Die Anwendung liefert eine Vorhersage zur Erfolgswahrscheinlichkeit, erklärt die Vorhersage (z. B. mit SHAP) und ermöglicht klinisches Feedback.

"Wir bauen ein schlankes Web‑MVP, das klinische Entscheidungen zur Cochlea‑Implantation unterstützt: Ein FastAPI‑Backend liefert kalibrierte Wahrscheinlichkeiten und SHAP‑basierte Erklärungen; das Frontend visualisiert die Vorhersage und sammelt klinisches Feedback. Ziel der nächsten zwei Wochen: funktionierender End‑to‑end‑Flow (Eingabe → Vorhersage → Erklärung) mit dokumentierter API und reproduzierbarer Dev‑Umgebung."

---

## Inhaltsverzeichnis

- [Ziel des Projekts](#ziel-des-projekts)
- [Kurzüberblick / MVP](#kurzuberblick-mvp)
- [Komponenten](#komponenten)
- [Werkzeuge - Übersicht](#werkzeuge-uebersicht)
- [Zeitplan](#zeitplan)
- [Betrieb & Entwicklung](#betrieb-entwicklung)
- [Datenschutz, Sicherheit und ethische Vorgaben](#datenschutz-ethik)
- [Demo‑Plan](#demo-plan)
- [Fragen](#fragen)

---

<a id="ziel-des-projekts"></a>
## Ziel des Projekts

Ziel ist ein schnell einsatzfähiges MVP für klinische Unterstützung: Eingabe → Vorhersage → Erklärung. 

Persistenz von Feedback und erweiterte Features folgen schrittweise.

---

<a id="kurzuberblick-mvp"></a>
## Kurzüberblick / MVP (konkret)

Für das MVP konzentrieren wir uns auf einen klaren End-to-End-Flow:

 - Frontend-Formular, also die Eingabe: Der Nutzer füllt ein Formular im Frontend aus.
 
 - Predict-Endpoint in FastAPI, also die Vorhersage: Das Backend (FastAPI) berechnet eine Vorhersage für den Erfolg des Cochlea-Implantats.

 - Vorhersage + SHAP-basierte Erklärung, also das System zeigt zusätzlich, welche Faktoren die Vorhersage beeinflusst (z. B. SHAP-Ranking oder Barplot).

 - Feedback speichern in PostgreSQL: Der Nutzer kann zustimmen oder ablehnen, und das Feedback wird in der Datenbank gespeichert.

=> Ziel: Damit können wir bereits echte Ergebnisse zeigen, auch wenn noch nicht alle Features ausgebaut sind.

**To sum it up:**

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
| MS2 (Prototype 1) | 2025‑11‑28 |H1 – Backend: Predict + Feedback (Sprint ist stark backend-fokussiert, um den MVP-Flow fertigzustellen)|
| MS3 (Prototype 2) | 2025‑12‑19 |H2 – Model & Explainability(SHAP) - sobald wir das Modell erhalten|
| MS4 (Release Prep) | 2026‑01‑23|H3 – Frontend- & DevOps-Erweiterungenx|
| Final Deliverable | 2026‑02‑27 | Abgabe aller Artefakte |

---

<a id="betrieb-entwicklung"></a>
## Betrieb & Entwicklung (Kurzhinweise)

Lokale Entwicklung:
- Backend (Server): uvicorn app.main:app --reload (API: http://127.0.0.1:8000) -> Die API‑Dokumentation ist unter: http://127.0.0.1:8000/docs
- Frontend: npm run dev (Vite) (Frontend: z. B. http://localhost:5173)

---

<a id="datenschutz-ethik"></a>
## Datenschutz, Sicherheit und ethische Vorgaben

1. Nur pseudonymisierte Daten in der Entwicklung verwenden:
    
    - Keine echten Patient:innen-Daten in deinem lokalen Backend oder Frontend.
    - Stattdessen Dummy-Daten oder anonymisierte Testdaten nutzen.

2. Keine Patient:innen-Identifiers in Logs oder Testdaten:
    - (E-Mail-Adressen), Namen oder andere persönliche Daten nicht ins Log schreiben.
    - Testdaten sollten generisch sein (user1@example.com, Test Patient).

3. Audit-Logging, Einwilligung, Zugriffskontrollen:
    - Wer darf Daten einsehen oder ändern?
    - Wer darf Feedback abgeben?
    - Für die MVP-Phase reicht ein einfaches Rollenmodell (Admin / User).

4. Secrets sicher speichern:
    - Alles, was sicherheitsrelevant ist (Passwörter, Tokens, API-Keys), in einer .env Datei ablegen.
    - Für CI/CD z. B. GitHub Actions Secrets verwenden.

5. Beispiel .env:
    - Enthält DB-Zugangsdaten, Superuser-Konto, SECRET_KEY, ENV etc.
    - Wird nicht ins Git-Repo eingecheckt (Gitignore).

---

<a id="demo-plan"></a>
## Demo‑Plan

→ Aktuell gibt der Vorhersage‑Endpunkt fiktive, beispielhafte Werte zurück, damit die App demonstriert werden kann. Später werden diese durch echte Modell‑Ergebnisse und echte Erklärungen (SHAP) ersetzt.

1. Backend starten (lokal): uvicorn app.main:app --reload
    
    → Zweck: Uvicorn startet den FastAPI‑Server, damit Endpunkte erreichbar sind

    → Der Server läuft standardmäßig auf http://127.0.0.1:8000

2. OpenAPI/ Swagger öffnen: http://127.0.0.1:8000/docs
   
    → In Swagger siehst du alle Endpunkte, erwartete JSON‑Schemas und kannst die Anfrage direkt aus dem Browser senden

3. POST /api/v1/predict/ mit Beispielpayload ausführen
    
    → Testaufruf des Predict‑Endpoints mit Beispiel‑Daten
    
    → Beispiel‑curl:
       
            
            curl -sS -X POST -H "Content-Type: application/json" \
              -d '{"age":45,"hearing_loss_duration":5.2,"implant_type":"typeA"}' \
              http://127.0.0.1:8000/api/v1/predict/ -w '\n%{http_code}\n'
            
        -sS : stille Ausgabe, aber zeige Fehler.
        -X POST : HTTP‑Methode POST.
        -H "Content-Type: application/json" : Sagt dem Server, dass der Body JSON ist.
        -d '{"..."}' : Der JSON‑Payload mit den Eingabe‑Features.
        -w '\n%{http_code}\n' : Am Ende zusätzlich den HTTP‑Statuscode ausgeben.

4. Ergebnis + SHAP‑Plot zeigen; Feedback absenden und DB‑Speicherung prüfen
    
    → Vorhersage: 0.45399999999999996 → ca. 45.4% Wahrscheinlichkeit für „erfolgreiches Ergebnis“.

    Erklärung (Feature‑Beiträge):
    - age: -0.01 → das Alter zieht die Vorhersage um −0.01 (−1.0 Prozentpunkte) nach unten.
    - hearing_loss_duration: 0.069 → längere Hörverlustdauer erhöht Vorhersage um +0.069 (+6.9 Prozentpunkte).
    - implant_type: -0.025 → der Implantat‑Typ zieht die Vorhersage um −0.025 (−2.5 Prozentpunkte) nach unten.

---

<a id="fragen"></a>
## Fragen

- Wann bekommen wir das KI-Modell?
- Wann bekommen wir die Beispiele von Patientendaten?

---