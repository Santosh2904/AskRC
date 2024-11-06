import pytest
import random
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_pipeline.get_all_url import get_all_links 
from src.data_pipeline.scrape import scrape_and_save

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
    data = get_all_links(random_url)
    assert data is not None, "No data retrieved from URL"
    assert len(data) > 0, "Empty data retrieved from URL"

#test1

def test_data_format(random_url):
    data = scrape_and_save(urls)
    
    # Ensure data is a dictionary
    assert isinstance(data, dict), "Data format is not a dictionary"
    
    # Check that each URL in data has corresponding text content or an error message
    for url, content in data.items():
        assert isinstance(content, str), f"Content for URL {url} is not a string"
        assert len(content) > 0, f"No content retrieved for URL {url}"

@patch("src.data_generation.Get_all_url.requests.get")
def test_error_handling(mock_get):
    """Test to check error handling for network failures."""
    mock_get.side_effect = Exception("Network error")
    with pytest.raises(Exception, match="Network error"):
        get_all_links("https://rc-docs.northeastern.edu/en/latest/nonexistent-page.html")
