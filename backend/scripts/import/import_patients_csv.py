#!/usr/bin/env python3
"""Import patients from a CSV file into the database as Patient records.

This reuses the column mapping and parsing helpers from
`app.api.routes.predict_batch` for best-effort normalization.

Usage: python import_patients_csv.py /path/to/patients.csv
"""
from __future__ import annotations

import sys
from pathlib import Path
import csv

from sqlmodel import Session

from app.core.db import engine
from app import crud
from app.models import PatientCreate
from app.api.routes.predict_batch import (
    COLUMN_MAPPING,
    _normalize_header,
    _to_bool,
    _parse_interval_to_years,
)


def load_csv(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Build input_features from row, normalized
            input_features = {}
            for k, v in row.items():
                if v is None or str(v).strip() == "":
                    continue
                nk = _normalize_header(k)
                mapped = COLUMN_MAPPING.get(nk, k)
                # try numeric
                try:
                    fv = float(v)
                    input_features[mapped] = fv
                    continue
                except Exception:
                    pass

                # interval -> years
                if mapped in ("onset_interval", "duration_interval"):
                    parsed = _parse_interval_to_years(v)
                    if parsed is not None:
                        input_features[mapped] = parsed
                        continue

                # boolean-like
                b = _to_bool(v)
                if b is not None:
                    input_features[mapped] = b
                    continue

                input_features[mapped] = v
            # Skip empty rows (no features extracted)
            if not input_features:
                continue

            yield PatientCreate(input_features=input_features)


def main(argv: list[str]):
    if len(argv) < 2:
        print("Usage: import_patients_csv.py /path/to/file.csv")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print("File not found:", path)
        return 2

    with Session(engine) as session:
        count = 0
        for p in load_csv(path):
            try:
                crud.create_patient(session=session, patient_in=p)
                count += 1
            except Exception as exc:
                print("Failed to insert row:", exc)

    print(f"Imported {count} patients")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
