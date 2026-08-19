import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_incident_history_view_returns_success(client):

    response = client.get(
        "/incidents/history/view"
    )

    assert response.status_code == 200


def test_incident_history_view_contains_incident_history(client):

    response = client.get(
        "/incidents/history/view"
    )

    assert b"Incident History" in response.data
    assert b"All Incidents" in response.data


def test_incident_history_view_contains_incident_columns(client):

    response = client.get(
        "/incidents/history/view"
    )

    assert b"Severity" in response.data
    assert b"Area" in response.data
    assert b"Status" in response.data
    assert b"Root Cause" in response.data
    assert b"Detected At" in response.data
    assert b"Resolved At" in response.data
    assert b"Details" in response.data


def test_incident_history_view_contains_view_details_link(client):

    response = client.get(
        "/incidents/history/view"
    )

    assert b"View Details" in response.data