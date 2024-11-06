import os
import re
import json
import uuid
import nltk
from nltk.corpus import stopwords
from datetime import datetime

try:
    from .azure_uploader import upload_to_blob
except (ImportError, ValueError):
    # Mock upload_to_blob for testing
    def upload_to_blob(file_path, container_name):
        return f"mock_url_for_{file_path}"

# Download stopwords if not already done
nltk.download('stopwords', quiet=True)

# Define maximum term size (in bytes)
MAX_TERM_SIZE = 20000

def clean_text(text):
    """
    Clean and preprocess the text. Includes:
    - Lowercasing
    - Removing HTML tags
    - Removing special characters and numbers
    - Stopword removal
    """
    if text is None:
        return ""
    
    # Convert text to lowercase
    text = str(text).lower()
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    
    return text

def split_content(content):
    """Split content into chunks that meet the max term size requirement."""
    parts = []
    words = content.split()
    current_part = []
    current_size = 0

    for word in words:
        # Add space character size if this isn't the first word in part
        space_size = 1 if current_part else 0
        word_size = len(word.encode('utf-8')) + space_size

        # If adding this word would exceed the limit, start a new part
        if current_size + word_size > MAX_TERM_SIZE and current_part:
            parts.append(" ".join(current_part))
            current_part = []
            current_size = 0

        # Handle words that are longer than MAX_TERM_SIZE
        if word_size > MAX_TERM_SIZE:
            if current_part:
                parts.append(" ".join(current_part))
                current_part = []
                current_size = 0
            # Split the long word
            while word:
                chunk = word[:MAX_TERM_SIZE//2]  # Take half of MAX_TERM_SIZE to be safe
                parts.append(chunk)
                word = word[MAX_TERM_SIZE//2:]
        else:
            current_part.append(word)
            current_size += word_size

    # Add the last part if there is one
    if current_part:
        parts.append(" ".join(current_part))

    return parts
