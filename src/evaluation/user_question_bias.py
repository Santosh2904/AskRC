import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def check_bias_in_user_question(question):
    """
    Checks for bias in the user's question using OpenAI's moderation API.
    Returns a sanitized version if no bias is detected or a message suggesting rephrasing.
    """
    response = openai.Moderation.create(input=question)
    flagged = response["results"][0]["flagged"]

    if flagged:
        return None, "We detected some language that might impact the quality of the response. Please consider rephrasing."
    
    return question, None

