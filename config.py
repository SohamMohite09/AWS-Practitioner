import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "travelgo-secret-key-practitioner-2026")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    # AWS Configuration
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    DYNAMODB_USERS_TABLE = os.environ.get("DYNAMODB_USERS_TABLE", "travelgo-users")
    DYNAMODB_BOOKINGS_TABLE = os.environ.get("DYNAMODB_BOOKINGS_TABLE", "travelgo-bookings")
    SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")

    # Local Mock Mode flag:
    # If True, or if AWS credentials / tables are unavailable,
    # the application uses local JSON persistence so development and testing can proceed offline.
    USE_LOCAL_MOCK_DB = os.environ.get("USE_LOCAL_MOCK_DB", "auto").lower()
