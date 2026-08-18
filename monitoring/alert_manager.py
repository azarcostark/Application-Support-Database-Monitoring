from datetime import datetime


def create_alert(incident_report):

    if not incident_report["incident"]:
        return None

    alert = {
        "alert_id": None,
        "created_at": datetime.now().isoformat(),
        "severity": incident_report["severity"],
        "area": incident_report["area"],
        "root_cause": incident_report["root_cause"],
        "recommended_action": incident_report[
            "recommended_action"
        ],
        "failed_api_endpoints": incident_report[
            "failed_api_endpoints"
        ],
        "slow_api_endpoints": incident_report[
            "slow_api_endpoints"
        ]
    }

    return alert


def format_alert(alert):

    if alert is None:
        return "No alert generated."

    lines = [
        "============================================================",
        "APPLICATION SUPPORT ALERT",
        "============================================================",
        f"Severity          : {alert['severity']}",
        f"Area              : {alert['area']}",
        f"Root Cause        : {alert['root_cause']}",
        f"Recommended Action: {alert['recommended_action']}"
    ]

    if alert["failed_api_endpoints"]:
        lines.append(
            "Failed API Endpoints: "
            + ", ".join(alert["failed_api_endpoints"])
        )

    if alert["slow_api_endpoints"]:
        lines.append(
            "Slow API Endpoints: "
            + ", ".join(alert["slow_api_endpoints"])
        )

    lines.append(
        f"Created At        : {alert['created_at']}"
    )

    lines.append(
        "============================================================"
    )

    return "\n".join(lines)