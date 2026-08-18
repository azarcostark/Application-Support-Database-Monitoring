import pytest

from monitoring.alert_repository import (
    create_alert,
    get_alert_by_id,
    get_all_alerts,
    get_alerts_by_severity
)


def create_test_alert():

    return {
        "alert_id": None,
        "created_at": None,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }


def test_create_alert():

    alert = create_test_alert()

    alert_id = create_alert(
        alert
    )

    assert alert_id is not None
    assert isinstance(alert_id, int)

    stored_alert = get_alert_by_id(
        alert_id
    )

    assert stored_alert is not None
    assert stored_alert["alert_id"] == alert_id
    assert stored_alert["severity"] == "CRITICAL"
    assert stored_alert["area"] == "DATABASE"

    assert stored_alert["root_cause"] == (
        "Database health check failed."
    )


def test_get_alert_by_id():

    alert = create_test_alert()

    alert_id = create_alert(
        alert
    )

    result = get_alert_by_id(
        alert_id
    )

    assert result is not None
    assert result["alert_id"] == alert_id


def test_get_missing_alert():

    result = get_alert_by_id(
        999999
    )

    assert result is None


def test_get_all_alerts():

    alert = create_test_alert()

    alert_id = create_alert(
        alert
    )

    alerts = get_all_alerts()

    assert isinstance(alerts, list)

    alert_ids = [
        item["alert_id"]
        for item in alerts
    ]

    assert alert_id in alert_ids


def test_get_alerts_by_severity():

    alert = create_test_alert()

    alert_id = create_alert(
        alert
    )

    alerts = get_alerts_by_severity(
        "CRITICAL"
    )

    assert isinstance(alerts, list)

    matching_alert_ids = [
        item["alert_id"]
        for item in alerts
    ]

    assert alert_id in matching_alert_ids

    for item in alerts:
        assert item["severity"] == "CRITICAL"


def test_create_warning_alert():

    alert = {
        "alert_id": None,
        "created_at": None,
        "severity": "WARNING",
        "area": "APPLICATION/API",
        "root_cause": (
            "One or more API endpoints exceeded "
            "the response-time threshold."
        ),
        "recommended_action": (
            "Investigate slow API endpoints."
        ),
        "failed_api_endpoints": [],
        "slow_api_endpoints": ["/orders"]
    }

    alert_id = create_alert(
        alert
    )

    assert alert_id is not None

    stored_alert = get_alert_by_id(
        alert_id
    )

    assert stored_alert is not None
    assert stored_alert["severity"] == "WARNING"
    assert stored_alert["area"] == "APPLICATION/API"
    assert stored_alert["slow_api_endpoints"] == "/orders"