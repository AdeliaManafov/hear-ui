#!/usr/bin/env python3
import argparse
import csv
import random
from pathlib import Path

import requests

CSV = Path(__file__).resolve().parents[1] / "patientsData" / "sample_patients.csv"
DEFAULT_API = "http://localhost:8000/api/v1/patients/"

FEMALE_FIRST_NAMES = [
    "Anna", "Maria", "Lena", "Sofia", "Lea", "Mia", "Emilia", "Hannah",
    "Johanna", "Laura", "Sarah", "Julia"
]
MALE_FIRST_NAMES = [
    "Max", "Paul", "Leon", "Jonas", "Lukas", "Noah", "Ben", "Finn",
    "Elias", "Felix", "Julian", "Tim"
]
LAST_NAMES = [
    "Muster", "Schmidt", "Meyer", "Schneider", "Fischer", "Weber",
    "Wagner", "Becker", "Hoffmann", "Schulz", "Koch", "Bauer"
]


def _pick_name(idx: int, gender: str | None) -> str:
    gender_norm = (gender or "").strip().lower()
    if gender_norm in {"w", "f", "female"}:
        first = FEMALE_FIRST_NAMES[idx % len(FEMALE_FIRST_NAMES)]
    elif gender_norm in {"m", "male"}:
        first = MALE_FIRST_NAMES[idx % len(MALE_FIRST_NAMES)]
    else:
        combined = FEMALE_FIRST_NAMES + MALE_FIRST_NAMES
        first = combined[idx % len(combined)]
    last = LAST_NAMES[idx % len(LAST_NAMES)]
    return f"{last}, {first}"


def _load_column_values(path: Path) -> tuple[list[str], dict[str, list[str]]]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers = reader.fieldnames or []
        values: dict[str, list[str]] = {h: [] for h in headers}
        for row in reader:
            for h in headers:
                v = row.get(h)
                if v is None:
                    continue
                v = str(v).strip()
                if v == "":
                    continue
                values[h].append(v)
    return headers, values


def _sample_value(rng: random.Random, pool: list[str], null_chance: float = 0.15) -> str | None:
    if not pool:
        return None
    if rng.random() < null_chance:
        return None
    return rng.choice(pool)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate plausible patient records and import via API.")
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--api", type=str, default=DEFAULT_API)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-id", type=int, default=1000)
    parser.add_argument("--dry-run", action="store_true", help="Print payloads instead of posting to API.")
    args = parser.parse_args()

    if not CSV.exists():
        print("CSV not found:", CSV)
        return 1

    headers, values = _load_column_values(CSV)
    if not headers:
        print("CSV has no headers.")
        return 1

    rng = random.Random(args.seed)
    created = 0
    for i in range(args.count):
        features: dict[str, str | None] = {}
        for h in headers:
            features[h] = _sample_value(rng, values.get(h, []))

        # enforce some plausibility
        if "ID" in features:
            features["ID"] = str(args.start_id + i)
        if "Geschlecht" in features:
            features["Geschlecht"] = rng.choice(["w", "m"])
        if "Alter [J]" in features and values.get("Alter [J]"):
            age_pool = values["Alter [J]"]
            features["Alter [J]"] = rng.choice(age_pool)

        display_name = _pick_name(i, features.get("Geschlecht"))
        payload = {"input_features": features, "display_name": display_name}

        if args.dry_run:
            print(payload)
            created += 1
        else:
            try:
                r = requests.post(args.api, json=payload, timeout=10)
                if r.status_code in (200, 201):
                    created += 1
                    print("Created:", r.json().get("id"))
                else:
                    print("Failed:", r.status_code, r.text)
            except Exception as e:
                print("Error posting:", e)

    print("Imported total:", created)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
