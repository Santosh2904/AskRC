import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download

# Ensure necessary NLTK resources are available
download('punkt')
download('stopwords')

def key_concept_match(answer, context):
    """
    Validates that the key concepts in the answer are present in the context.
    Returns True if sufficient key concepts are found, False otherwise.
    """
    # Tokenize and filter out stopwords for both answer and context
    answer_tokens = set(word_tokenize(answer.lower())) - set(stopwords.words("english"))
    context_tokens = set(word_tokenize(context.lower())) - set(stopwords.words("english"))
    
    # Identify key concepts in answer that should appear in context
    key_concepts = answer_tokens.intersection(context_tokens)
    
    # Define a threshold (number of matching key concepts required for sufficient context match)
    threshold = 7  # Adjust this value based on experimentation with the dataset
    return len(key_concepts) >= threshold
