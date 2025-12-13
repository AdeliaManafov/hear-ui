# Patient Update & Delete API Endpoints

Diese Dokumentation beschreibt die neuen Endpoints zum Aktualisieren und Löschen von Patienten.

## Übersicht

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/v1/patients/{id}` | PUT | Patient-Daten aktualisieren |
| `/api/v1/patients/{id}` | DELETE | Patient löschen |

---

## PUT /api/v1/patients/{id} - Patient aktualisieren

Aktualisiert die Daten eines bestehenden Patienten. Nur die übergebenen Felder werden aktualisiert (partial update).

### Request

**URL:** `/api/v1/patients/{patient_id}`  
**Methode:** `PUT`  
**Content-Type:** `application/json`

#### Body Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `input_features` | `object` | Nein | Neue Input-Features (ersetzt alte Features) |
| `display_name` | `string` | Nein | Neuer Anzeigename |

**Hinweis:** Mindestens ein Feld muss angegeben werden.

### Response

**Status Code:** `200 OK`

```json
{
  "id": "8d0f0bdf-70ff-4553-a46d-4be58023d319",
  "input_features": {
    "Alter [J]": 50,
    "Geschlecht": "m",
    "Primäre Sprache": "Deutsch"
  },
  "display_name": "Mustermann, Max",
  "created_at": "2025-12-13T10:30:00.000000"
}
```

### Fehler-Responses

| Status Code | Beschreibung |
|-------------|--------------|
| `400 Bad Request` | Keine Felder zum Update angegeben |
| `404 Not Found` | Patient mit der ID existiert nicht |
| `500 Internal Server Error` | Server-Fehler beim Update |

### Beispiele

#### Beispiel 1: Input-Features aktualisieren

```bash
curl -X PUT http://localhost:8000/api/v1/patients/8d0f0bdf-70ff-4553-a46d-4be58023d319 \
  -H "Content-Type: application/json" \
  -d '{
    "input_features": {
      "Alter [J]": 50,
      "Geschlecht": "m",
      "Primäre Sprache": "Deutsch"
    }
  }'
```

#### Beispiel 2: Nur Display-Name aktualisieren

```bash
curl -X PUT http://localhost:8000/api/v1/patients/8d0f0bdf-70ff-4553-a46d-4be58023d319 \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "Mustermann, Max"
  }'
```

#### Beispiel 3: Beide Felder aktualisieren

```bash
curl -X PUT http://localhost:8000/api/v1/patients/8d0f0bdf-70ff-4553-a46d-4be58023d319 \
  -H "Content-Type: application/json" \
  -d '{
    "input_features": {
      "Alter [J]": 55,
      "Geschlecht": "w"
    },
    "display_name": "Musterfrau, Maria"
  }'
```

#### Python-Beispiel

```python
import requests

patient_id = "8d0f0bdf-70ff-4553-a46d-4be58023d319"
url = f"http://localhost:8000/api/v1/patients/{patient_id}"

payload = {
    "input_features": {
        "Alter [J]": 50,
        "Geschlecht": "m"
    },
    "display_name": "Mustermann, Max"
}

response = requests.put(url, json=payload)
if response.status_code == 200:
    updated_patient = response.json()
    print(f"Patient updated: {updated_patient['display_name']}")
else:
    print(f"Error: {response.status_code} - {response.json()}")
```

---

## DELETE /api/v1/patients/{id} - Patient löschen

Löscht einen Patienten permanent aus der Datenbank (hard delete).

### Request

**URL:** `/api/v1/patients/{patient_id}`  
**Methode:** `DELETE`

### Response

**Status Code:** `204 No Content`

Bei erfolgreicher Löschung wird kein Body zurückgegeben.

### Fehler-Responses

| Status Code | Beschreibung |
|-------------|--------------|
| `404 Not Found` | Patient mit der ID existiert nicht |
| `500 Internal Server Error` | Server-Fehler beim Löschen |

### Beispiele

#### Beispiel 1: Patient löschen

```bash
curl -X DELETE http://localhost:8000/api/v1/patients/8d0f0bdf-70ff-4553-a46d-4be58023d319
```

**Response:**
```
HTTP/1.1 204 No Content
```

#### Beispiel 2: Patient löschen und prüfen

```bash
# Patient löschen
curl -X DELETE http://localhost:8000/api/v1/patients/8d0f0bdf-70ff-4553-a46d-4be58023d319

# Prüfen ob Patient gelöscht wurde (sollte 404 zurückgeben)
curl -X GET http://localhost:8000/api/v1/patients/8d0f0bdf-70ff-4553-a46d-4be58023d319
```

**Response:**
```json
{
  "detail": "Patient not found"
}
```

#### Python-Beispiel

```python
import requests

patient_id = "8d0f0bdf-70ff-4553-a46d-4be58023d319"
url = f"http://localhost:8000/api/v1/patients/{patient_id}"

response = requests.delete(url)
if response.status_code == 204:
    print(f"Patient {patient_id} successfully deleted")
elif response.status_code == 404:
    print(f"Patient {patient_id} not found")
else:
    print(f"Error: {response.status_code}")
```

---

## Wichtige Hinweise

### Hard Delete vs. Soft Delete

Die aktuelle Implementierung nutzt **Hard Delete** — der Patient wird permanent aus der Datenbank entfernt.

**Vor- und Nachteile:**

✅ **Vorteile:**
- Einfache Implementierung
- DSGVO-konform (Recht auf Vergessen)
- Keine "gelöschten" Datensätze in der DB

❌ **Nachteile:**
- Keine Wiederherstellung möglich
- Verlust von Audit-Trail
- Verknüpfte Predictions/Feedback müssen ggf. auch gelöscht werden

**Alternative: Soft Delete**

Falls später ein Soft Delete benötigt wird (Patient als "gelöscht" markieren aber Daten behalten):
1. `is_active` Boolean-Flag zum Patient-Model hinzufügen
2. DELETE-Endpoint setzt `is_active=False` statt Datensatz zu löschen
3. LIST/GET-Endpoints filtern nach `is_active=True`

### Datenintegrität

Bei Löschung eines Patienten sollte geprüft werden:
- Gibt es verknüpfte Predictions?
- Gibt es verknüpftes Feedback?

**Empfehlung:** In Zukunft Foreign Keys mit CASCADE-Delete einrichten oder vor Löschung prüfen.

### Berechtigungen

Aktuell sind beide Endpoints **ohne Authentifizierung** zugänglich.

**Für Produktion:**
- Authentifizierung hinzufügen (JWT, OAuth)
- Autorisierung prüfen (nur Admin/Besitzer darf löschen)
- Audit-Logging für Löschungen implementieren

---

## Frontend-Integration

### Vue/TypeScript Beispiel

```typescript
import { PatientsService, type PatientUpdate } from '@/client';

// Patient aktualisieren
async function updatePatient(patientId: string, updates: PatientUpdate) {
  try {
    const updatedPatient = await PatientsService.updatePatientApi(
      patientId,
      updates
    );
    console.log('Patient updated:', updatedPatient);
    return updatedPatient;
  } catch (error) {
    console.error('Failed to update patient:', error);
    throw error;
  }
}

// Patient löschen
async function deletePatient(patientId: string) {
  try {
    await PatientsService.deletePatientApi(patientId);
    console.log('Patient deleted successfully');
    return true;
  } catch (error) {
    console.error('Failed to delete patient:', error);
    return false;
  }
}

// Verwendung
const patientId = '8d0f0bdf-70ff-4553-a46d-4be58023d319';

// Update
await updatePatient(patientId, {
  input_features: { 'Alter [J]': 50, Geschlecht: 'm' },
  display_name: 'Mustermann, Max'
});

// Delete
await deletePatient(patientId);
```

---

## Tests

Umfassende Tests sind verfügbar in:
- `backend/app/tests/api/routes/test_patients.py`

### Test-Klassen

- `TestUpdatePatient` (6 Tests)
  - Update von input_features
  - Update von display_name
  - Update beider Felder
  - Fehlerfall: Patient nicht gefunden
  - Fehlerfall: Leerer Body
  - Prüfung: Andere Felder bleiben erhalten

- `TestDeletePatient` (3 Tests)
  - Erfolgreiche Löschung
  - Fehlerfall: Patient nicht gefunden
  - Idempotenz-Prüfung (zweimaliges Löschen)

### Tests ausführen

```bash
# Alle Patient-Tests
docker compose exec backend python -m pytest app/tests/api/routes/test_patients.py -v

# Nur UPDATE/DELETE Tests
docker compose exec backend python -m pytest \
  app/tests/api/routes/test_patients.py::TestUpdatePatient \
  app/tests/api/routes/test_patients.py::TestDeletePatient \
  -v
```

---

## API-Dokumentation

Die Endpoints sind automatisch in der Swagger-Dokumentation verfügbar:

**URL:** http://localhost:8000/docs

Dort können die Endpoints interaktiv getestet werden.

---

## Nächste Schritte

Mögliche Erweiterungen:
1. [ ] Soft Delete implementieren (`is_active` Flag)
2. [ ] Authentifizierung/Autorisierung hinzufügen
3. [ ] Audit-Logging für Updates/Deletes
4. [ ] Cascade-Delete für verknüpfte Entities (Predictions, Feedback)
5. [ ] Bulk-Update/Delete Endpoints
6. [ ] Versionierung von Patient-Daten (History)
7. [ ] Validierung vor Update (z.B. ML-Model-kompatible Features)
