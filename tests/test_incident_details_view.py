def test_incident_details_view_returns_success(client):
    response = client.get("/incidents/399/view")

    assert response.status_code == 200


def test_incident_details_view_contains_incident_id(client):
    response = client.get("/incidents/399/view")

    assert b"399" in response.data


def test_incident_details_view_contains_incident_information(client):
    response = client.get("/incidents/399/view")

    assert b"CRITICAL" in response.data
    assert b"DATABASE" in response.data
    assert b"Automated API test incident" in response.data


def test_incident_details_view_missing_incident(client):
    response = client.get("/incidents/999999/view")

    assert response.status_code == 404