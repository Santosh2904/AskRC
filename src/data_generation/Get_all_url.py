import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(url, visited=None):
    if visited is None:
        visited = set()  
        
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        links = set()
        for a_tag in soup.find_all("a", href=True):
            absolute_url = urljoin(url, a_tag['href'])
            if absolute_url not in visited:
                links.add(absolute_url)
                visited.add(absolute_url)
        
        for link in list(links):  
            if link.startswith(url):  
                links.update(get_all_links(link, visited))
        return links
        print("returned links")

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        print(set)
        return set()


'''
documentation_url = "https://rc-docs.northeastern.edu/en/latest/index.html"  # Replace with your documentation webpage URL
all_links = get_all_links(documentation_url)
response = requests.get(documentation_url)
print(f"Total Links fetched = {len(all_links)}")
for link in all_links:
    print(link)
'''