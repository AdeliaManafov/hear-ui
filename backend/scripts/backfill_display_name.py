"""Backfill script to populate Patient.display_name from input_features.

Run this script with the project environment active, it will iterate all
patients and set `display_name` based on common name fields or a sensible
fallback.

Usage:
    python backend/scripts/backfill_display_name.py
"""
from sqlmodel import Session, select
from app.core.db import engine
from app.models import Patient

NAME_KEYS = ["vorname", "nachname", "name", "full_name", "fullname", "first_name", "last_name"]


def _iter_strings(obj):
    """Recursively yield string values from nested structures."""
    if obj is None:
        return
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _iter_strings(v)


def _find_by_keys(d: dict, keys: list[str]) -> str | None:
    if not isinstance(d, dict):
        return None
    lowered = {k.lower(): v for k, v in d.items()}
    for k in keys:
        v = lowered.get(k)
        if v:
            return v
    return None


def compute_display_name(input_features: dict) -> str | None:
    """Compute a sensible `display_name` from `input_features`.

    Algorithm:
    - Prefer explicit `vorname` + `nachname` (or first/last) concatenation.
    - Else prefer explicit full-name keys like `name` / `full_name`.
    - Else search recursively for the first candidate string that looks like a
      name (not a single-letter gender marker like 'w'/'m').
    - Return None when no reasonable candidate is found.
    """
    if not input_features:
        return None

    # prefer combined Vorname + Nachname (case-insensitive keys)
    first = _find_by_keys(input_features, ['vorname', 'first', 'first_name', 'firstname'])
    last = _find_by_keys(input_features, ['nachname', 'last', 'last_name', 'lastname'])
    try:
        if isinstance(first, str):
            first = first.strip()
        if isinstance(last, str):
            last = last.strip()
    except Exception:
        pass

    if first or last:
        parts = [p for p in [first, last] if p]
        combined = ' '.join(parts).strip()
        if combined:
            return combined

    # prefer explicit full-name keys
    full = _find_by_keys(input_features, ['name', 'full_name', 'fullname'])
    if isinstance(full, str) and full.strip():
        return full.strip()

    # fallback: look for any reasonable string-ish candidate (not single-char gender markers)
    for s in _iter_strings(input_features):
        if not isinstance(s, str):
            continue
        t = s.strip()
        if not t:
            continue
        # ignore single-letter gender flags and common non-name tokens
        if len(t) <= 2 and t.lower() in {'w', 'm', 'd', 'f', 'ja', 'nein'}:
            continue
        # prefer strings that look like a name: contain a space/comma or are longer than 2 chars
        # (avoid single-letter codes like 'L'/'R')
        if ' ' in t or ',' in t or len(t) > 2:
            return t

    return None


def main():
    with Session(engine) as session:
        stmt = select(Patient)
        results = session.exec(stmt).all()
        updated = 0
        # consider these values invalid and overwrite them when found
        invalid_values = {None, "", "w", "m", "W", "M"}
        for p in results:
            name = compute_display_name(p.input_features or {})
            current = p.display_name if p.display_name is not None else ""
            # update when we found a better name OR the current value is clearly invalid
            should_update = False
            if name and name != current:
                should_update = True
            if (not name) and (current in invalid_values):
                # nothing to set, but if current is invalid we prefer NULL
                if current != "":
                    p.display_name = None
                    session.add(p)
                    updated += 1
                continue

            if current in invalid_values and name:
                should_update = True

            if should_update:
                p.display_name = name
                session.add(p)
                updated += 1

        if updated:
            session.commit()
        print(f"Backfill complete, updated {updated} patients")


if __name__ == '__main__':
    main()
