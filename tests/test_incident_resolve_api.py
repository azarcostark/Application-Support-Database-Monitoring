import requests

from config.database import get_database_connection


BASE_URL = "http://127.0.0.1:5000"


def create_test_incident():
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO incidents (
            severity,
            area,
            root_cause,
            recommended_action,
            status
        )
        VALUES (
            'WARNING',
            'TEST',
            'API resolution test incident',
            'Resolve test incident',
            'OPEN'
        )
    """)

    connection.commit()

    incident_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return incident_id


def test_resolve_incident():

    incident_id = create_test_incident()

    response = requests.patch(
        f"{BASE_URL}/incidents/{incident_id}/resolve"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "RESOLVED"
    assert data["incident_id"] == incident_id

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            status,
            resolved_at
        FROM incidents
        WHERE incident_id = %s
    """, (incident_id,))

    incident = cursor.fetchone()

    cursor.close()
    connection.close()

    assert incident["status"] == "RESOLVED"
    assert incident["resolved_at"] is not None

def test_resolve_already_resolved_incident():

    incident_id = create_test_incident()

    first_response = requests.patch(
        f"{BASE_URL}/incidents/{incident_id}/resolve"
    )

    assert first_response.status_code == 200

    second_response = requests.patch(
        f"{BASE_URL}/incidents/{incident_id}/resolve"
    )

    assert second_response.status_code == 404

    data = second_response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "Open incident not found"