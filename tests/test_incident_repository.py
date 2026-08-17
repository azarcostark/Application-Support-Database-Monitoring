from utils.incident_repository import (
    create_incident,
    get_open_incidents,
    resolve_incident
)


def test_create_and_resolve_incident():
    incident_id = create_incident(
        severity="WARNING",
        area="TEST",
        root_cause="Automated repository test",
        recommended_action="Resolve test incident"
    )

    assert incident_id is not None

    open_incidents = get_open_incidents()

    matching_incident = next(
        incident
        for incident in open_incidents
        if incident["incident_id"] == incident_id
    )

    assert matching_incident["severity"] == "WARNING"
    assert matching_incident["area"] == "TEST"
    assert matching_incident["status"] == "OPEN"

    resolved_count = resolve_incident(incident_id)

    assert resolved_count == 1

    open_incidents_after_resolution = get_open_incidents()

    assert not any(
        incident["incident_id"] == incident_id
        for incident in open_incidents_after_resolution
    )