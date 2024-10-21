from Get_all_url import get_all_links

documentation_url = "https://rc-docs.northeastern.edu/en/latest/index.html"

links = get_all_links(documentation_url)
print(f"Fetched {len(links)} links")