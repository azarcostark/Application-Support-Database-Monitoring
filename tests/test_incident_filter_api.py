import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_critical_incidents():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"severity": "CRITICAL"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "MYSQL"
    assert isinstance(data["incidents"], list)
    assert data["count"] == len(data["incidents"])

    for incident in data["incidents"]:
        assert incident["severity"] == "CRITICAL"


def test_get_open_critical_incidents():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={
            "status": "OPEN",
            "severity": "CRITICAL"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == len(data["incidents"])

    for incident in data["incidents"]:
        assert incident["status"] == "OPEN"
        assert incident["severity"] == "CRITICAL"


def test_get_resolved_warning_incidents():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={
            "status": "RESOLVED",
            "severity": "WARNING"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == len(data["incidents"])

    for incident in data["incidents"]:
        assert incident["status"] == "RESOLVED"
        assert incident["severity"] == "WARNING"


def test_invalid_incident_severity():

    response = requests.get(
        f"{BASE_URL}/incidents",
        params={"severity": "INFO"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == (
        "Invalid incident severity. "
        "Use WARNING or CRITICAL."
    )