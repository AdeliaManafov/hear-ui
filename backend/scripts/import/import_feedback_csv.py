#!/usr/bin/env python3
"""Import historical feedback CSV into the database.

This script is intentionally lightweight and uses the application's DB engine
to insert rows using the existing CRUD helpers. It expects a CSV with a
header row. Columns named `prediction`, `explanation`, `accepted`,
`comment`, `user_email` are mapped directly. All other columns are collected
into `input_features` as a JSON-like dict.

Usage: python import_feedback_csv.py /path/to/file.csv
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app import crud
from app.models import FeedbackCreate


KNOWN = {"prediction", "explanation", "accepted", "comment"}


def load_csv(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Build input_features from unknown columns
            input_features = {k: v for k, v in row.items() if k not in KNOWN}

            # Parse types
            pred = None
            if row.get("prediction"):
                try:
                    pred = float(row.get("prediction"))
                except Exception:
                    pred = None

            explanation = None
            if row.get("explanation"):
                try:
                    explanation = json.loads(row.get("explanation"))
                except Exception:
                    explanation = {"raw": row.get("explanation")}

            accepted = None
            if row.get("accepted"):
                v = row.get("accepted").strip().lower()
                accepted = v in ("1", "true", "yes", "y", "t")

            fb = FeedbackCreate(
                input_features=input_features,
                prediction=pred,
                explanation=explanation,
                accepted=accepted,
                comment=row.get("comment") or None,
            )

            yield fb


def main(argv: list[str]):
    if len(argv) < 2:
        print("Usage: import_feedback_csv.py /path/to/file.csv")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print("File not found:", path)
        return 2

    with Session(engine) as session:
        for fb in load_csv(path):
            try:
                crud.create_feedback(session=session, feedback_in=fb)
            except Exception as exc:
                print("Failed to insert row:", exc)

    print("Import complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
