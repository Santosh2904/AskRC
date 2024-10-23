from Get_all_url import fetch_and_print_links
from arrange import arrange_scraped_data
#from Scrape import scrape_and_save
documentation_url = "https://rc-docs.northeastern.edu/en/latest/index.html"




#links = get_all_links(documentation_url)
#print(f"Fetched {len(links)} links")
#print(links)
#scrape_and_save(links, "./scraped_content.txt")

section_urls = {
    'section-1': ["https://rc-docs.northeastern.edu/en/latest/connectingtocluster/index.html#"],
    'section-2': ["https://rc-docs.northeastern.edu/en/latest/runningjobs/index.html"],
    'section-3': ["https://rc-docs.northeastern.edu/en/latest/gpus/index.html"],
    'section-4': ["https://rc-docs.northeastern.edu/en/latest/datamanagement/index.html"],
    'section-5': ["https://rc-docs.northeastern.edu/en/latest/software/index.html"],
    'section-6': ["https://rc-docs.northeastern.edu/en/latest/slurmguide/index.html"],
    'section-7': ["https://rc-docs.northeastern.edu/en/latest/classroom/index.html"],
    'section-8': ["https://rc-docs.northeastern.edu/en/latest/containers/index.html"],
    'section-9': ["https://rc-docs.northeastern.edu/en/latest/best-practices/index.html"],
    'section-10': ["https://rc-docs.northeastern.edu/en/latest/glossary.html"],
    'section-11': ["https://rc-docs.northeastern.edu/en/latest/faqs-new.html"]
}

# Fetch and print links for all sections
fetched_links=fetch_and_print_links(section_urls)
arrange_scraped_data(fetched_links)