from monitoring.health_monitor import run_full_health_check
from monitoring.log_analyzer import analyze_log_file
from utils.logger import get_logger

from utils.incident_repository import (
    create_incident as create_database_incident,
    get_open_incidents as get_database_open_incidents,
    resolve_matching_incident
)

from monitoring.incident_store import (
    create_local_incident,
    get_local_open_incidents,
    resolve_local_incidents
)


logger = get_logger("incident_analyzer")


def analyze_incident(report):
    """
    Analyze the health report and determine
    whether an incident exists.
    """

    log_summary = analyze_log_file()

    log_errors = log_summary.get(
        "error_messages",
        []
    )

    log_warnings = log_summary.get(
        "warning_messages",
        []
    )


    if report["overall_status"] == "HEALTHY":
       return {
            "incident": False,
            "severity": "NONE",
            "area": "NONE",
            "root_cause": "No incident detected.",
            "recommended_action": "No action required.",
            "failed_api_endpoints": [],
            "slow_api_endpoints": [],
            "log_errors": log_errors,
            "log_warnings": log_warnings
            }

    database = report["database"]
    api_results = report["api"]

    database_down = database["status"] != "UP"

    failed_api_endpoints = [
        result["endpoint"]
        for result in api_results
        if not result["status_ok"]
    ]

    slow_api_endpoints = [
        result["endpoint"]
        for result in api_results
        if result["status_ok"]
        and not result["response_time_ok"]
    ]

    if database_down:
        severity = "CRITICAL"
        area = "DATABASE"
        root_cause = "Database health check failed."
        recommended_action = (
            "Check MySQL service status, database connectivity, "
            "and database logs."
        )

    elif failed_api_endpoints:
        severity = "CRITICAL"
        area = "APPLICATION/API"
        root_cause = (
            "One or more API health checks failed."
        )
        recommended_action = (
            "Investigate the failed API endpoints and review "
            "application logs."
        )

    elif slow_api_endpoints:
        severity = "WARNING"
        area = "APPLICATION/API"
        root_cause = (
            "One or more API endpoints exceeded "
            "the response-time threshold."
        )
        recommended_action = (
            "Review application logs, database queries, "
            "and API performance."
        )

    else:
        severity = "WARNING"
        area = "APPLICATION"
        root_cause = "Application health is degraded."
        recommended_action = (
            "Review monitoring results and application logs."
        )

    return {
        "incident": True,
        "severity": severity,
        "area": area,
        "root_cause": root_cause,
        "recommended_action": recommended_action,
        "failed_api_endpoints": failed_api_endpoints,
        "slow_api_endpoints": slow_api_endpoints,
        "log_errors": log_errors,
        "log_warnings": log_warnings

    }


def save_incident(incident):
    """
    Save the incident to MySQL.

    If MySQL is unavailable, save it to the
    local JSON fallback store.
    """

    if not incident["incident"]:
        return None

    severity = incident["severity"]
    area = incident["area"]
    root_cause = incident["root_cause"]
    recommended_action = incident["recommended_action"]

    try:
        open_incidents = get_database_open_incidents()

        duplicate = any(
            existing["severity"] == severity
            and existing["area"] == area
            and existing["root_cause"] == root_cause
            for existing in open_incidents
        )

        if duplicate:
            logger.warning(
                "OPEN INCIDENT ALREADY EXISTS | "
                "severity=%s | area=%s",
                severity,
                area
            )
            return None

        incident_id = create_database_incident(
            severity=severity,
            area=area,
            root_cause=root_cause,
            recommended_action=recommended_action
        )

        logger.warning(
            "INCIDENT CREATED IN MYSQL | "
            "incident_id=%s | severity=%s | area=%s",
            incident_id,
            severity,
            area
        )

        return incident_id

    except Exception as error:
        logger.error(
            "MYSQL INCIDENT STORAGE FAILED | error=%s",
            error
        )

        local_incident_id = create_local_incident(
            severity=severity,
            area=area,
            root_cause=root_cause,
            recommended_action=recommended_action
        )

        logger.warning(
            "INCIDENT SAVED TO LOCAL FALLBACK | "
            "incident_id=%s | severity=%s | area=%s",
            local_incident_id,
            severity,
            area
        )

        return local_incident_id


def resolve_recovered_incidents(report):
    """
    Resolve incidents when the system becomes healthy.
    """

    if report["overall_status"] != "HEALTHY":
        return 0

    resolved_count = 0

    # Resolve incidents stored in MySQL
    try:
        open_incidents = get_database_open_incidents()

        for incident in open_incidents:
            resolved_count += resolve_matching_incident(
                severity=incident["severity"],
                area=incident["area"],
                root_cause=incident["root_cause"]
            )

    except Exception as error:
        logger.error(
            "MYSQL INCIDENT RECOVERY FAILED | error=%s",
            error
        )

    # Resolve incidents stored in local fallback
    try:
        local_incidents = get_local_open_incidents()

        if local_incidents:
            resolved_count += resolve_local_incidents()

    except Exception as error:
        logger.error(
            "LOCAL INCIDENT RECOVERY FAILED | error=%s",
            error
        )

    if resolved_count > 0:
        logger.info(
            "INCIDENTS RESOLVED | count=%s",
            resolved_count
        )

    return resolved_count


def print_incident_report(incident):

    print("=" * 60)
    print("APPLICATION SUPPORT INCIDENT REPORT")
    print("=" * 60)

    print(
        f"Incident       : {incident['incident']}"
    )

    print(
        f"Incident ID    : {incident.get('incident_id')}"
    )

    print(
        f"Severity       : {incident['severity']}"
    )

    print(
        f"Area           : {incident['area']}"
    )

    print(
        f"Root Cause     : {incident['root_cause']}"
    )

    print(
        f"Recommended    : {incident['recommended_action']}"
    )

    if incident["failed_api_endpoints"]:
        print("\nFailed API Endpoints:")

        for endpoint in incident["failed_api_endpoints"]:
            print(f"  - {endpoint}")

    if incident["slow_api_endpoints"]:
        print("\nSlow API Endpoints:")

        for endpoint in incident["slow_api_endpoints"]:
            print(f"  - {endpoint}")

    if incident.get("log_errors"):
        print("\nLog Errors:")

        for error in incident["log_errors"]:
            print(f"  - {error}")

    if incident.get("log_warnings"):
        print("\nLog Warnings:")

        for warning in incident["log_warnings"]:
            print(f"  - {warning}")

    print("=" * 60)


if __name__ == "__main__":

    health_report = run_full_health_check()

    if health_report["overall_status"] == "HEALTHY":

        resolved_count = resolve_recovered_incidents(
            health_report
        )

        print(
            f"Recovered incidents : {resolved_count}"
        )

    incident_report = analyze_incident(
        health_report
    )

    if incident_report["incident"]:

        incident_id = save_incident(
            incident_report
        )

        incident_report["incident_id"] = incident_id

    else:

        incident_report["incident_id"] = None

    print_incident_report(
        incident_report
    )