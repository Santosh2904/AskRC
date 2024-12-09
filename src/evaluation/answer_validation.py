import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from config.mlflow_config import *
import sys
collector = MetricsCollector()

sys.path.append('/opt/airflow/src')
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
    collector.add_metric('answer_tokens_len',len(answer_tokens))
    collector.add_metric('context_tokens_len',len(context_tokens))
    
    # Identify key concepts in answer that should appear in context
    key_concepts = answer_tokens.intersection(context_tokens)
    # Define a threshold (number of matching key concepts required for sufficient context match)
    threshold = 7  # Adjust this value based on experimentation with the dataset
    collector.add_metric('key_concepts ',len(key_concepts))
    #print(('key_concepts ',key_concepts))
    collector.add_metric('key_concepts_threshold', threshold)
    return len(key_concepts) >= threshold
