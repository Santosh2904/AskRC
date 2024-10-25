"""
arrange.py

This module is responsible for organizing scraped data into the appropriate folders.
It saves the scraped content from each section into its own directory and text file.
"""

import os
from .scrape import scrape_and_save

# Define the base directory where all scraped data will be stored
base_dir = '/opt/airflow/data/raw/'

def arrange_scraped_data(fetched_links):
    """
    Arrange the scraped data into directories and save the content into files.

    This function takes the fetched links for each section, creates a directory for each section 
    (if it doesn't already exist), and saves the scraped content into text files.

    Args:
        fetched_links (dict): A dictionary of sections and their corresponding fetched links.
    """
    print("Arranging scraped data...")  # Indicate the start of the arrangement process
    for section_name, links in fetched_links.items():
        # Define the directory path for each section
        dir_path = f"{base_dir}/{section_name}"
        file_path = f"{dir_path}/{section_name}_scraped_content.txt"
        
        # Ensure the directory exists; create it if it doesn't
        os.makedirs(dir_path, exist_ok=True)
        
        try:
            # Scrape and save the content for each section
            scrape_and_save(links, file_path)
        except Exception as e:
            print(f"An error occurred while saving to {file_path}: {e}")
