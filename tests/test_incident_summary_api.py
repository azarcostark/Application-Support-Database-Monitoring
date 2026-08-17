import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_incident_summary():

    response = requests.get(
        f"{BASE_URL}/incidents/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "open" in data
    assert "resolved" in data
    assert "critical" in data
    assert "warning" in data

    total = int(data["total"])
    open_incidents = int(data["open"])
    resolved_incidents = int(data["resolved"])
    critical_incidents = int(data["critical"])
    warning_incidents = int(data["warning"])

    assert total == (
        open_incidents + resolved_incidents
    )

    assert total == (
        critical_incidents + warning_incidents
    )

    assert isinstance(total, int)
    assert isinstance(open_incidents, int)
    assert isinstance(resolved_incidents, int)
    assert isinstance(critical_incidents, int)
    assert isinstance(warning_incidents, int)