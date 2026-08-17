import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_incident_summary_by_area():

    response = requests.get(
        f"{BASE_URL}/incidents/summary/areas"
    )

    assert response.status_code == 200

    data = response.json()

    assert "areas" in data
    assert isinstance(data["areas"], list)

    for area in data["areas"]:

        assert "area" in area
        assert "total" in area
        assert "open" in area
        assert "resolved" in area

        total = int(area["total"])
        open_incidents = int(area["open"])
        resolved_incidents = int(area["resolved"])

        assert total == (
            open_incidents + resolved_incidents
        )

        assert isinstance(area["area"], str)