# HEAR CI Prediction Model – Model Card

## Zweck
Dieses Dokument beschreibt den Aufbau und die Pflege der Model Card für das HEAR CI Prediction Model.  
Die Model Card wird automatisch im Frontend angezeigt und bietet eine Übersicht über das Modell, seine Features, Metriken und Nutzungshinweise.

---

## Datenquellen

1. **Hardcoded Werte**
    - Name, Version, intended_use, not_intended_for, limitations, recommendations
    - Diese Werte liegen in der JSON-Datei `model_card_config.json`.
    - Vorteil: Bei einem Modellwechsel muss nur diese Datei aktualisiert werden, nicht der Python-Code.

2. **Features**
    - Aus `app/core/preprocessor.py` (Liste `EXPECTED_FEATURES`)
    - Diese werden automatisch geladen und in die Model Card eingetragen.

3. **Modelltyp & Pfad**
    - Aus dem FastAPI Wrapper (`fastapi_app.state.model_wrapper`) oder, falls nicht vorhanden, Standardpfad `backend/app/models/logreg_best_model.pkl`.

4. **Model Metrics**
    - Teilweise hartkodiert in der JSON-Datei.
    - Nur vorhandene Werte werden im Frontend angezeigt. Felder mit `null` oder nicht vorhandene Werte werden nicht dargestellt.

5. **Optional: SHAP Top Features**
    - Wenn ein Wrapper geladen ist und Background/Sample vorhanden ist, werden Top SHAP Features berechnet.
    - Diese werden für die Feature-Interpretation genutzt.

---

## Anpassen bei Modellwechsel

1. **JSON-Datei aktualisieren**
    - Passe `model_card_config.json` an: Name, Version, Metrics, Empfehlungen, Einschränkungen, etc.
    - Erstelle eine neue datei und wechsel den namen in model_card.py:
         config_path = Path(__file__).parent / "model_card_config.json"