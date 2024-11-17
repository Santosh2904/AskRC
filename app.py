import os
import time
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from dotenv import load_dotenv
import nltk

# Azure Search Imports
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Custom Module Imports
from src.model.retrive_azure_index import search_azure_index
from src.model.system_prompt import create_system_prompt
from src.model.get_model_response import get_openai_response
from src.evaluation.user_question_bias import check_bias_in_user_question
from src.evaluation.model_response_bias import check_bias_in_model_response
from src.evaluation.answer_validation import key_concept_match 
from src.model.alerts import send_slack_alert
from mlflow.config import MLFLOW_TRACKING_URI, SLACK_WEBHOOK_URL

# Initialize environment variables
load_dotenv()

# Download NLTK data
nltk.download('punkt')  # Tokenizer
nltk.download('punkt_tab')  # Additional tokenizer (if needed)

# Retrieve Slack Webhook URL from environment variables
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    raise ValueError("SLACK_WEBHOOK_URL is not set in the environment.")

# Email alert function
def send_email_alert(subject, body):
    """
    Sends an email alert using SMTP.
    """
    # Environment variables for email configuration
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_emails = os.getenv("EMAIL_TO").split(',')
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))

    # Compose the email
    msg = MIMEText(body, 'plain')
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject

    try:
        # Connect to SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) if smtp_port == 465 else smtplib.SMTP(smtp_server, smtp_port) as server:
            if smtp_port == 587:
                server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
            print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email alert: {e}")

def main():
    """
    Main function to run the AskRC Streamlit application.
    """
    st.set_page_config(page_title="AskRC", page_icon="🎓")
    st.header("AskRC 🎓")

    # User input: Ask a question
    user_question = st.text_input("Ask a Question")

    if st.button("Get Answer"):
        with st.spinner("Processing..."):
            # Step 1: Check for bias in the user question
            user_question_clean, bias_message = check_bias_in_user_question(user_question)
            
            if bias_message:
                # Notify user about bias and send an email alert
                st.warning(bias_message)
                send_email_alert(
                    "Bias detected in user question",
                    f"The user question contains bias: {user_question_clean}. Bias message: {bias_message}"
                )
            else:
                # Step 2: Retrieve context from Azure Search
                context = search_azure_index(user_question_clean)
                
                # Step 3: Create the system prompt
                system_prompt = create_system_prompt(context, user_question_clean)
                
                # Step 4: Get response from OpenAI API
                answer = get_openai_response(system_prompt)
                
                # Step 5: Check for bias in the model response
                answer_clean, response_bias_message = check_bias_in_model_response(answer)
                
                # Step 6: Validate answer relevance using key concept match
                if key_concept_match(answer_clean, context):
                    # Display the final answer
                    st.write(answer_clean)

                    if response_bias_message:
                        # Notify about bias in the model response and send a Slack alert
                        st.warning(response_bias_message)
                        send_slack_alert(
                            "Bias detected in model response",
                            f"Bias message in the model response: {response_bias_message}"
                        )
                    else:
                        st.success("Answer provided.")
                else:
                    # Notify about insufficient contextual relevance and send a Slack alert
                    st.warning("The answer lacks sufficient contextual relevance.")
                    send_slack_alert(
                        "Answer lacks context",
                        f"The answer provided lacks sufficient contextual relevance: {answer_clean}"
                    )

# Entry point
if __name__ == "__main__":
    main()