from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Retrieve environment variables
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    raise ValueError("SLACK_WEBHOOK_URL is not set in the environment.")