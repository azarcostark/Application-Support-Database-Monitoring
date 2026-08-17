from monitoring.incident_analyzer import analyze_incident


def test_healthy_system_has_no_incident():
    report = {
        "overall_status": "HEALTHY",
        "api": [],
        "database": {
            "status": "UP"
        }
    }

    incident = analyze_incident(report)

    assert incident["incident"] is False
    assert incident["severity"] == "NONE"
    assert incident["area"] == "NONE"
    assert incident["failed_api_endpoints"] == []
    assert incident["slow_api_endpoints"] == []


def test_database_failure_is_critical():
    report = {
        "overall_status": "CRITICAL",
        "api": [],
        "database": {
            "status": "DOWN"
        }
    }

    incident = analyze_incident(report)

    assert incident["incident"] is True
    assert incident["severity"] == "CRITICAL"
    assert incident["area"] == "DATABASE"


def test_api_failure_is_critical():
    report = {
        "overall_status": "CRITICAL",
        "api": [
            {
                "endpoint": "/orders",
                "status_ok": False,
                "response_time_ok": False
            }
        ],
        "database": {
            "status": "UP"
        }
    }

    incident = analyze_incident(report)

    assert incident["incident"] is True
    assert incident["severity"] == "CRITICAL"
    assert incident["area"] == "APPLICATION/API"
    assert "/orders" in incident["failed_api_endpoints"]


def test_slow_api_is_warning():
    report = {
        "overall_status": "DEGRADED",
        "api": [
            {
                "endpoint": "/orders",
                "status_ok": True,
                "response_time_ok": False
            }
        ],
        "database": {
            "status": "UP"
        }
    }

    incident = analyze_incident(report)

    assert incident["incident"] is True
    assert incident["severity"] == "WARNING"
    assert incident["area"] == "APPLICATION/API"
    assert "/orders" in incident["slow_api_endpoints"]

def test_database_failure_includes_log_errors(monkeypatch):

    report = {
        "overall_status": "CRITICAL",
        "api": [],
        "database": {
            "status": "DOWN"
        }
    }

    log_summary = {
        "error_messages": [
            "Database connection failed",
            "MySQL server is unavailable"
        ],
        "warning_messages": []
    }

    monkeypatch.setattr(
        "monitoring.incident_analyzer.analyze_log_file",
        lambda: log_summary
    )

    incident = analyze_incident(report)

    assert incident["incident"] is True
    assert incident["severity"] == "CRITICAL"
    assert incident["area"] == "DATABASE"

    assert incident["log_errors"] == [
        "Database connection failed",
        "MySQL server is unavailable"
    ]

def test_print_incident_report_shows_log_evidence(capsys):

    incident = {
        "incident": True,
        "incident_id": 101,
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL connectivity.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": [],
        "log_errors": [
            "Database connection failed"
        ],
        "log_warnings": [
            "Database response is slow"
        ]
    }

    from monitoring.incident_analyzer import print_incident_report

    print_incident_report(incident)

    output = capsys.readouterr().out

    assert "DATABASE" in output
    assert "CRITICAL" in output
    assert "Database connection failed" in output
    assert "Database response is slow" in output