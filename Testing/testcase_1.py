import pytest
import random
from unittest.mock import patch
from src.data_generation.Get_all_url import fetch_and_print_links
from src.data_generation.Scrape import scrape_and_save

# Using a pytest fixture to set up URLs and data for tests
@pytest.fixture
def urls():
    return {
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

@pytest.fixture
def random_url(urls):
    """Fixture to select a random URL from the given sections."""
    return random.choice(list(urls.values()))[0]

def test_data_retrieval(random_url):
    """Test to verify data retrieval from a random URL."""
    # Fetch and verify the data
    data = fetch_and_print_links(random_url)
    assert data is not None, "No data retrieved from URL"
    assert len(data) > 0, "Empty data retrieved from URL"

def test_data_format(random_url):
    """Test to verify data format from a scraped page."""
    # Ensure data retrieval and format check
    data = scrape_and_save(random_url)  # Adjust to your expected return type
    assert isinstance(data, dict), "Data format is not a dictionary"

@patch("src.data_generation.Get_all_url.requests.get")
def test_error_handling(mock_get):
    """Test to check error handling for network failures."""
    mock_get.side_effect = Exception("Network error")
    with pytest.raises(Exception, match="Network error"):
        fetch_and_print_links("https://rc-docs.northeastern.edu/en/latest/nonexistent-page.html")
