import openai
import os
import re
import nltk
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

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
    
    # Flag the response if the negative sentiment is exceptionally high (>0.95)
    if sentiment_score["neg"] > 0.95:
        return None, "The response was flagged for high negative sentiment, which may impact the quality of the information provided."

    # Return the modified response if no strong negativity is detected
    return modified_response, None


# explicit_inappropriate_terms = {
#     "idiot", "stupid", "dumb", "lazy", "useless", "incompetent", "moron",
#     "ignorant", "annoying", "worthless", "terrible", "hopeless",
#     "nonsense", "pathetic", "disgusting", "foolish", "horrible", "rubbish",
#     "awful", "offensive", "waste", "ridiculous"
# }

# def check_bias_in_model_response(response, context):
#     """
#     Checks for biased or inappropriate language in the model's response.
#     Uses context as a whitelist for terms not to redact.
#     Replaces gendered terms with neutral terms and redacts explicitly inappropriate words.
#     """
#     # Tokenize context into a set of unique words (whitelist)
#     documentation_terms = set(nltk.word_tokenize(context.lower()))
    
#     redacted_response = response
#     redaction_occurred = False

#     # Replace gendered terms with neutral equivalents
#     for gendered_term, neutral_term in gender_neutral_map.items():
#         redacted_response = re.sub(rf"\b{re.escape(gendered_term)}\b", neutral_term, redacted_response, flags=re.IGNORECASE)

#     # Perform NER to skip redaction for entities likely to be technical terms
#     doc = nlp(response)
#     entities = {ent.text.lower() for ent in doc.ents}

#     # Tokenize response to check each word against documentation context
#     words = nltk.word_tokenize(response.lower())
#     for word in words:
#         # Skip redaction for terms found in context or recognized entities
#         if word in documentation_terms or word in entities:
#             continue

#         # Apply sentiment analysis only to words outside the context with high negativity
#         sentiment_score = sia.polarity_scores(word)
#         if sentiment_score['neg'] > 0.95:  # Only redact words with very high negative sentiment
#             redacted_response = re.sub(rf"\b{re.escape(word)}\b", "[REDACTED]", redacted_response, flags=re.IGNORECASE)
#             redaction_occurred = True

#     # Set redaction message if changes were made
#     if redaction_occurred or redacted_response != response:
#         return redacted_response, "Certain parts of the response were redacted or adjusted for neutrality due to potentially inappropriate or biased content."

#     return response, None