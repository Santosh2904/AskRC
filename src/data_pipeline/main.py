"""
main.py

This script orchestrates the entire scraping process. It determines which sections to scrape 
based on the current week and runs the scraping for all sections up to and including the current week.
"""

from .scraper import scrape_sections_up_to_current_week

def main():
    """
    Main function to initiate the scraping process.

    This function triggers the scraping of sections up to the current week, calling the 
    `scrape_sections_up_to_current_week()` function from the scraper module.
    """
    scraped_sections = scrape_sections_up_to_current_week()  # Scrape sections based on the current week
    print(f"Scraped sections: {scraped_sections}")

if __name__ == '__main__':
    main()
