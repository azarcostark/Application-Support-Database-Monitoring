import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_incident_history():

    response = requests.get(
        f"{BASE_URL}/incidents/history"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "MYSQL"
    assert isinstance(data["count"], int)
    assert isinstance(data["incidents"], list)

    assert data["count"] == len(data["incidents"])

    if data["incidents"]:
        incident = data["incidents"][0]

        assert "incident_id" in incident
        assert "severity" in incident
        assert "area" in incident
        assert "root_cause" in incident
        assert "recommended_action" in incident
        assert "status" in incident
        assert "detected_at" in incident
        assert "resolved_at" in incident