import openai
import os
import re
import nltk
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from config.mlflow_config import *
collector = MetricsCollector()
# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Download required NLTK resources if not already available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/opinion_lexicon')
except LookupError:
    nltk.download('opinion_lexicon')

# Initialize sentiment analyzer and spaCy NER
sia = SentimentIntensityAnalyzer()
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Mapping of gendered terms to neutral terms
gender_neutral_map = {
    "he": "they",
    "she": "they",
    "him": "them",
    "her": "them",
    "his": "their",
    "hers": "theirs",
}

import re
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Mapping of gendered terms to neutral terms
gender_neutral_map = {
    "he": "they",
    "she": "they",
    "him": "them",
    "her": "them",
    "his": "their",
    "hers": "theirs",
}

def check_bias_in_model_response(response):
    """
    Checks for inappropriate or biased language in the model's response.
    Replaces gendered terms with neutral terms and flags based on high negativity sentiment.
    """
    # Replace gendered terms with neutral equivalents
    modified_response = response
    for gendered_term, neutral_term in gender_neutral_map.items():
        modified_response = re.sub(rf"\b{re.escape(gendered_term)}\b", neutral_term, modified_response, flags=re.IGNORECASE)

    # Check sentiment score of the entire response
    sentiment_score = sia.polarity_scores(modified_response)
    #collector.add_metric('sentiment_score',sentiment_score)
    #collector.add_metric('sentiment_score_threshold',0.95)
    # Flag the response if the negative sentiment is exceptionally high (>0.95)
    if sentiment_score["neg"] > 0.95:
        return None, "The response was flagged for high negative sentiment, which may impact the quality of the information provided."

    # Return the modified response if no strong negativity is detected
    return modified_response, None
