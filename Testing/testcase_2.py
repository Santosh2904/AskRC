import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Mock Azure modules
sys.modules['azure.identity'] = MagicMock()
sys.modules['azure.storage.blob'] = MagicMock()
sys.modules['azure.search.documents'] = MagicMock()

# Import after mocking
from src.data_pipeline.preprocess import clean_text, split_content

@pytest.fixture(autouse=True)
def mock_azure_credentials():
    """Mock Azure credentials for testing"""
    with patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'mock-client-id',
        'AZURE_CLIENT_SECRET': 'mock-client-secret',
        'AZURE_TENANT_ID': 'mock-tenant-id',
        'AZURE_BLOB_STORAGE_URL': 'https://mock.blob.core.windows.net',
        'AZURE_BLOB_KEY': 'mock-key',
        'AZURE_SEARCH_ENDPOINT': 'https://mock.search.windows.net',
        'AZURE_SEARCH_KEY': 'mock-search-key'
    }):
        yield

def test_clean_text():
    raw_data = "<p>Hello, World! 123</p>"
    clean_text_result = clean_text(raw_data)
    expected_result = "hello world"
    assert clean_text_result == expected_result

def test_split_content():
    long_text = "word " * 10000
    parts = split_content(long_text)
    assert len(parts) > 1
    assert all(len(part.encode('utf-8')) <= 20000 for part in parts)

def test_clean_text_edge_cases():
    assert clean_text("") == ""
    assert clean_text(None) == ""