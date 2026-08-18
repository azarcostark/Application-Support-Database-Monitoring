from monitoring.alert_manager import (
    create_alert,
    format_alert
)


def test_create_alert_for_incident():

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    alert = create_alert(incident_report)

    assert alert is not None
    assert alert["severity"] == "CRITICAL"
    assert alert["area"] == "DATABASE"
    assert (
        alert["root_cause"]
        == "Database health check failed."
    )


def test_no_alert_for_healthy_system():

    incident_report = {
        "incident": False,
        "severity": "NONE",
        "area": "NONE",
        "root_cause": "No incident detected.",
        "recommended_action": "No action required.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    alert = create_alert(incident_report)

    assert alert is None


def test_create_alert_contains_failed_endpoints():

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "APPLICATION/API",
        "root_cause": "API health check failed.",
        "recommended_action": "Check API service.",
        "failed_api_endpoints": [
            "/customers",
            "/orders?status=PENDING"
        ],
        "slow_api_endpoints": []
    }

    alert = create_alert(incident_report)

    assert alert["failed_api_endpoints"] == [
        "/customers",
        "/orders?status=PENDING"
    ]


def test_create_alert_contains_slow_endpoints():

    incident_report = {
        "incident": True,
        "severity": "WARNING",
        "area": "APPLICATION/API",
        "root_cause": "API response time exceeded threshold.",
        "recommended_action": "Investigate API performance.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": [
            "/customers"
        ]
    }

    alert = create_alert(incident_report)

    assert alert["slow_api_endpoints"] == [
        "/customers"
    ]


def test_format_alert():

    alert = {
        "alert_id": None,
        "created_at": "2026-08-17T20:00:00",
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    formatted_alert = format_alert(alert)

    assert "APPLICATION SUPPORT ALERT" in formatted_alert
    assert "CRITICAL" in formatted_alert
    assert "DATABASE" in formatted_alert
    assert "Database health check failed." in formatted_alert
    assert "Check MySQL service status." in formatted_alert


def test_format_alert_with_api_information():

    alert = {
        "alert_id": None,
        "created_at": "2026-08-17T20:00:00",
        "severity": "CRITICAL",
        "area": "APPLICATION/API",
        "root_cause": "API health check failed.",
        "recommended_action": "Check API service.",
        "failed_api_endpoints": [
            "/customers"
        ],
        "slow_api_endpoints": [
            "/orders?status=PENDING"
        ]
    }

    formatted_alert = format_alert(alert)

    assert "/customers" in formatted_alert
    assert "/orders?status=PENDING" in formatted_alert


def test_format_alert_without_alert():

    result = format_alert(None)

    assert result == "No alert generated."