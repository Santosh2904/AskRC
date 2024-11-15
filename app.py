from email.mime.text import MIMEText
import os
import openai
import time
import streamlit as st
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from src.model.retrive_azure_index import search_azure_index
from src.model.system_prompt import create_system_prompt
from src.model.get_model_response import get_openai_response
from src.evaluation.user_question_bias import check_bias_in_user_question
from src.evaluation.model_response_bias import check_bias_in_model_response
from src.evaluation.answer_validation import key_concept_match 
from src.model.alerts import send_slack_alert
# Load environment variables from .env file
load_dotenv()

# Email alert function (you can integrate any email provider like SendGrid or use SMTP)
def send_email_alert(subject, body):
    sender_email = os.getenv("SENDER_EMAIL")  # Sender's email
    receiver_emails = os.getenv("EMAIL_TO").split(',')  # List of recipient emails
    app_password = os.getenv("EMAIL_APP_PASSWORD")  # App Password or regular password
    smtp_server = os.getenv("SMTP_SERVER")  # SMTP server from .env
    smtp_port = int(os.getenv("SMTP_PORT"))  # SMTP port from .env

    # Set up the MIME
    msg = MIMEText(body, 'plain')
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject

    try:
        # Connect to the SMTP server with the configured server and port
        with smtplib.SMTP_SSL(smtp_server, smtp_port) if smtp_port == 465 else smtplib.SMTP(smtp_server, smtp_port) as server:
            if smtp_port == 587:
                server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
            print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email alert: {e}")

def main():
    st.set_page_config(page_title="AskRC", page_icon="🎓")
    st.header("AskRC 🎓")

    user_question = st.text_input("Ask a Question")

    if st.button("Get Answer"):
        with st.spinner("Processing..."):
            # Step 1: Check for bias in the user question
            user_question_clean, bias_message = check_bias_in_user_question(user_question)
            
            if bias_message:
                # Display rephrase suggestion if bias is detected
                st.warning(bias_message)
                send_email_alert("Bias detected in user question", f"The user question contains bias: {user_question_clean}. Bias message: {bias_message}")
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
                    st.write(answer_clean)
                    if response_bias_message:
                        st.warning(response_bias_message)
                        send_slack_alert("Bias detected in model response", f"Bias message in the model response: {response_bias_message}")
                    else:
                        st.success("Answer provided.")
                else:
                    st.warning("The answer lacks sufficient contextual relevance.")
                    send_slack_alert("Answer lacks context", f"The answer provided lacks sufficient contextual relevance: {answer_clean}")

# Run the app
if __name__ == "__main__":
    main()
