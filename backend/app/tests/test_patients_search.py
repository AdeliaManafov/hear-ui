"""Tests for the patient search endpoint."""

from unittest.mock import patch, MagicMock
from uuid import uuid4
from datetime import datetime

import pytest
from app.models import Patient


def make_patient_with_name(name: str):
    return Patient(id=uuid4(), input_features={"Name": name}, created_at=datetime.utcnow())


def test_search_patients_matches_name():
    """Search should return patient whose `Name` contains query (case-insensitive)."""
    from app.api.routes.patients import search_patients_api
    from sqlmodel import Session

    mock_session = MagicMock(spec=Session)

    p1 = make_patient_with_name("Max Mustermann")
    p2 = make_patient_with_name("Anna Beispiel")

    with patch('app.api.routes.patients.crud') as mock_crud:
        mock_crud.list_patients.return_value = [p1, p2]

        res = search_patients_api(q="must", session=mock_session, limit=100)

        assert isinstance(res, list)
        assert {r['id'] for r in res} == {str(p1.id)}
        assert res[0]['name'] == "Max Mustermann"


def test_search_patients_fallback_uses_any_string_value():
    """If no Name key, fallback to first string value inside input_features."""
    from app.api.routes.patients import search_patients_api
    from sqlmodel import Session

    mock_session = MagicMock(spec=Session)

    p = Patient(id=uuid4(), input_features={"foo": 123, "bar": "Beispiel"}, created_at=datetime.utcnow())

    with patch('app.api.routes.patients.crud') as mock_crud:
        mock_crud.list_patients.return_value = [p]

        res = search_patients_api(q="bei", session=mock_session, limit=100)

        assert len(res) == 1
        assert res[0]['name'] == "Beispiel"
