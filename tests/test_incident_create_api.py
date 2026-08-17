import requests

from config.database import get_database_connection


BASE_URL = "http://127.0.0.1:5000"


def test_create_incident():

    payload = {
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Automated API test incident",
        "recommended_action": "Verify database connectivity"
    }

    response = requests.post(
        f"{BASE_URL}/incidents",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "OPEN"
    assert data["message"] == "Incident created successfully"
    assert "incident" in data

    incident = data["incident"]

    assert isinstance(incident["incident_id"], int)

    incident_id = incident["incident_id"]

    assert incident["severity"] == "CRITICAL"
    assert incident["area"] == "DATABASE"
    assert incident["root_cause"] == "Automated API test incident"
    assert incident["recommended_action"] == "Verify database connectivity"
    assert incident["status"] == "OPEN"
    assert incident["resolved_at"] is None

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            incident_id,
            severity,
            area,
            root_cause,
            recommended_action,
            status,
            resolved_at
        FROM incidents
        WHERE incident_id = %s
    """, (incident_id,))

    database_incident = cursor.fetchone()

    cursor.close()
    connection.close()

    assert database_incident is not None
    assert database_incident["incident_id"] == incident_id
    assert database_incident["severity"] == "CRITICAL"
    assert database_incident["area"] == "DATABASE"
    assert database_incident["root_cause"] == (
        "Automated API test incident"
    )
    assert database_incident["recommended_action"] == (
        "Verify database connectivity"
    )
    assert database_incident["status"] == "OPEN"
    assert database_incident["resolved_at"] is None


def test_create_incident_missing_fields():

    payload = {
        "severity": "CRITICAL",
        "area": "DATABASE"
    }

    response = requests.post(
        f"{BASE_URL}/incidents",
        json=payload
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "Missing required fields"
    assert "root_cause" in data["fields"]
    assert "recommended_action" in data["fields"]


def test_create_incident_invalid_severity():

    payload = {
        "severity": "INFO",
        "area": "DATABASE",
        "root_cause": "Invalid severity test",
        "recommended_action": "No action required"
    }

    response = requests.post(
        f"{BASE_URL}/incidents",
        json=payload
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == (
        "Severity must be WARNING or CRITICAL"
    )


def test_create_incident_without_request_body():

    response = requests.post(
        f"{BASE_URL}/incidents"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "Request body is required"