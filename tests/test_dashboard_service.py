from app.dashboard_service import build_dashboard_data


def test_build_dashboard_data_returns_dictionary():

    dashboard = build_dashboard_data()

    assert isinstance(dashboard, dict)


def test_dashboard_service_contains_system_status():

    dashboard = build_dashboard_data()

    assert "system_status" in dashboard

    assert dashboard["system_status"] in {
        "HEALTHY",
        "DEGRADED",
        "CRITICAL"
    }


def test_dashboard_service_contains_api_information():

    dashboard = build_dashboard_data()

    api = dashboard["api"]

    assert "status" in api
    assert "total_endpoints" in api
    assert "healthy_endpoints" in api
    assert "slow_endpoints" in api
    assert "failed_endpoints" in api

    assert api["total_endpoints"] >= 0
    assert api["healthy_endpoints"] >= 0
    assert api["slow_endpoints"] >= 0
    assert api["failed_endpoints"] >= 0


def test_dashboard_service_contains_database_information():

    dashboard = build_dashboard_data()

    database = dashboard["database"]

    assert "status" in database
    assert "response_time" in database
    assert "query_ok" in database
    assert "response_time_ok" in database

    assert database["status"] in {
        "UP",
        "DOWN"
    }


def test_dashboard_service_contains_incident_information():

    dashboard = build_dashboard_data()

    incidents = dashboard["incidents"]

    assert "total" in incidents
    assert "open" in incidents
    assert "resolved" in incidents
    assert "critical" in incidents
    assert "warning" in incidents


def test_dashboard_service_contains_recent_incidents():

    dashboard = build_dashboard_data()

    assert "recent_incidents" in dashboard

    assert isinstance(
        dashboard["recent_incidents"],
        list
    )


def test_dashboard_service_contains_alert_information():

    dashboard = build_dashboard_data()

    alerts = dashboard["alerts"]

    assert "total" in alerts
    assert "critical" in alerts
    assert "warning" in alerts
    assert "recent" in alerts

    assert isinstance(
        alerts["recent"],
        list
    )