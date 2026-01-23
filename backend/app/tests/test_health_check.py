# tests/test_health_check.py


def test_health_check(client):
    """
    Testet den Health-Check Endpoint
    """
    # GET Request an Health-Check Endpoint
    response = client.get("/api/v1/utils/health-check")

    # Status-Code prüfen
    assert response.status_code == 200

    # Rückgabe prüfen
    assert response.json() == {"status": "ok"}
