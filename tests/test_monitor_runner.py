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

    result = run_monitoring_cycle()

    assert result["health"]["overall_status"] == "CRITICAL"

    assert result["incident"]["incident"] is True
    assert result["incident"]["severity"] == "CRITICAL"
    assert result["incident"]["area"] == "DATABASE"
    assert result["incident"]["incident_id"] == 999


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