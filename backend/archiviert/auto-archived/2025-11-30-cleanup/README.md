# Archivierte Dateien — 2025-11-30

Diese Dateien wurden archiviert, weil sie für das MVP nicht benötigt werden oder durch aktuellere Versionen ersetzt wurden.

## Inhalt

| Datei | Grund der Archivierung |
|-------|------------------------|
| `api_predict_old.py` | Alte/duplizierte Predict-Route (jetzt in `app/api/routes/predict.py`) |
| `core_predict_dummy.py` | Dummy-Predict-Funktion (ersetzt durch echte ML-Pipeline) |
| `items.py` | Items-Feature nicht im MVP-Scope |
| `login.py` | Auth-Endpoints für MVP deaktiviert (kein Login im Demo) |
| `users.py` | User-Management für MVP deaktiviert |
| `private.py` | Private Endpoints nicht benötigt |
| `item.py` | Item-Model nicht im MVP-Scope |
| `user.py` | User-Model für MVP nicht aktiv genutzt |
| `patient.py` | Ältere Patient-Definition (ersetzt durch `patient_record.py`) |
| `calibrated_regressor.py` | Kalibrierungs-Helfer (nicht aktiv genutzt) |
| `routes/` | Alter Route-Ordner (Duplikat von `api/routes/`) |
| `archive/` | Weitere archivierte Items-Dateien |

## Wiederherstellen

Falls du eine Datei wieder benötigst:

```bash
# Beispiel: user.py wiederherstellen
mv archiviert/auto-archived/2025-11-30-cleanup/user.py app/models/user.py
```

## MVP-Fokus

Das Backend konzentriert sich jetzt auf:
- ✅ **Predict** (`/api/v1/predict/`) — ML-Vorhersage mit Pipeline
- ✅ **SHAP** (`/api/v1/shap/explain`, `/api/v1/patients/{id}/shap`) — Erklärbare KI
- ✅ **Feedback** (`/api/v1/feedback/`) — Nutzerfeedback persistieren
- ✅ **Patients** (`/api/v1/patients/`) — Patientenliste aus DB
- ✅ **Utils** (`/api/v1/utils/health-check/`) — Health-Check
