from monitoring.notification_service import (
    send_notification
)


def test_send_notification_with_alert(capsys):

    alert = {
        "alert_id": None,
        "created_at": "2026-08-18T10:00:00",
        "severity": "CRITICAL",
        "area": "DATABASE",
        "root_cause": "Database health check failed.",
        "recommended_action": "Check MySQL service status.",
        "failed_api_endpoints": [],
        "slow_api_endpoints": []
    }

    result = send_notification(alert)

    captured = capsys.readouterr()

    assert result is True
    assert "APPLICATION SUPPORT ALERT" in captured.out
    assert "CRITICAL" in captured.out
    assert "DATABASE" in captured.out


def test_send_notification_without_alert(capsys):

    result = send_notification(None)

    captured = capsys.readouterr()

    assert result is False
    assert captured.out == ""