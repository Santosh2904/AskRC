import openai
import os
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('corpora/opinion_lexicon')
except LookupError:
    nltk.download('opinion_lexicon')

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

def check_bias_in_model_response(response):
    """
    Checks for biased or inappropriate language in the model's response.
    Redacts flagged words if bias is detected.
    """
    # Define gendered terms and biased terms
    gendered_terms = ["he", "she", "him", "her", "his", "hers"]
    biased_terms = set(opinion_lexicon.negative())
    
    redacted_response = response  # Start with the original response

    # Redact gendered terms
    for term in gendered_terms:
        redacted_response = re.sub(rf"\b{re.escape(term)}\b", "[REDACTED]", redacted_response, flags=re.IGNORECASE)

    # Redact words with strong negative sentiment in the opinion lexicon
    words = response.split()
    for word in words:
        if word.lower() in biased_terms:
            sentiment_score = sia.polarity_scores(word)
            if sentiment_score["neg"] > 0.7:  # Higher threshold to avoid false positives
                redacted_response = re.sub(rf"\b{re.escape(word)}\b", "[REDACTED]", redacted_response, flags=re.IGNORECASE)

    # Only set redaction message if actual changes were made
    if redacted_response != response:
        return redacted_response, "Certain parts of the response were redacted due to potentially inappropriate or biased content."

    # If no redaction occurred, return the original response without a message
    return response, None