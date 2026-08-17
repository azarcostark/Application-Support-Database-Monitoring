import os

from utils.logger import get_logger


def test_logger_writes_to_file():
    logger = get_logger("test_logger")

    test_message = "Logger test message"

    logger.info(test_message)

    assert os.path.exists("logs/application.log")

    with open("logs/application.log", "r", encoding="utf-8") as log_file:
        log_content = log_file.read()

    assert test_message in log_content