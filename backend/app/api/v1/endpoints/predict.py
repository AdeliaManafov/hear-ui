from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any
import pandas as pd

router = APIRouter()

@router.post("/upload")
async def upload_prediction_data(file: UploadFile = File(...)) -> Any:
    """
    Upload-Endpunkt für Vorhersagedaten mit patients-Spalte.
    """
    try:
        df = pd.read_csv(file.file)
        
        # Überprüfe ob 'patients' Spalte existiert
        if "patients" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Die Spalte 'patients' fehlt in der hochgeladenen Datei"
            )
        
        # Verarbeite Patientendaten
        patients_data = df["patients"].tolist()
        
        # Weitere Verarbeitung...
        return {"status": "success", "patients_count": len(patients_data)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
