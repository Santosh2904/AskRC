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

def check_bias_in_user_question(question):
    """
    Checks for biased or inappropriate language in the user's question.
    Uses sentiment analysis and opinion lexicon to identify bias.
    Returns a suggestion to rephrase if bias is detected.
    """
    # Define gendered and negative opinion words
    gendered_terms = ["he", "she", "him", "her", "his", "hers"]
    biased_terms = set(opinion_lexicon.negative())

    # Check for gendered language
    if any(term in question.lower().split() for term in gendered_terms):
        return None, "We detected some language that might impact the quality of the response. Please consider rephrasing."

    # Check for specific biased terms like "lazy" in a negative context
    sentiment_score = sia.polarity_scores(question)
    if "lazy" in question.lower() or (any(word in question.lower() for word in biased_terms) and sentiment_score["neg"] > 0.5):
        return None, "We detected some language that might impact the quality of the response. Please consider rephrasing."

    # Return the question if no bias is detected
    return question, None