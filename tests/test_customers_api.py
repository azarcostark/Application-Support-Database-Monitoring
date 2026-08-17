import requests

from config.database import get_database_connection


BASE_URL = "http://127.0.0.1:5000"


def test_get_customers():
    response = requests.get(f"{BASE_URL}/customers")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "customers" in data
    assert data["count"] == len(data["customers"])


def test_customer_count_matches_database():
    response = requests.get(f"{BASE_URL}/customers")

    assert response.status_code == 200

    api_data = response.json()

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")

    database_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert api_data["count"] == database_count


def test_customer_data_matches_database():
    response = requests.get(f"{BASE_URL}/customers")

    assert response.status_code == 200

    api_data = response.json()

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            customer_id,
            name,
            email
        FROM customers
        ORDER BY customer_id
    """)

    database_customers = cursor.fetchall()

    cursor.close()
    connection.close()

    for api_customer, database_customer in zip(
        api_data["customers"],
        database_customers
    ):
        assert api_customer["customer_id"] == database_customer["customer_id"]
        assert api_customer["name"] == database_customer["name"]
        assert api_customer["email"] == database_customer["email"]