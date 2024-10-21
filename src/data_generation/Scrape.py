import requests
from bs4 import BeautifulSoup

def scrape_and_save(urls, output_file="scraped_content.txt"):

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for url in urls:
                print(f"Scraping content from: {url}")
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Check if request was successful
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_text = soup.get_text(separator="\n", strip=True)
                    
                    if page_text:
                        # Write URL as a header for clarity
                        f.write(f"URL: {url}\n\n")
                        f.write(page_text + "\n\n")
                        f.write("="*80 + "\n\n")  # Separator between pages
                    else:
                        f.write(f"No content found at: {url}\n\n")
                        f.write("="*80 + "\n\n")
                
                except requests.exceptions.RequestException as e:
                    print(f"Failed to retrieve {url}: {e}")
                    f.write(f"Failed to retrieve content from: {url}\n\n")
                    f.write("="*80 + "\n\n")

        print(f"Scraped content saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred while saving to {output_file}: {e}")


#scrape_and_save(urls, "scraped_content.txt")
