from monitoring.run_monitor import run_monitoring_cycle


def test_monitoring_cycle_healthy(monkeypatch):

    health_report = {
        "overall_status": "HEALTHY",
        "api": [],
        "database": {
            "status": "UP",
            "response_time_ok": True
        }
    }

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.resolve_recovered_incidents",
        lambda report: 3
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: {
            "incident": False,
            "severity": "NONE",
            "area": "NONE",
            "root_cause": "No incident detected.",
            "recommended_action": "No action required.",
            "failed_api_endpoints": [],
            "slow_api_endpoints": []
        }
    )

    result = run_monitoring_cycle()

    assert result["health"]["overall_status"] == "HEALTHY"
    assert result["incident"]["incident"] is False
    assert result["incident"]["incident_id"] is None
    assert result["alert"] is None
    assert result["notification_sent"] is False


def test_monitoring_cycle_creates_incident(monkeypatch):

    health_report = {
        "overall_status": "CRITICAL",
        "api": [],
        "database": {
            "status": "DOWN",
            "response_time_ok": False
        }
    }

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_incident",
        lambda incident: 999
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: 500
    )

    result = run_monitoring_cycle()

    assert result["health"]["overall_status"] == "CRITICAL"
    assert result["incident"]["incident"] is True
    assert result["incident"]["severity"] == "CRITICAL"
    assert result["incident"]["area"] == "DATABASE"
    assert result["incident"]["incident_id"] == 999
    assert result["alert"] is not None
    assert result["alert"]["alert_id"] == 500


def test_monitoring_cycle_resolves_incidents(monkeypatch):

    health_report = {
        "overall_status": "HEALTHY",
        "api": [],
        "database": {
            "status": "UP",
            "response_time_ok": True
        }
    }

    incident_report = {
        "incident": False,
        "severity": "NONE",
        "area": "NONE",
        "root_cause": "No incident detected.",
        "recommended_action": "No action required.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.resolve_recovered_incidents",
        lambda report: 5
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    result = run_monitoring_cycle()

    assert result["health"]["overall_status"] == "HEALTHY"
    assert result["incident"]["incident"] is False
    assert result["incident"]["incident_id"] is None
    assert result["alert"] is None
    assert result["notification_sent"] is False


def test_monitoring_cycle_creates_alert_for_database_failure(
    monkeypatch
):

    health_report = {
        "overall_status": "CRITICAL",
        "api": [],
        "database": {
            "status": "DOWN",
            "response_time_ok": False
        }
    }

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_incident",
        lambda incident: 1001
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: 501
    )

    result = run_monitoring_cycle()

    alert = result["alert"]

    assert alert is not None
    assert alert["alert_id"] == 501
    assert alert["severity"] == "CRITICAL"
    assert alert["area"] == "DATABASE"
    assert alert["root_cause"] == (
        "Database health check failed."
    )


def test_monitoring_cycle_alert_contains_failed_endpoints(
    monkeypatch
):

    health_report = {
        "overall_status": "CRITICAL",
        "api": [
            {
                "endpoint": "/customers",
                "status_ok": False,
                "response_time_ok": False
            }
        ],
        "database": {
            "status": "UP",
            "response_time_ok": True
        }
    }

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "APPLICATION/API",
        "root_cause": "One or more API health checks failed.",
        "recommended_action": "Investigate failed API endpoints.",
        "failed_api_endpoints": ["/customers"],
        "slow_api_endpoints": []
    }

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_incident",
        lambda incident: 1002
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: 502
    )

    result = run_monitoring_cycle()

    alert = result["alert"]

    assert alert is not None
    assert alert["alert_id"] == 502
    assert alert["failed_api_endpoints"] == [
        "/customers"
    ]


def test_monitoring_cycle_alert_contains_slow_endpoints(
    monkeypatch
):

    health_report = {
        "overall_status": "DEGRADED",
        "api": [
            {
                "endpoint": "/orders",
                "status_ok": True,
                "response_time_ok": False
            }
        ],
        "database": {
            "status": "UP",
            "response_time_ok": True
        }
    }

    incident_report = {
        "incident": True,
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

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_incident",
        lambda incident: 1003
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: 503
    )

    result = run_monitoring_cycle()

    alert = result["alert"]

    assert alert is not None
    assert alert["alert_id"] == 503
    assert alert["severity"] == "WARNING"
    assert alert["slow_api_endpoints"] == ["/orders"]


def test_monitoring_cycle_calls_alert_manager(monkeypatch):

    health_report = {
        "overall_status": "CRITICAL",
        "api": [],
        "database": {
            "status": "DOWN",
            "response_time_ok": False
        }
    }

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    alert_calls = []
    saved_alerts = []

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_incident",
        lambda incident: 1004
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.create_alert",
        lambda report: (
            alert_calls.append(report)
            or {
                "alert_id": None,
                "created_at": "test",
                "severity": "CRITICAL",
                "area": "DATABASE",
                "root_cause": "Database health check failed.",
                "recommended_action": (
                    "Check MySQL service status."
                ),
                "failed_api_endpoints": [],
                "slow_api_endpoints": []
            }
        )
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: (
            saved_alerts.append(
                (alert, incident_id)
            )
            or 504
        )
    )

    result = run_monitoring_cycle()

    assert len(alert_calls) == 1
    assert alert_calls[0]["incident"] is True
    assert result["alert"] is not None
    assert result["alert"]["alert_id"] == 504

    assert len(saved_alerts) == 1
    assert saved_alerts[0][1] == 1004


def test_monitoring_cycle_sends_notification(monkeypatch):

    health_report = {
        "overall_status": "CRITICAL",
        "api": [],
        "database": {
            "status": "DOWN",
            "response_time_ok": False
        }
    }

    incident_report = {
        "incident": True,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    notifications = []

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_incident",
        lambda incident: 100
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.create_alert",
        lambda incident: {
            "alert_id": None,
            "created_at": "2026-08-18T10:00:00",
            "severity": "CRITICAL",
            "area": "DATABASE",
            "root_cause": "Database health check failed.",
            "recommended_action": "Check MySQL service status.",
            "failed_api_endpoints": [],
            "slow_api_endpoints": []
        }
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: 505
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.send_notification",
        lambda alert: notifications.append(alert) or True
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.print_incident_report",
        lambda report: None
    )

    result = run_monitoring_cycle()

    assert len(notifications) == 1
    assert notifications[0]["severity"] == "CRITICAL"
    assert result["notification_sent"] is True
    assert result["alert"]["alert_id"] == 505


def test_monitoring_cycle_does_not_notify_when_healthy(monkeypatch):

    health_report = {
        "overall_status": "HEALTHY",
        "api": [],
        "database": {
            "status": "UP",
            "response_time_ok": True
        }
    }

    incident_report = {
        "incident": False,
        "severity": "NONE",
        "area": "NONE",
        "root_cause": "No incident detected.",
        "recommended_action": "No action required.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    notifications = []

    monkeypatch.setattr(
        "monitoring.run_monitor.run_full_health_check",
        lambda: health_report
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.resolve_recovered_incidents",
        lambda report: 0
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.analyze_incident",
        lambda report: incident_report.copy()
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.create_alert",
        lambda incident: None
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.save_alert",
        lambda alert, incident_id=None: 506
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.send_notification",
        lambda alert: notifications.append(alert) or True
    )

    monkeypatch.setattr(
        "monitoring.run_monitor.print_incident_report",
        lambda report: None
    )

    result = run_monitoring_cycle()

    assert len(notifications) == 0
    assert result["notification_sent"] is False
    assert result["alert"] is None