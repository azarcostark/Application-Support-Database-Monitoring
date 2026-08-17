from config.database import get_database_connection


def create_incident(
    severity,
    area,
    root_cause,
    recommended_action
):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO incidents (
                severity,
                area,
                root_cause,
                recommended_action,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                severity,
                area,
                root_cause,
                recommended_action,
                "OPEN"
            )
        )

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


def get_open_incidents():
    return get_incidents_by_status("OPEN")


def get_incidents_by_status(
    status,
    severity=None,
    area=None
):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                incident_id,
                severity,
                area,
                root_cause,
                recommended_action,
                status,
                detected_at,
                resolved_at
            FROM incidents
            WHERE status = %s
        """

        parameters = [status]

        if severity is not None:
            query += """
                AND severity = %s
            """
            parameters.append(severity)

        if area is not None:
            query += """
                AND area = %s
            """
            parameters.append(area)

        query += """
            ORDER BY detected_at DESC
        """

        cursor.execute(
            query,
            parameters
        )

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def get_all_incidents():
    connection = None
    cursor = None

    try:
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
                detected_at,
                resolved_at
            FROM incidents
            ORDER BY detected_at DESC
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def get_incident_by_id(incident_id):
    connection = None
    cursor = None

    try:
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
                detected_at,
                resolved_at
            FROM incidents
            WHERE incident_id = %s
        """, (incident_id,))

        return cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def resolve_incident(incident_id):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE incidents
            SET
                status = 'RESOLVED',
                resolved_at = CURRENT_TIMESTAMP
            WHERE incident_id = %s
              AND status = 'OPEN'
        """, (incident_id,))

        connection.commit()

        return cursor.rowcount

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()


def resolve_matching_incident(
    severity,
    area,
    root_cause
):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE incidents
            SET
                status = 'RESOLVED',
                resolved_at = CURRENT_TIMESTAMP
            WHERE severity = %s
              AND area = %s
              AND root_cause = %s
              AND status = 'OPEN'
        """, (
            severity,
            area,
            root_cause
        ))

        connection.commit()

        return cursor.rowcount

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()

def get_incident_summary():
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(status = 'OPEN') AS open,
                SUM(status = 'RESOLVED') AS resolved,
                SUM(severity = 'CRITICAL') AS critical,
                SUM(severity = 'WARNING') AS warning
            FROM incidents
        """)

        summary = cursor.fetchone()

        return summary

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()

def get_incident_summary_by_area():
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                area,
                COUNT(*) AS total,
                SUM(status = 'OPEN') AS open,
                SUM(status = 'RESOLVED') AS resolved
            FROM incidents
            GROUP BY area
            ORDER BY area
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()

def get_incident_statistics():
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                area,
                severity,
                COUNT(*) AS total,
                SUM(status = 'OPEN') AS open,
                SUM(status = 'RESOLVED') AS resolved
            FROM incidents
            GROUP BY area, severity
            ORDER BY area, severity
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()