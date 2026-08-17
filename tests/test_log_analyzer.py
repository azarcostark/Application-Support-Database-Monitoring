from monitoring.log_analyzer import analyze_log_file


def test_log_analyzer_reads_application_log():
    summary = analyze_log_file()

    assert "total_lines" in summary
    assert "info_count" in summary
    assert "warning_count" in summary
    assert "error_count" in summary

    assert "api_requests" in summary
    assert "slow_api_requests" in summary

    assert summary["total_lines"] >= 0
    assert isinstance(summary["api_requests"], list)
    assert isinstance(summary["slow_api_requests"], list)


def test_log_analyzer_extracts_error_messages(tmp_path):

    log_file = tmp_path / "test_application.log"

    log_file.write_text(
        "2026-08-17 03:00:00 | INFO | test | Application started\n"
        "2026-08-17 03:01:00 | ERROR | test | Database connection failed\n"
        "2026-08-17 03:02:00 | WARNING | test | API response is slow\n"
        "2026-08-17 03:03:00 | ERROR | test | Unable to retrieve customers\n",
        encoding="utf-8"
    )

    from monitoring.log_analyzer import analyze_log_file

    summary = analyze_log_file(str(log_file))

    assert summary["error_count"] == 2

    assert len(summary["error_messages"]) == 2

    assert "Database connection failed" in summary["error_messages"][0]

    assert "Unable to retrieve customers" in summary["error_messages"][1]

def test_log_analyzer_extracts_warning_messages(tmp_path):

    log_file = tmp_path / "test_application.log"

    log_file.write_text(
        "2026-08-17 03:00:00 | INFO | test | Application started\n"
        "2026-08-17 03:01:00 | WARNING | test | API response is slow\n"
        "2026-08-17 03:02:00 | WARNING | test | Database response is slow\n",
        encoding="utf-8"
    )

    from monitoring.log_analyzer import analyze_log_file

    summary = analyze_log_file(str(log_file))

    assert summary["warning_count"] == 2

    assert len(summary["warning_messages"]) == 2

    assert "API response is slow" in summary["warning_messages"][0]

    assert "Database response is slow" in summary["warning_messages"][1]