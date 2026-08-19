import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def test_incident(client):
    response = client.post(
        "/incidents",
        json={
            "severity": "CRITICAL",
            "area": "DATABASE",
            "root_cause": "Test database incident",
            "recommended_action": "Verify database connectivity"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    return data["incident_id"]


def test_incident_details_view_returns_success(
    client,
    test_incident
):
    response = client.get(
        f"/incidents/{test_incident}/view"
    )

    assert response.status_code == 200


def test_incident_details_view_contains_incident_id(
    client,
    test_incident
):
    response = client.get(
        f"/incidents/{test_incident}/view"
    )

    assert str(test_incident).encode() in response.data


def test_incident_details_view_contains_incident_information(
    client,
    test_incident
):
    response = client.get(
        f"/incidents/{test_incident}/view"
    )

    assert b"CRITICAL" in response.data
    assert b"DATABASE" in response.data
    assert b"Test database incident" in response.data


def test_incident_details_view_missing_incident(client):

    response = client.get(
        "/incidents/999999/view"
    )

    assert response.status_code == 404