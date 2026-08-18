import os
import re

from config.settings import API_RESPONSE_TIME_THRESHOLD
from utils.logger import LOG_FILE

LOG_LEVEL_PATTERN = re.compile(
    r"\|\s+(INFO|WARNING|ERROR)\s+\|"
)

API_REQUEST_PATTERN = re.compile(
    r"(GET|POST|PUT|DELETE)\s+(\S+)\s+\|\s+status=(\d+)\s+\|\s+response_time=([0-9.]+)s"
)


def analyze_log_file(log_file=LOG_FILE):
    summary = {
        "total_lines": 0,
        "info_count": 0,
        "warning_count": 0,
        "error_count": 0,
        "warning_messages": [],
        "error_messages": [],
        "monitor_pass_count": 0,
        "monitor_slow_count": 0,
        "monitor_fail_count": 0,
        "monitor_error_count": 0,
        "db_pass_count": 0,
        "db_slow_count": 0,
        "db_error_count": 0,
        "api_requests": [],
        "slow_api_requests": [],
    }

    if not os.path.exists(log_file):
        return summary

    with open(log_file, "r", encoding="utf-8") as log_file_handle:
        for line in log_file_handle:
            line = line.strip()

            if not line:
                continue

            summary["total_lines"] += 1

            level_match = LOG_LEVEL_PATTERN.search(line)

            if level_match:
                level = level_match.group(1)

                if level == "INFO":
                    summary["info_count"] += 1

                elif level == "WARNING":
                    summary["warning_count"] += 1
                    summary["warning_messages"].append(line)

                elif level == "ERROR":
                    summary["error_count"] += 1
                    summary["error_messages"].append(line)

            if "MONITOR PASS" in line:
                summary["monitor_pass_count"] += 1

            if "MONITOR SLOW" in line:
                summary["monitor_slow_count"] += 1

            if "MONITOR FAIL" in line:
                summary["monitor_fail_count"] += 1

            if "MONITOR ERROR" in line:
                summary["monitor_error_count"] += 1

            if "DB MONITOR PASS" in line:
                summary["db_pass_count"] += 1

            if "DB MONITOR SLOW" in line:
                summary["db_slow_count"] += 1

            if "DB MONITOR ERROR" in line:
                summary["db_error_count"] += 1

            api_match = API_REQUEST_PATTERN.search(line)

            if api_match:
                method = api_match.group(1)
                endpoint = api_match.group(2)
                status_code = int(api_match.group(3))
                response_time = float(api_match.group(4))

                request_data = {
                    "method": method,
                    "endpoint": endpoint,
                    "status_code": status_code,
                    "response_time": response_time,
                }

                summary["api_requests"].append(request_data)

                if response_time >= API_RESPONSE_TIME_THRESHOLD:
                    summary["slow_api_requests"].append(request_data)

    return summary


def print_log_summary(summary):
    print("=" * 60)
    print("APPLICATION LOG ANALYSIS")
    print("=" * 60)

    print(f"Total log lines       : {summary['total_lines']}")
    print(f"INFO messages         : {summary['info_count']}")
    print(f"WARNING messages      : {summary['warning_count']}")
    print(f"ERROR messages        : {summary['error_count']}")
    print("\nWARNING DETAILS")
    print("-" * 60)
    if summary["warning_messages"]:
        for warning in summary["warning_messages"]:
            print(warning)
    else:
        print("No warnings detected.")

    print("\nERROR DETAILS")
    print("-" * 60)

    if summary["error_messages"]:
        for error in summary["error_messages"]:
            print(error)
    else:
        print("No errors detected.")

    print("\nAPI MONITORING")
    print("-" * 60)

    print(f"Monitor PASS          : {summary['monitor_pass_count']}")
    print(f"Monitor SLOW          : {summary['monitor_slow_count']}")
    print(f"Monitor FAIL          : {summary['monitor_fail_count']}")
    print(f"Monitor ERROR         : {summary['monitor_error_count']}")

    print("\nDATABASE MONITORING")
    print("-" * 60)

    print(f"DB Monitor PASS       : {summary['db_pass_count']}")
    print(f"DB Monitor SLOW       : {summary['db_slow_count']}")
    print(f"DB Monitor ERROR      : {summary['db_error_count']}")

    print("\nAPI REQUESTS")
    print("-" * 60)

    for request in summary["api_requests"]:
        print(
            f"{request['method']:<6} "
            f"{request['endpoint']:<30} "
            f"HTTP={request['status_code']} "
            f"time={request['response_time']:.4f}s"
        )

    print("\nSLOW API REQUESTS")
    print("-" * 60)

    if summary["slow_api_requests"]:
        for request in summary["slow_api_requests"]:
            print(
                f"{request['method']:<6} "
                f"{request['endpoint']:<30} "
                f"time={request['response_time']:.4f}s"
            )
    else:
        print("No slow API requests detected.")

    print("=" * 60)


if __name__ == "__main__":
    log_summary = analyze_log_file()
    print_log_summary(log_summary)