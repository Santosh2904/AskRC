import openai
import os
import re
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def check_bias_in_model_response(response):
    """
    Checks for bias in the model's response using OpenAI's moderation API.
    Redacts flagged parts of the response if bias is detected.
    Returns the sanitized response and a message indicating that content was redacted, if applicable.
    """
    moderation_response = openai.Moderation.create(input=response)
    flagged_categories = moderation_response["results"][0]["categories"]
    flagged = moderation_response["results"][0]["flagged"]

    # If bias or inappropriate content is detected, redact the flagged parts
    if flagged:
        # Define the words/phrases associated with flagged categories to redact
        redacted_response = response
        for category, is_flagged in flagged_categories.items():
            if is_flagged:
                # Using regex to replace flagged words/phrases with "[REDACTED]"
                redacted_response = re.sub(r'\b{}\b'.format(re.escape(category)), "[REDACTED]", redacted_response, flags=re.IGNORECASE)
        
        # Inform the user that some content was redacted
        redaction_message = "Certain parts of the response were redacted due to potentially inappropriate or biased content."
        return redacted_response, redaction_message

    # If no bias is detected, return the original response with no redaction message
    return response, None
