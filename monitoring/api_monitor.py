import time

import requests

from config.settings import (
    API_BASE_URL,
    API_RESPONSE_TIME_THRESHOLD
)

from utils.logger import get_logger


BASE_URL = API_BASE_URL

RESPONSE_TIME_THRESHOLD = API_RESPONSE_TIME_THRESHOLD

logger = get_logger("api_monitor")

def check_endpoint(endpoint, expected_status=200, timeout=5):
    url = f"{BASE_URL}{endpoint}"

    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)

        response_time = time.perf_counter() - start_time

        status_ok = response.status_code == expected_status
        response_time_ok = (
    response_time < API_RESPONSE_TIME_THRESHOLD
)

        if status_ok and response_time_ok:
            logger.info(
                "MONITOR PASS | %s | status=%s | response_time=%.4fs",
                endpoint,
                response.status_code,
                response_time,
            )

        elif status_ok and not response_time_ok:
            logger.warning(
                "MONITOR SLOW | %s | status=%s | response_time=%.4fs | threshold=%.2fs",
                endpoint,
                response.status_code,
                response_time,
                API_RESPONSE_TIME_THRESHOLD,
            )

        else:
            logger.error(
                "MONITOR FAIL | %s | expected_status=%s | actual_status=%s | response_time=%.4fs",
                endpoint,
                expected_status,
                response.status_code,
                response_time,
            )

        return {
            "endpoint": endpoint,
            "status_code": response.status_code,
            "expected_status": expected_status,
            "response_time": response_time,
            "status_ok": status_ok,
            "response_time_ok": response_time_ok,
        }

    except requests.RequestException as error:
        response_time = time.perf_counter() - start_time

        logger.error(
            "MONITOR ERROR | %s | response_time=%.4fs | error=%s",
            endpoint,
            response_time,
            error,
        )

        return {
            "endpoint": endpoint,
            "status_code": None,
            "expected_status": expected_status,
            "response_time": response_time,
            "status_ok": False,
            "response_time_ok": False,
            "error": str(error),
        }


def run_api_health_check():
    endpoints = [
        "/health",
        "/customers",
        "/orders?status=PENDING",
    ]

    results = []

    for endpoint in endpoints:
        result = check_endpoint(endpoint)
        results.append(result)

    return results


if __name__ == "__main__":
    results = run_api_health_check()

    for result in results:
        print(result)