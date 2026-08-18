import time

from config.database import get_database_connection
from config.settings import DB_RESPONSE_TIME_THRESHOLD
from utils.logger import get_logger


DB_RESPONSE_TIME_THRESHOLD = 1.0

logger = get_logger("db_monitor")


def check_database():
    connection = None
    cursor = None

    start_time = time.perf_counter()

    try:
        connection = get_database_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT 1")

        result = cursor.fetchone()

        response_time = time.perf_counter() - start_time

        query_ok = result is not None and result[0] == 1
        response_time_ok = response_time < DB_RESPONSE_TIME_THRESHOLD

        if query_ok and response_time_ok:
            logger.info(
                "DB MONITOR PASS | query=SELECT 1 | response_time=%.4fs",
                response_time,
            )

        elif query_ok and not response_time_ok:
            logger.warning(
                "DB MONITOR SLOW | query=SELECT 1 | response_time=%.4fs | threshold=%.2fs",
                response_time,
                DB_RESPONSE_TIME_THRESHOLD,
            )

        else:
            logger.error(
                "DB MONITOR FAIL | query=SELECT 1 | response_time=%.4fs",
                response_time,
            )

        return {
            "status": "UP" if query_ok else "DOWN",
            "response_time": response_time,
            "query_ok": query_ok,
            "response_time_ok": response_time_ok,
        }

    except Exception as error:
        response_time = time.perf_counter() - start_time

        logger.error(
            "DB MONITOR ERROR | response_time=%.4fs | error=%s",
            response_time,
            error,
        )

        return {
            "status": "DOWN",
            "response_time": response_time,
            "query_ok": False,
            "response_time_ok": False,
            "error": str(error),
        }

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    result = check_database()
    print(result)