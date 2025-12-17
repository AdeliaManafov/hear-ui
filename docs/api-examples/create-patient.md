# Patient API Dokumentation

## POST /api/v1/patients/ — Neuen Patienten anlegen (JSON)

### Beschreibung
Erstellt einen neuen Patientendatensatz in der Datenbank via JSON-Request (ohne CSV-Upload).

### Endpoint
```
POST http://localhost:8000/api/v1/patients/
```

### Request Body
```json
{
  "input_features": {
    "Alter [J]": 45,
    "Geschlecht": "w",
    "Primäre Sprache": "Deutsch"
  },
  "display_name": "Muster, Anna"
}
```

**Pflichtfelder:**
- `input_features` (dict): Patientendaten mit deutschen Spaltennamen (wie vom Modell erwartet)

**Optionale Felder:**
- `display_name` (string): Anzeigename für Suche/UI

### Response (201 Created)
```json
{
  "id": "834668ff-e993-4d8c-8999-ad8b28ce8da2",
  "input_features": {
    "Alter [J]": 45,
    "Geschlecht": "w",
    "Primäre Sprache": "Deutsch"
  },
  "display_name": "Muster, Anna",
  "created_at": "2025-12-08T12:34:56.789Z"
}
```

### Fehler
- **400 Bad Request**: `input_features` fehlt oder ist leer
- **500 Internal Server Error**: Datenbankfehler

---

## Beispiel-Verwendung

### 1. Minimaler Patient (nur Alter & Geschlecht)
```bash
curl -X POST "http://localhost:8000/api/v1/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "input_features": {
      "Alter [J]": 30,
      "Geschlecht": "m"
    }
  }'
```

### 2. Patient mit vielen Features
```bash
curl -X POST "http://localhost:8000/api/v1/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "input_features": {
      "Alter [J]": 55,
      "Geschlecht": "w",
      "Primäre Sprache": "Deutsch",
      "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
      "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
      "Symptome präoperativ.Tinnitus...": "ja",
      "Behandlung/OP.CI Implantation": "Cochlear Nucleus"
    },
    "display_name": "Schmidt, Maria"
  }'
```

### 3. Patient anlegen und direkt Prediction abrufen
```bash
# Patient erstellen und ID speichern
PATIENT_ID=$(curl -sS -X POST "http://localhost:8000/api/v1/patients/" \
  -H "Content-Type: application/json" \
  -d '{"input_features":{"Alter [J]":45,"Geschlecht":"w"},"display_name":"Test"}' \
  | jq -r '.id')

echo "Patient ID: $PATIENT_ID"

# Prediction für diesen Patienten abrufen
curl -sS "http://localhost:8000/api/v1/patients/$PATIENT_ID/predict" | jq
```

**Output:**
```json
{
  "prediction": 0.7552789278637184,
  "explanation": {}
}
```

---

## Verwandte Endpoints

Nach dem Anlegen eines Patienten können folgende Endpoints verwendet werden:

- **GET /api/v1/patients/{patient_id}** — Patient abrufen
- **GET /api/v1/patients/{patient_id}/predict** — Prediction für Patient
- **GET /api/v1/patients/{patient_id}/explainer** — SHAP-Erklärung für Patient
- **GET /api/v1/patients/{patient_id}/validate** — Prüfe ob alle nötigen Features vorhanden sind

---

## Python-Beispiel (Requests)

```python
import requests

url = "http://localhost:8000/api/v1/patients/"

payload = {
    "input_features": {
        "Alter [J]": 45,
        "Geschlecht": "w",
        "Primäre Sprache": "Deutsch"
    },
    "display_name": "Muster, Anna"
}

response = requests.post(url, json=payload)

if response.status_code == 201:
    patient = response.json()
    print(f"Patient erstellt: {patient['id']}")
    
    # Prediction abrufen
    pred_response = requests.get(
        f"http://localhost:8000/api/v1/patients/{patient['id']}/predict"
    )
    print(f"Prediction: {pred_response.json()['prediction']}")
else:
    print(f"Fehler: {response.status_code} - {response.json()}")
```

---

## Tests

Tests für diesen Endpoint befinden sich in:
```
backend/app/tests/api/routes/test_create_patient.py
```

Ausführen:
```bash
docker compose exec backend pytest app/tests/api/routes/test_create_patient.py -v
```

**Test-Coverage:**
-  Patient mit gültigen Daten erstellen
-  Patient mit minimalen Feldern erstellen
-  Fehler bei leeren input_features
-  Fehler bei fehlenden input_features
-  Patient mit komplexen Features erstellen
-  Erstellter Patient kann abgerufen werden
-  Mehrere Patienten erstellen

Alle 7 Tests bestehen.
