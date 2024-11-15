import requests
import os
from dotenv import load_dotenv

load_dotenv()
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(alert_type, message):
    payload = {
        "text": f"Alert Type: {alert_type}\nMessage: {message}"
    }
    # Send the payload to Slack using your webhook URL
    response = requests.post(slack_webhook_url, json=payload)

    if response.status_code != 200:
        print(f"Failed to send alert: {response.status_code}, {response.text}")
    else:
        print("Alert sent successfully")

# Example usage in your main function
def main():
    user_question = "Why is the sky blue?"
    # After processing the user question, if there's an issue:
    send_slack_alert("Answer lacks context", "The answer provided lacks sufficient contextual relevance.")

if __name__ == "__main__":
    main()
