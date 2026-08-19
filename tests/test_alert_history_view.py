import pytest

from app import create_app


@pytest.fixture
def client():

    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_alert_history_view_returns_success(client):

    response = client.get(
        "/alerts/history/view"
    )

    assert response.status_code == 200


def test_alert_history_view_contains_alert_history(client):

    response = client.get(
        "/alerts/history/view"
    )

    assert b"Alert History" in response.data


def test_alert_history_view_contains_alert_columns(client):

    response = client.get(
        "/alerts/history/view"
    )

    assert b"Alert ID" in response.data
    assert b"Incident ID" in response.data
    assert b"Severity" in response.data
    assert b"Area" in response.data
    assert b"Root Cause" in response.data
    assert b"Recommended Action" in response.data
    assert b"Failed API Endpoints" in response.data
    assert b"Slow API Endpoints" in response.data
    assert b"Created At" in response.data