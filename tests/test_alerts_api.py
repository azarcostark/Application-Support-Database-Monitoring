import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_all_alerts():

    response = requests.get(
        f"{BASE_URL}/alerts"
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "alerts" in data

    assert data["count"] == len(
        data["alerts"]
    )


def test_get_critical_alerts():

    response = requests.get(
        f"{BASE_URL}/alerts",
        params={"severity": "CRITICAL"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "alerts" in data

    assert data["count"] == len(
        data["alerts"]
    )

    for alert in data["alerts"]:
        assert alert["severity"] == "CRITICAL"


def test_get_warning_alerts():

    response = requests.get(
        f"{BASE_URL}/alerts",
        params={"severity": "WARNING"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "alerts" in data

    assert data["count"] == len(
        data["alerts"]
    )

    for alert in data["alerts"]:
        assert alert["severity"] == "WARNING"


def test_get_alert_by_id():

    all_alerts_response = requests.get(
        f"{BASE_URL}/alerts"
    )

    assert all_alerts_response.status_code == 200

    alerts = all_alerts_response.json()["alerts"]

    if not alerts:
        return

    alert_id = alerts[0]["alert_id"]

    response = requests.get(
        f"{BASE_URL}/alerts/{alert_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert "alert" in data
    assert data["alert"]["alert_id"] == alert_id


def test_get_missing_alert():

    response = requests.get(
        f"{BASE_URL}/alerts/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_alert_severity():

    response = requests.get(
        f"{BASE_URL}/alerts",
        params={"severity": "INVALID"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"