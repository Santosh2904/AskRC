import os
from Scrape import scrape_and_save
from Get_all_url import get_all_links

# Base directory where all scraped data will be stored
base_dir = 'ScrapedData'

# Define a function to arrange and scrape the data
def arrange_scraped_data(fetched_links):
    for i in range(1, 12):
        section_name = f'section-{i}'
        links = fetched_links[section_name]  # Get the list of links for the current section
        
        # Define the directory path for each section
        dir_path = f"{base_dir}/section-{i}"
        file_path = f"{dir_path}/section-{i}_scraped_content.txt"  # Define the file path
        
        # Ensure the directory exists, creating it if necessary
        os.makedirs(dir_path, exist_ok=True)
        
        try:
            # Pass the links and the file path to the scrape_and_save function
            scrape_and_save(links, file_path)
        except Exception as e:
            print(f"An error occurred while saving to {file_path}: {e}")

# Example usage of the function
# fetched_links should be obtained by running your get_all_links logic first
# fetched_links = {...}

# arrange_scraped_data(fetched_links)
