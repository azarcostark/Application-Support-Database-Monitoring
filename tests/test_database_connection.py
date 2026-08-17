from config.database import get_database_connection


def test_database_connection():
    connection = get_database_connection()

    assert connection.is_connected()

    connection.close()


def test_database_query():
    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")

    result = cursor.fetchone()

    assert result[0] == 5

    cursor.close()
    connection.close()