import requests


BASE_URL = "http://127.0.0.1:5000"


def test_get_all_orders():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"page": 1, "limit": 50}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 50
    assert data["count"] == len(data["orders"])
    assert data["count"] <= 50

    assert "total" in data
    assert "total_pages" in data
    assert "has_next" in data
    assert "has_previous" in data


def test_get_pending_orders():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={
            "status": "PENDING",
            "page": 1,
            "limit": 50
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 50
    assert data["count"] == len(data["orders"])
    assert data["count"] <= 50

    assert data["total"] > 0
    assert data["total_pages"] > 0
    assert data["has_next"] is True
    assert data["has_previous"] is False

    for order in data["orders"]:
        assert order["status"] == "PENDING"


def test_get_orders_by_customer():
    customer_id = 1

    response = requests.get(
        f"{BASE_URL}/orders",
        params={
            "customer_id": customer_id,
            "page": 1,
            "limit": 50
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 50
    assert data["count"] == len(data["orders"])
    assert data["count"] <= 50

    assert data["total"] >= data["count"]
    assert data["total_pages"] > 0

    for order in data["orders"]:
        assert order["customer_id"] == customer_id


def test_get_orders_page_2():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={
            "status": "PENDING",
            "page": 2,
            "limit": 50
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 50
    assert data["count"] == len(data["orders"])
    assert data["count"] <= 50

    assert data["has_previous"] is True

    for order in data["orders"]:
        assert order["status"] == "PENDING"


def test_custom_page_size():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={
            "status": "PENDING",
            "page": 1,
            "limit": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["count"] == len(data["orders"])
    assert data["count"] <= 10


def test_invalid_order_status():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"status": "FAILED"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_customer_id():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"customer_id": "abc"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_page():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"page": "abc"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_limit():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"limit": "abc"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_page_must_be_positive():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"page": 0}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_limit_must_be_positive():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"limit": 0}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_limit_cannot_exceed_100():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"limit": 101}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"