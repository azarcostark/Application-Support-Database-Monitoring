import requests

from config.database import get_database_connection


BASE_URL = "http://127.0.0.1:5000"


def test_incident_lifecycle():

    payload = {
        "severity": "WARNING",
        "area": "APPLICATION",
        "root_cause": "Application response time increased",
        "recommended_action": "Review application logs and API response times"
    }

    create_response = requests.post(
        f"{BASE_URL}/incidents",
        json=payload
    )

    assert create_response.status_code == 201

    created_incident = create_response.json()

    incident = created_incident["incident"]

    incident_id = incident["incident_id"]

    assert created_incident["status"] == "OPEN"

    details_response = requests.get(
        f"{BASE_URL}/incidents/{incident_id}"
    )

    assert details_response.status_code == 200

    incident = details_response.json()["incident"]

    assert incident["incident_id"] == incident_id
    assert incident["severity"] == "WARNING"
    assert incident["area"] == "APPLICATION"
    assert incident["status"] == "OPEN"

    resolve_response = requests.patch(
        f"{BASE_URL}/incidents/{incident_id}/resolve"
    )

    assert resolve_response.status_code == 200

    resolved_data = resolve_response.json()

    assert resolved_data["status"] == "RESOLVED"
    assert resolved_data["incident_id"] == incident_id

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            status,
            resolved_at
        FROM incidents
        WHERE incident_id = %s
    """, (incident_id,))

    database_incident = cursor.fetchone()

    cursor.close()
    connection.close()

    assert database_incident is not None
    assert database_incident["status"] == "RESOLVED"
    assert database_incident["resolved_at"] is not None