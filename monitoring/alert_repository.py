from config.database import get_database_connection


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
            slow_api_endpoints
        )

        cursor.execute(query, values)

        connection.commit()

        return cursor.lastrowid

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

    finally:

        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()