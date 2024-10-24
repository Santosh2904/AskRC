import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to get all links from a URL up to a certain depth
def get_all_links(url, visited=None, depth=0, max_depth=10):
    if visited is None:
        visited = set()

    if depth > max_depth:
        return set()  # Stop recursion if max depth is reached

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        links = set()
        for a_tag in soup.find_all("a", href=True):
            absolute_url = urljoin(url, a_tag['href'])
            if absolute_url not in visited:
                links.add(absolute_url)
                visited.add(absolute_url)
        
        # Recursively visit each new link, increasing the depth
        for link in list(links):
            if link.startswith(url):  # Scrape only links that start with the base URL
                links.update(get_all_links(link, visited, depth + 1, max_depth))
        
        return links

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

# Function to fetch links for all sections and print the number of links for each section
def fetch_and_print_links(section_urls):
    fetched_links = {}

        
    for section, urls in section_urls.items():
        fetched_links[section] = []  # Initialize an empty list for each section
        for url in urls:
            # Call the get_all_links function to fetch the links from each URL
            all_links = get_all_links(url)
            # Append the fetched links to the corresponding section in the new dictionary
            fetched_links[section].extend(all_links)

    # Print the fetched links
    for i in range(0, 12):  # Loop from 1 to 11 (inclusive)
        section_name = f'section-{i}'
        print(f"{section_name} has {len(fetched_links[section_name])} links")
    
    return fetched_links
# Example usage

