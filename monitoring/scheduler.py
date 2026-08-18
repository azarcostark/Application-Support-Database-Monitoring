import time

from config.settings import MONITOR_INTERVAL_SECONDS
from monitoring.run_monitor import run_monitoring_cycle


def run_scheduler(
    interval_seconds=MONITOR_INTERVAL_SECONDS,
    max_cycles=None,
):
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be greater than 0")

    cycle_count = 0

    while max_cycles is None or cycle_count < max_cycles:

        run_monitoring_cycle()

        cycle_count += 1

        if max_cycles is not None and cycle_count >= max_cycles:
            break

        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_scheduler()