import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_incident_by_id():
    response = requests.get(
        f"{BASE_URL}/incidents/15"
    )

    assert response.status_code == 200

    data = response.json()

    assert "incident" in data

    incident = data["incident"]

    assert incident["incident_id"] == 15
    assert "severity" in incident
    assert "area" in incident
    assert "status" in incident
    assert "root_cause" in incident


def test_get_missing_incident():
    response = requests.get(
        f"{BASE_URL}/incidents/9999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "Incident not found"