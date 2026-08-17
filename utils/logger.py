import logging
import os


LOG_DIRECTORY = "logs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "application.log")


def get_logger(name="application"):
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger