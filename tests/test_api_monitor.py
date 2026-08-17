from monitoring.api_monitor import RESPONSE_TIME_THRESHOLD


def test_response_time_threshold():
    assert RESPONSE_TIME_THRESHOLD == 1.0