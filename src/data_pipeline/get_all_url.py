"""
get_all_url.py

This module handles fetching all links from the URLs of the sections provided.
It recursively visits links on each page, up to a specified depth, to gather all relevant URLs.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(url, visited=None, depth=0, max_depth=10):
    """
    Recursively fetch all links from a given URL up to a certain depth.

    Args:
        url (str): The base URL to scrape for links.
        visited (set): A set of already visited URLs to avoid duplication.
        depth (int): The current depth of recursion.
        max_depth (int): The maximum depth of recursion.

    Returns:
        set: A set of URLs found on the page and its sub-pages up to the specified depth.
    """
    print("running get_all_links") 
    if visited is None:
        visited = set()

    if depth > max_depth:
        return set()  # Stop recursion if max depth is reached

    try:
        response = requests.get(url)  # Fetch the content of the URL
        soup = BeautifulSoup(response.content, "html.parser")
        
        links = set()
        for a_tag in soup.find_all("a", href=True):
            absolute_url = urljoin(url, a_tag['href'])  # Convert relative URLs to absolute
            if absolute_url not in visited:
                links.add(absolute_url)
                visited.add(absolute_url)
        
        # Recursively visit each new link, increasing the depth
        for link in list(links):
            if link.startswith(url):  # Only follow links that start with the base URL
                links.update(get_all_links(link, visited, depth + 1, max_depth))
        
        return links

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

def fetch_and_print_links(section_urls):
    """
    Fetch and print links for each section.

    This function takes the section URLs, fetches the links for each, and prints 
    how many links were found for each section.

    Args:
        section_urls (dict): A dictionary containing section names and their URLs.

    Returns:
        dict: A dictionary of sections and their corresponding fetched links.
    """
    fetched_links = {}

    for section, urls in section_urls.items():
        fetched_links[section] = []
        for url in urls:
            # Fetch all links for the section
            all_links = get_all_links(url)
            fetched_links[section].extend(all_links)

    # Print the number of links found for each section
    for section, links in fetched_links.items():
        print(f"{section} has {len(links)} links")
    
    return fetched_links