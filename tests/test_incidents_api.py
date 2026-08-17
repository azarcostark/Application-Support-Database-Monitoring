import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_open_incidents():
    response = requests.get(
        f"{BASE_URL}/incidents"
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "source" in data
    assert "incidents" in data

    assert data["source"] in {
        "MYSQL",
        "LOCAL_FALLBACK"
    }

    assert data["count"] == len(
        data["incidents"]
    )

    for incident in data["incidents"]:
        assert incident["status"] == "OPEN"


def test_get_open_incidents_explicitly():
    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"status": "OPEN"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "incidents" in data

    for incident in data["incidents"]:
        assert incident["status"] == "OPEN"


def test_get_resolved_incidents():
    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"status": "RESOLVED"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "incidents" in data

    for incident in data["incidents"]:
        assert incident["status"] == "RESOLVED"


def test_invalid_incident_status():
    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"status": "FAILED"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"