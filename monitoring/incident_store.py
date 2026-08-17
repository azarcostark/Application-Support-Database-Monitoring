import json
from datetime import datetime
from pathlib import Path


INCIDENT_FILE = Path("logs/incidents.json")


def _read_incidents():
    if not INCIDENT_FILE.exists():
        return []

    try:
        with INCIDENT_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def _write_incidents(incidents):
    INCIDENT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with INCIDENT_FILE.open("w", encoding="utf-8") as file:
        json.dump(incidents, file, indent=2)


def create_local_incident(
    severity,
    area,
    root_cause,
    recommended_action
):
    incidents = _read_incidents()

    existing = next(
        (
            incident
            for incident in incidents
            if incident["status"] == "OPEN"
            and incident["severity"] == severity
            and incident["area"] == area
            and incident["root_cause"] == root_cause
        ),
        None
    )

    if existing:
        return existing["incident_id"]

    incident_id = (
        max(
            (
                incident["incident_id"]
                for incident in incidents
            ),
            default=0
        ) + 1
    )

    incident = {
        "incident_id": incident_id,
        "severity": severity,
        "area": area,
        "root_cause": root_cause,
        "recommended_action": recommended_action,
        "status": "OPEN",
        "detected_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "resolved_at": None
    }

    incidents.append(incident)

    _write_incidents(incidents)

    return incident_id


def get_local_open_incidents():
    incidents = _read_incidents()

    return [
        incident
        for incident in incidents
        if incident["status"] == "OPEN"
    ]


def resolve_local_incidents():
    incidents = _read_incidents()

    resolved_count = 0

    for incident in incidents:

        if incident["status"] == "OPEN":

            incident["status"] = "RESOLVED"

            incident["resolved_at"] = (
                datetime.now().isoformat(
                    timespec="seconds"
                )
            )

            resolved_count += 1

    if resolved_count:
        _write_incidents(incidents)

    return resolved_count