from monitoring.alert_repository import get_all_alerts

from monitoring.health_monitor import run_full_health_check

from utils.incident_repository import (
    get_incident_summary,
    get_incidents_by_status,
)


def build_dashboard_data():

    health_report = run_full_health_check()

    api_results = health_report["api"]

    failed_endpoints = [
        result["endpoint"]
        for result in api_results
        if not result["status_ok"]
    ]

    slow_endpoints = [
        result["endpoint"]
        for result in api_results
        if (
            result["status_ok"]
            and not result["response_time_ok"]
        )
    ]

    if failed_endpoints:
        api_status = "DOWN"
    elif slow_endpoints:
        api_status = "DEGRADED"
    else:
        api_status = "UP"

    database_result = health_report["database"]

    summary = get_incident_summary()

    recent_incidents = get_incidents_by_status(
        "OPEN"
    )[:5]

    for incident in recent_incidents:

        if incident["detected_at"] is not None:
            incident["detected_at"] = (
                incident["detected_at"].isoformat()
            )

        if incident["resolved_at"] is not None:
            incident["resolved_at"] = (
                incident["resolved_at"].isoformat()
            )

    alerts = get_all_alerts()

    for alert in alerts:

        if alert["created_at"] is not None:
            alert["created_at"] = (
                alert["created_at"].isoformat()
            )

        if alert["failed_api_endpoints"]:
            alert["failed_api_endpoints"] = (
                alert["failed_api_endpoints"].split(",")
            )
        else:
            alert["failed_api_endpoints"] = []

        if alert["slow_api_endpoints"]:
            alert["slow_api_endpoints"] = (
                alert["slow_api_endpoints"].split(",")
            )
        else:
            alert["slow_api_endpoints"] = []

    return {
        "system_status": health_report["overall_status"],
        "api": {
            "status": api_status,
            "total_endpoints": len(api_results),
            "healthy_endpoints": (
                len(api_results)
                - len(failed_endpoints)
            ),
            "slow_endpoints": len(slow_endpoints),
            "failed_endpoints": len(failed_endpoints),
            "failed_endpoint_names": failed_endpoints,
            "slow_endpoint_names": slow_endpoints,
        },
        "database": {
            "status": database_result["status"],
            "response_time": database_result["response_time"],
            "query_ok": database_result["query_ok"],
            "response_time_ok": (
                database_result["response_time_ok"]
            ),
        },
        "incidents": {
            "total": int(summary["total"] or 0),
            "open": int(summary["open"] or 0),
            "resolved": int(summary["resolved"] or 0),
            "critical": int(summary["critical"] or 0),
            "warning": int(summary["warning"] or 0),
        },
        "recent_incidents": recent_incidents,
        "alerts": {
            "total": len(alerts),
            "critical": len([
                alert
                for alert in alerts
                if alert["severity"] == "CRITICAL"
            ]),
            "warning": len([
                alert
                for alert in alerts
                if alert["severity"] == "WARNING"
            ]),
            "recent": alerts[-5:],
        },
    }