from monitoring.alert_manager import format_alert


def send_notification(alert):
    """
    Send a notification for an alert.

    Returns True when a notification is generated.
    Returns False when no alert exists.
    """

    if alert is None:
        return False

    message = format_alert(alert)

    print(message)

    return True