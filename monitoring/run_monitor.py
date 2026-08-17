from monitoring.health_monitor import run_full_health_check
from monitoring.incident_analyzer import (
    analyze_incident,
    save_incident,
    resolve_recovered_incidents,
    print_incident_report
)


def run_monitoring_cycle():

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

    return {
        "health": health_report,
        "incident": incident_report
    }


if __name__ == "__main__":
    run_monitoring_cycle()