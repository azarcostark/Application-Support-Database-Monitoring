import os

from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:5000",
)


API_RESPONSE_TIME_THRESHOLD = float(
    os.getenv(
        "API_RESPONSE_TIME_THRESHOLD",
        "1.0",
    )
)


DB_RESPONSE_TIME_THRESHOLD = float(
    os.getenv(
        "DB_RESPONSE_TIME_THRESHOLD",
        "1.0",
    )
)