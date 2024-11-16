import requests
from config import SLACK_WEBHOOK_URL

import requests
load_dotenv()

# Download NLTK data
nltk.download('punkt')  # Tokenizer
nltk.download('punkt_tab')  # Additional tokenizer (if needed)

# Retrieve Slack Webhook URL from environment variables
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    raise ValueError("SLACK_WEBHOOK_URL is not set in the environment.")
def send_slack_alert(title, message, user_question=None):
    """
    Sends an alert to Slack using the configured webhook URL.

    Parameters:
    - title (str): Title of the alert.
    - message (str): Main content of the alert.
    - user_question (str): Optional user question to include in the alert.
    """
    if not slack_webhook_url:
        raise ValueError("Slack webhook URL is not configured properly.")

    # Build the Slack payload
    payload = {
        "text": f"*{title}*\n{message}"
    }

    if user_question:
        payload["text"] += f"\n\n*User Question:*\n>{user_question}"

    try:
        # Send the Slack alert
        response = requests.post(slack_webhook_url, json=payload)
        response.raise_for_status()
        print(f"Slack alert sent successfully: {title}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack alert: {e}")
        raise