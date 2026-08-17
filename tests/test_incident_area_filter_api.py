import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_database_incidents():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"area": "DATABASE"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "MYSQL"
    assert isinstance(data["incidents"], list)
    assert data["count"] == len(data["incidents"])

    for incident in data["incidents"]:
        assert incident["area"] == "DATABASE"


def test_get_open_critical_database_incidents():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={
            "status": "OPEN",
            "severity": "CRITICAL",
            "area": "DATABASE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == len(data["incidents"])

    for incident in data["incidents"]:
        assert incident["status"] == "OPEN"
        assert incident["severity"] == "CRITICAL"
        assert incident["area"] == "DATABASE"


def test_invalid_incident_area():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"area": "PAYMENTS"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == (
        "Invalid incident area. "
        "Use APPLICATION, DATABASE, or TEST."
    )