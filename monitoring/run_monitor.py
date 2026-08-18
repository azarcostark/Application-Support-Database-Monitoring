from monitoring.health_monitor import run_full_health_check

from monitoring.incident_analyzer import (
    analyze_incident,
    save_incident,
    resolve_recovered_incidents,
    print_incident_report
)

from monitoring.alert_manager import create_alert

from monitoring.alert_repository import (
    create_alert as save_alert
)

from monitoring.notification_service import (
    send_notification
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

    alert = create_alert(
        incident_report
    )

    if alert is not None:

        alert_id = save_alert(
            alert,
            incident_id=incident_report["incident_id"]
        )

        alert["alert_id"] = alert_id

        notification_sent = send_notification(
            alert
        )

    else:

        notification_sent = False

    print_incident_report(
        incident_report
    )

    return {
        "health": health_report,
        "incident": incident_report,
        "alert": alert,
        "notification_sent": notification_sent
    }


if __name__ == "__main__":
    run_monitoring_cycle()