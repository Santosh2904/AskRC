from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import mlflow

def key_concept_match(answer, context):
    """
    Validates that the key concepts in the answer are present in the context.
    Returns True if sufficient key concepts are found, False otherwise.
    """
    # Load stopwords once to optimize performance
    stop_words = set(stopwords.words("english"))

    # Tokenize and filter out stopwords for both answer and context
    answer_tokens = set(word_tokenize(answer.lower())) - stop_words
    context_tokens = set(word_tokenize(context.lower())) - stop_words

    # Identify key concepts in the answer that should appear in the context
    key_concepts = answer_tokens.intersection(context_tokens)

    # Define a threshold (number of matching key concepts required for sufficient context match)
    threshold = 7  # Adjust this value based on experimentation with the dataset

    # Determine if the answer is valid based on threshold
    is_valid = len(key_concepts) >= threshold

    # Log metrics and parameters with MLflow
    with mlflow.start_run(run_name="key_concept_validation"):
        mlflow.log_metric("threshold", threshold)
        mlflow.log_metric("key_concepts_length", len(key_concepts))
        mlflow.log_param("is_valid", is_valid)
        mlflow.log_param("key_concepts", ", ".join(key_concepts))  # Optional for debugging
    
    return is_valid