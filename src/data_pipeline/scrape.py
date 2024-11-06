import requests
from bs4 import BeautifulSoup

def scrape_and_save(urls, output_file="scraped_content.txt"):
    """
    Scrape content from a list of URLs and save the content into a text file.
    
    Args:
        urls (list): List of URLs to scrape content from.
        output_file (str): File path where the scraped content will be saved.
        
    Returns:
        dict: Dictionary with URLs as keys and scraped content as values.
    """
    print("Running scrape & save")
    scraped_data = {}  # Dictionary to store scraped content
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for url in urls:
                print(f"Scraping content from: {url}")
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Check for successful response
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_text = soup.get_text(separator="\n", strip=True)  # Extract text from the page
                    
                    if page_text:
                        # Store the content in the dictionary
                        scraped_data[url] = page_text
                        
                        # Write the content to file for logging purposes
                        f.write(f"URL: {url}\n\n")
                        f.write(page_text + "\n\n")
                        f.write("="*80 + "\n\n")  # Separator between pages
                    else:
                        scraped_data[url] = "No content found"
                        f.write(f"No content found at: {url}\n\n")
                        f.write("="*80 + "\n\n")
                
                except requests.exceptions.RequestException as e:
                    print(f"Failed to retrieve {url}: {e}")
                    scraped_data[url] = f"Failed to retrieve content: {e}"
                    f.write(f"Failed to retrieve content from: {url}\n\n")
                    f.write("="*80 + "\n\n")

        print(f"Scraped content saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred while saving to {output_file}: {e}")
    
    return scraped_data  # Return the scraped data dictionary
