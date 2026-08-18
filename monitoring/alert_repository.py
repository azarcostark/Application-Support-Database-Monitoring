import json
from datetime import datetime
from pathlib import Path

from config.database import get_database_connection


ALERT_FILE = Path("logs/alerts.json")


def _read_local_alerts():
    if not ALERT_FILE.exists():
        return []

    try:
        with ALERT_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def _write_local_alerts(alerts):
    ALERT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ALERT_FILE.open("w", encoding="utf-8") as file:
        json.dump(alerts, file, indent=2)


def _create_local_alert(alert, incident_id=None):
    alerts = _read_local_alerts()

    alert_id = (
        max(
            (
                item["alert_id"]
                for item in alerts
            ),
            default=0
        ) + 1
    )

    local_alert = {
        "alert_id": alert_id,
        "incident_id": incident_id,
        "severity": alert["severity"],
        "area": alert["area"],
        "root_cause": alert["root_cause"],
        "recommended_action": alert["recommended_action"],
        "failed_api_endpoints": ",".join(
            alert["failed_api_endpoints"]
        ),
        "slow_api_endpoints": ",".join(
            alert["slow_api_endpoints"]
        ),
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),
    }

    alerts.append(local_alert)

    _write_local_alerts(alerts)

    return alert_id


def create_alert(alert, incident_id=None):

    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        failed_api_endpoints = ",".join(
            alert["failed_api_endpoints"]
        )

        slow_api_endpoints = ",".join(
            alert["slow_api_endpoints"]
        )

        query = """
            INSERT INTO alerts (
                incident_id,
                severity,
                area,
                root_cause,
                recommended_action,
                failed_api_endpoints,
                slow_api_endpoints
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            incident_id,
            alert["severity"],
            alert["area"],
            alert["root_cause"],
            alert["recommended_action"],
            failed_api_endpoints,
            slow_api_endpoints,
        )

        cursor.execute(query, values)

        connection.commit()

        return cursor.lastrowid

    except Exception:
        return _create_local_alert(
            alert,
            incident_id
        )

    finally:

        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def get_alert_by_id(alert_id):

    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                alert_id,
                incident_id,
                severity,
                area,
                root_cause,
                recommended_action,
                failed_api_endpoints,
                slow_api_endpoints,
                created_at
            FROM alerts
            WHERE alert_id = %s
        """

        cursor.execute(query, (alert_id,))

        return cursor.fetchone()

    except Exception:

        alerts = _read_local_alerts()

        return next(
            (
                alert
                for alert in alerts
                if alert["alert_id"] == alert_id
            ),
            None
        )

    finally:

        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def get_all_alerts():

    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                alert_id,
                incident_id,
                severity,
                area,
                root_cause,
                recommended_action,
                failed_api_endpoints,
                slow_api_endpoints,
                created_at
            FROM alerts
            ORDER BY alert_id
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Exception:

        return _read_local_alerts()

    finally:

        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def get_alerts_by_severity(severity):

    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                alert_id,
                incident_id,
                severity,
                area,
                root_cause,
                recommended_action,
                failed_api_endpoints,
                slow_api_endpoints,
                created_at
            FROM alerts
            WHERE severity = %s
            ORDER BY alert_id
        """

        cursor.execute(query, (severity,))

        return cursor.fetchall()

    except Exception:

        alerts = _read_local_alerts()

        return [
            alert
            for alert in alerts
            if alert["severity"] == severity
        ]

    finally:

        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()