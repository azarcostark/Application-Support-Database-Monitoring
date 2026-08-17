from monitoring.api_monitor import run_api_health_check
from monitoring.db_monitor import check_database
from utils.logger import get_logger


logger = get_logger("health_monitor")


def run_full_health_check():
    api_results = run_api_health_check()
    database_result = check_database()

    api_healthy = all(
        result["status_ok"]
        for result in api_results
    )

    database_healthy = database_result["status"] == "UP"

    api_slow = any(
        not result["response_time_ok"]
        for result in api_results
        if result["status_ok"]
    )

    database_slow = (
        database_healthy
        and not database_result["response_time_ok"]
    )

    if not api_healthy or not database_healthy:
        overall_status = "CRITICAL"

    elif api_slow or database_slow:
        overall_status = "DEGRADED"

    else:
        overall_status = "HEALTHY"

    report = {
        "overall_status": overall_status,
        "api": api_results,
        "database": database_result,
    }

    logger.info(
        "FULL HEALTH CHECK | overall_status=%s",
        overall_status,
    )

    return report


def print_health_report(report):
    print("=" * 60)
    print("APPLICATION SUPPORT HEALTH REPORT")
    print("=" * 60)

    print(f"\nOverall Status: {report['overall_status']}")

    print("\nAPI")
    print("-" * 60)

    for result in report["api"]:
        endpoint = result["endpoint"]
        status_code = result["status_code"]
        response_time = result["response_time"]

        if result["status_ok"] and result["response_time_ok"]:
            status = "UP"

        elif result["status_ok"]:
            status = "SLOW"

        else:
            status = "DOWN"

        print(
            f"{endpoint:<30} "
            f"{status:<8} "
            f"HTTP={status_code} "
            f"time={response_time:.4f}s"
        )

    print("\nDATABASE")
    print("-" * 60)

    database = report["database"]

    print(
        f"MySQL{'':<25} "
        f"{database['status']:<8} "
        f"time={database['response_time']:.4f}s"
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    health_report = run_full_health_check()
    print_health_report(health_report)