from monitoring.health_monitor import run_full_health_check


def test_full_health_check():
    report = run_full_health_check()

    assert "overall_status" in report
    assert "api" in report
    assert "database" in report

    assert report["overall_status"] in {
        "HEALTHY",
        "DEGRADED",
        "CRITICAL",
    }

    assert len(report["api"]) == 3