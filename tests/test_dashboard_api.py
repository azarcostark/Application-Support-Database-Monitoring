import requests


BASE_URL = "http://127.0.0.1:5000"


def test_dashboard_returns_success():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200


def test_dashboard_contains_system_status():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert "system_status" in data
    assert data["system_status"] in {
        "HEALTHY",
        "DEGRADED",
        "CRITICAL"
    }


def test_dashboard_contains_api_information():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert "api" in data
    assert "status" in data["api"]
    assert "slow_endpoints" in data["api"]
    assert "failed_endpoints" in data["api"]


def test_dashboard_contains_database_information():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert "database" in data
    assert "status" in data["database"]


def test_dashboard_contains_incident_information():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert "incidents" in data

    assert "total" in data["incidents"]
    assert "open" in data["incidents"]
    assert "resolved" in data["incidents"]
    assert "critical" in data["incidents"]
    assert "warning" in data["incidents"]


def test_dashboard_incident_counts_are_consistent():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    incidents = data["incidents"]

    assert incidents["total"] == (
        incidents["open"] +
        incidents["resolved"]
    )

    assert incidents["total"] == (
        incidents["critical"] +
        incidents["warning"]
    )

def test_dashboard_contains_recent_incidents():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert "recent_incidents" in data
    assert isinstance(
        data["recent_incidents"],
        list
    )

    assert len(data["recent_incidents"]) <= 5

    for incident in data["recent_incidents"]:
        assert "incident_id" in incident
        assert "severity" in incident
        assert "area" in incident
        assert "root_cause" in incident
        assert "status" in incident

        assert incident["status"] == "OPEN"