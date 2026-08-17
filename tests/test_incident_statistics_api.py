import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_incident_statistics():

    response = requests.get(
        f"{BASE_URL}/incidents/statistics"
    )

    assert response.status_code == 200

    data = response.json()

    assert "statistics" in data
    assert isinstance(data["statistics"], list)

    for statistic in data["statistics"]:
        assert "area" in statistic
        assert "severity" in statistic
        assert "total" in statistic
        assert "open" in statistic
        assert "resolved" in statistic

        assert statistic["total"] == (
            statistic["open"] + statistic["resolved"]
        )

        assert statistic["area"] in {
            "APPLICATION",
            "DATABASE",
            "TEST"
        }

        assert statistic["severity"] in {
            "WARNING",
            "CRITICAL"
        }