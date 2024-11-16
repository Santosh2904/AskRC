import requests

# Slack webhook URL
slack_webhook_url = "https://hooks.slack.com/services/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"

def send_test_slack_message():
    payload = {
        "text": "Test message from your application! 🎉"
    }
    response = requests.post(slack_webhook_url, json=payload)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")

# Send test message
send_test_slack_message()