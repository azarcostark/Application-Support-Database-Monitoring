from monitoring.incident_store import (
    create_local_incident,
    get_local_open_incidents,
    resolve_local_incidents
)


def test_local_incident_lifecycle(tmp_path, monkeypatch):

    import monitoring.incident_store as incident_store

    test_file = tmp_path / "incidents.json"

    monkeypatch.setattr(
        incident_store,
        "INCIDENT_FILE",
        test_file
    )

    incident_id = create_local_incident(
        severity="CRITICAL",
        area="DATABASE",
        root_cause="Test database failure",
        recommended_action="Test recovery"
    )

    assert incident_id == 1

    open_incidents = get_local_open_incidents()

    assert len(open_incidents) == 1

    assert open_incidents[0]["status"] == "OPEN"

    resolved_count = resolve_local_incidents()

    assert resolved_count == 1

    open_incidents = get_local_open_incidents()

    assert len(open_incidents) == 0