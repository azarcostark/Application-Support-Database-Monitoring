from monitoring.scheduler import run_scheduler


def test_scheduler_runs_monitoring_cycle(monkeypatch):

    cycles = []

    monkeypatch.setattr(
        "monitoring.scheduler.run_monitoring_cycle",
        lambda: cycles.append(1)
    )

    run_scheduler(
        interval_seconds=1,
        max_cycles=1
    )

    assert len(cycles) == 1


def test_scheduler_runs_multiple_cycles(monkeypatch):

    cycles = []

    monkeypatch.setattr(
        "monitoring.scheduler.run_monitoring_cycle",
        lambda: cycles.append(1)
    )

    monkeypatch.setattr(
        "monitoring.scheduler.time.sleep",
        lambda seconds: None
    )

    run_scheduler(
        interval_seconds=60,
        max_cycles=3
    )

    assert len(cycles) == 3


def test_scheduler_waits_between_cycles(monkeypatch):

    cycles = []
    wait_times = []

    monkeypatch.setattr(
        "monitoring.scheduler.run_monitoring_cycle",
        lambda: cycles.append(1)
    )

    monkeypatch.setattr(
        "monitoring.scheduler.time.sleep",
        lambda seconds: wait_times.append(seconds)
    )

    run_scheduler(
        interval_seconds=30,
        max_cycles=3
    )

    assert len(cycles) == 3
    assert wait_times == [30, 30]


def test_scheduler_rejects_invalid_interval():

    try:
        run_scheduler(
            interval_seconds=0,
            max_cycles=1
        )

        assert False

    except ValueError as error:
        assert str(error) == (
            "interval_seconds must be greater than 0"
        )


def test_scheduler_stops_after_max_cycles(monkeypatch):

    cycles = []

    monkeypatch.setattr(
        "monitoring.scheduler.run_monitoring_cycle",
        lambda: cycles.append(1)
    )

    monkeypatch.setattr(
        "monitoring.scheduler.time.sleep",
        lambda seconds: None
    )

    run_scheduler(
        interval_seconds=10,
        max_cycles=5
    )

    assert len(cycles) == 5