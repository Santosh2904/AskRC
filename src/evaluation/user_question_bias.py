# import openai
# import os
# import re
# import nltk
# import spacy
# from nltk.sentiment import SentimentIntensityAnalyzer
# from nltk.corpus import opinion_lexicon
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Download required NLTK resources if not already available
# try:
#     nltk.data.find('sentiment/vader_lexicon.zip')
# except LookupError:
#     nltk.download('vader_lexicon')

# try:
#     nltk.data.find('corpora/opinion_lexicon')
# except LookupError:
#     nltk.download('opinion_lexicon')

# # Initialize sentiment analyzer
# sia = SentimentIntensityAnalyzer()

# # Mapping of gendered terms to neutral terms
# gender_neutral_map = {
#     "he": "they",
#     "she": "they",
#     "him": "them",
#     "her": "them",
#     "his": "their",
#     "hers": "theirs",
# }

# import re
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer

# # Initialize sentiment analyzer
# sia = SentimentIntensityAnalyzer()

# # Mapping of gendered terms to neutral terms
# gender_neutral_map = {
#     "he": "they",
#     "she": "they",
#     "him": "them",
#     "her": "them",
#     "his": "their",
#     "hers": "theirs",
# }

# def check_bias_in_user_question(question):
#     """
#     Checks for inappropriate or biased language in the user's question.
#     Replaces gendered terms with neutral terms and flags strongly negative language.
#     """
#     # Replace gendered terms with neutral equivalents
#     modified_question = question
#     for gendered_term, neutral_term in gender_neutral_map.items():
#         modified_question = re.sub(rf"\b{re.escape(gendered_term)}\b", neutral_term, modified_question, flags=re.IGNORECASE)

#     # Tokenize question to evaluate each word's sentiment for strongly negative language
#     words = nltk.word_tokenize(modified_question.lower())
#     for word in words:
#         # Perform sentiment analysis; flag if negativity is very high
#         sentiment_score = sia.polarity_scores(word)
#         if sentiment_score["neg"] > 0.95:
#             return None, "We detected some language that might impact the quality of the response. Please consider rephrasing."

#     # Return the modified question if no bias is detected
#     return modified_question, None

import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

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
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/opinion_lexicon')
except LookupError:
    nltk.download('opinion_lexicon')


# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()



# Mapping of gendered terms to neutral terms
gender_neutral_map = {
    "he": "they",
    "she": "they",
    "him": "them",
    "her": "their",
    "his": "their",
    "hers": "theirs",
}

# Set of common technical terms that should not be flagged for negativity
technical_terms = {"error", "failed", "issue", "setup", "connection", "installation", "SSH", "passwordless"}

def check_bias_in_user_question(question):
    """
    Checks for inappropriate or biased language in the user's question.
    Replaces gendered terms with neutral terms and flags strongly negative language, ignoring standard technical terms.
    """
    # Replace gendered terms with neutral equivalents
    modified_question = question
    for gendered_term, neutral_term in gender_neutral_map.items():
        modified_question = re.sub(rf"\b{re.escape(gendered_term)}\b", neutral_term, modified_question, flags=re.IGNORECASE)

    # Tokenize question to evaluate each word's sentiment for strongly negative language
    words = nltk.word_tokenize(modified_question.lower())
    for word in words:
        # Skip technical terms in the sentiment check
        if word in technical_terms:
            continue
        # Perform sentiment analysis; flag if negativity is very high
        sentiment_score = sia.polarity_scores(word)
        if sentiment_score["neg"] > 0.95:
            # Return a rephrase suggestion if inappropriate content is detected
            return None, "We detected some language that might impact the quality of the response. Please consider rephrasing."

    # Return the modified question if no bias is detected
    return modified_question, None
