# HEAR-UI Demo-Skript – Präsentation für Kliniker

**Zweck:** Videoaufnahme / Live-Demonstration für das klinische Team  
**Dauer:** ca. 8–12 Minuten  
**Sprache:** Deutsch (Oberfläche per Schalter auf DE gestellt)

---

## 0. Vorbereitung (nicht im Video)

- Browser öffnen → **http://localhost:5173** (oder Produktions-URL)
- Sprache auf **Deutsch** stellen (Sprachschalter oben rechts: 🌐 DE)
- Demo-Patienten vorhanden: *Muster, Anna* und *Schmidt, Maria*
- Lautsprecher/Mikrofon testen

---

## 1. Eröffnung (ca. 1 min)

> „Willkommen zu HEAR-UI – unserem KI-gestützten Entscheidungsunterstützungssystem
> für die Cochlea-Implantat-Versorgung. Das System hilft dem klinischen Team dabei,
> auf Basis von audiologischen und anamnestischen Daten eine Vorhersage zu treffen,
> ob ein Patient von einem CI voraussichtlich profitieren wird.
>
> Wichtig: HEAR-UI ersetzt keine ärztliche Entscheidung – es liefert einen
> zusätzlichen datenbasierten Hinweis als Unterstützung."

---

## 2. Modellkarte – Transparenz über das Modell (ca. 2 min)

**Navigation:** Seitenleiste → „Modellkarte" (oder `/model-card`)

> „Bevor wir Vorhersagen ansehen, schauen wir uns an, *was* das Modell eigentlich
> ist und wie verlässlich es ist."

**Zeigen und kommentieren:**

| Abschnitt | Was zu sagen |
|---|---|
| **Modellübersicht** | „Das Modell ist ein Random-Forest-Klassifikator, trainiert auf [N] CI-Patientendaten aus unserem eigenen Zentrum." |
| **Eingabe-Features** | „Es nutzt bis zu 21 klinisch relevante Merkmale: Alter, Geschlecht, Hördauer, Audiometrie-Werte u. v. m." |
| **Leistungsmetriken** | „Die Trennschärfe (AUC) beträgt [Wert] – das bedeutet, das Modell unterscheidet Profiteure von Nicht-Profitierende in ~[X]% der Fälle besser als der Zufall." |
| **Limitierungen** | „Das Modell wurde an unserem Patientenkollektiv trainiert. Übertragbarkeit auf andere Zentren muss noch validiert werden." |

> „Die Modellkarte ist versioniert – wir können immer nachvollziehen, welche
> Modellversion wann welche Metriken hatte."

---

## 3. Patientensuche & vorhandener Patient (ca. 2 min)

**Navigation:** Seitenleiste → „Patienten" → Suchfeld

> „Schauen wir uns eine bereits im System erfasste Patientin an."

**Eingabe im Suchfeld:** `Muster`

> „Anna Muster, 58 Jahre, weiblich – CI auf der rechten Seite, Hörverlust seit
> 12 Jahren. Diese Daten wurden aus unserer klinischen Tabelle importiert."

**Auf den Patient klicken → Detailansicht**

> „Im Profil sehen wir alle erfassten klinischen Parameter."

---

## 4. Vorhersage anzeigen (ca. 1 min)

**In der Patientenansicht:** Button „Vorhersage berechnen" (oder `/patients/{id}/predict`)

> „Mit einem Klick berechnet das System die Wahrscheinlichkeit eines CI-Erfolgs.
> Bei Frau Muster ergibt sich ein Wert von beispielsweise **0.72** – das heißt,
> das Modell schätzt eine ~72 % Wahrscheinlichkeit für ein gutes Ergebnis."

> „Der Wert allein sagt noch nicht alles. Deshalb schauen wir uns auch die
> Erklärung an."

---

## 5. SHAP-Erklärung / Feature Importance (ca. 2 min)

**Button „Erklärung anzeigen"** (oder `/patients/{id}/explainer`)

> „Das Wasserfall-Diagramm zeigt, welche Faktoren die Vorhersage nach oben
> oder unten verschoben haben."

**Konkret erklären:**

> „Die roten Balken erhöhen die Wahrscheinlichkeit – zum Beispiel das Alter
> von 58 Jahren und ein Hörverlust, der erst vor wenigen Jahren begann.
> Die blauen Balken wirken absenkend – hier etwa das Ausmaß des Verlusts
> im kontralateralen Ohr."

> „Als Kliniker kann ich so nachvollziehen, warum das Modell zu diesem
> Ergebnis kommt – und ob das mit meiner klinischen Einschätzung übereinstimmt."

---

## 6. Neuen Patienten anlegen (ca. 2 min)

**Navigation:** „Patienten" → „Patient anlegen" (oder `/patients/create`)

> „Ich zeige jetzt, wie ein neuer Patient erfasst wird."

**Auf das Formular hinweisen:**

> „Oben sehen Sie den Hinweis: Für eine Vorhersage sind mindestens **Geschlecht**
> und **Alter** erforderlich. Weitere klinische Felder verbessern die Qualität
> der Vorhersage."

**Demo-Eingabe (schrittweise eintippen):**

- Anzeigename: `Testpatient, Max`
- Alter: `63`
- Geschlecht: `männlich`
- Operierte Seite: `links`
- Hördauer: `8`

> „Das Formular ist zweisprachig – alle Feldbezeichnungen und Hinweise sind auf
> Deutsch verfügbar."

**Formular absenden:**

> „Nach dem Speichern wird sofort eine erste Vorhersage berechnet."

---

## 7. Sprachumschalter (ca. 30 s)

**Sprachschalter oben rechts → EN**

> „Für internationale Kollegen oder englischsprachige Protokolle kann die
> gesamte Oberfläche mit einem Klick auf Englisch umgestellt werden."

**Zurück auf DE schalten.**

---

## 8. Abschluss (ca. 30 s)

> „HEAR-UI ist kein Black-Box-Tool. Jede Vorhersage ist nachvollziehbar,
> jede Modellversion dokumentiert. Wir sind gespannt auf Ihr Feedback –
> insbesondere: Welche Features fehlen noch? Welche Darstellungen sind
> für den klinischen Alltag am hilfreichsten?"

> „Vielen Dank."

---

## Technische Hinweise für die Aufnahme

- Auflösung: mind. 1080p, Fenster maximiert
- Browser-Zoom: 100 % (oder 110 % für bessere Lesbarkeit auf Video)
- Demo-Daten sind in der lokalen Datenbank – kein Echtpatientendaten-Risiko
- Falls die KI-Erklärung zu lange lädt: Vorab-Screenshot bereitstellen
