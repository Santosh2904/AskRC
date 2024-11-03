"""
preprocess.py

This module handles the preprocessing of raw text data after scraping. The cleaned text data is saved
in the 'processed/' folder, maintaining the same structure as the 'raw/' folder.
"""

import os
import re
import nltk
from nltk.corpus import stopwords
from data_pipeline.azure_uploader import upload_to_blob
from datetime import datetime


# Download stopwords if not already done
nltk.download('stopwords')

def clean_text(text):
    """
    Clean and preprocess the text for RAG. Includes:
    - Lowercasing
    - Removing special characters and numbers
    - Tokenization
    - Stopword removal
    
    Args:
        text (str): The raw text data.
    
    Returns:
        str: The cleaned text ready for RAG.
    """
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'\W+', ' ', text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    
    return text

def preprocess_text_file(input_file_path, output_file_path):
    """
    Preprocess the raw text file and save the cleaned text in the processed directory.
    
    Args:
        input_file_path (str): The file path of the raw text data.
        output_file_path (str): The file path to save the cleaned text.
    """
    try:
        # Read the raw text data
        with open(input_file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
        
        # Clean the text
        cleaned_text = clean_text(raw_text)
        
        # Ensure the processed directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Write the cleaned text to the processed file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)
        
        print(f"Processed text saved to {output_file_path}")
        #print("Uploading to Azure blob storage")
        #upload_to_blob(output_file_path, file_name=getFileName(output_file_path))
        #print("Uploaded to azure")
    except Exception as e:
        print(f"Error during preprocessing file {input_file_path}: {str(e)}")


def getFileName(file_path):
    file_name = getFileNameWithoutExtension(file_path)
    # Get the current time in a format safe for filenames
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return file_name + "_" + time_str + ".txt"


def getFileNameWithoutExtension(file_path):
    filename = os.path.basename(file_path)
    return os.path.splitext(filename)[0]

def preprocess_data(input_folder, output_folder):
    """
    Process all text files from the input folder and store the cleaned files in the output folder.
    
    Args:
        input_folder (str): The directory containing raw text files (e.g., data/raw/).
        output_folder (str): The directory to save the cleaned text files (e.g., data/processed/).
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".txt"):  # Assuming raw files are .txt
                raw_file_path = os.path.join(root, file)
                
                # Generate corresponding path in the processed folder
                processed_file_path = raw_file_path.replace(input_folder, output_folder)
                processed_file_path = processed_file_path.replace('scraped_content', 'processed_content')
                
                preprocess_text_file(raw_file_path, processed_file_path)