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

def preprocess_text_file(input_file_path, output_folder):
    """
    Preprocess the raw text file, split if necessary, and save cleaned text as JSON files.
    """
    try:
        # Read the raw text data
        with open(input_file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
        
        # Clean the text
        cleaned_text = clean_text(raw_text)
        
        # Split content if it exceeds MAX_TERM_SIZE
        if len(cleaned_text.encode('utf-8')) > MAX_TERM_SIZE:
            print(f"Warning: Content in {input_file_path} exceeds max term size. Splitting content.")
            parts = split_content(cleaned_text)
        else:
            parts = [cleaned_text]  # No splitting needed
 
        # Save each part as a separate JSON document
        base_id = str(uuid.uuid4())
        for i, part in enumerate(parts):
            document = {
                "id": f"{base_id}_{i}",  # Unique ID for each split part
                "content": part
            }
            output_file_path = os.path.join(output_folder, f"{base_id}_{i}.json")
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                json.dump(document, file, ensure_ascii=False, indent=4)
            print(f"Processed text saved to {output_file_path}")
 
    except Exception as e:
        print(f"Error during preprocessing file {input_file_path}: {str(e)}")
 
def getFileName(file_path):
    file_name = getFileNameWithoutExtension(file_path)
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return file_name + "_" + time_str + ".json"
 
def getFileNameWithoutExtension(file_path):
    filename = os.path.basename(file_path)
    return os.path.splitext(filename)[0]
 
def preprocess_data(input_folder, output_folder):
    """
    Process all text files from the input folder and store the cleaned, split files in the output folder.
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".txt"):  # Assuming raw files are .txt
                raw_file_path = os.path.join(root, file)
                
                # Generate corresponding path in the processed folder
                processed_file_path = raw_file_path.replace(input_folder, output_folder)
                processed_file_path = processed_file_path.replace('scraped_content', 'processed_content')
                processed_file_path = processed_file_path.replace('.txt', '.json')  # Change file extension to .json
                
                preprocess_text_file(raw_file_path, output_folder)
 
 