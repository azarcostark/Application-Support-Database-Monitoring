import os

from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:5000"
)

# API response-time threshold in seconds
API_RESPONSE_TIME_THRESHOLD = 1.0

# Database response-time threshold in seconds
DB_RESPONSE_TIME_THRESHOLD = 1.0