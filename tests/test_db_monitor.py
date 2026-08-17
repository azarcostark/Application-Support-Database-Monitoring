from monitoring.db_monitor import check_database


def test_database_monitor():
    result = check_database()

    assert result["status"] == "UP"
    assert result["query_ok"] is True
    assert result["response_time_ok"] is True