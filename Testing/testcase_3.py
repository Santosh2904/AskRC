import pytest
import json
import os
from unittest.mock import patch, MagicMock

# Mock environment variables before importing the module
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        'AZURE_BLOB_STORAGE_URL': 'https://test.blob.core.windows.net',
        'AZURE_BLOB_KEY': 'test-blob-key',
        'AZURE_SEARCH_ENDPOINT': 'https://test.search.windows.net',
        'AZURE_SEARCH_KEY': 'test-search-key'
    }):
        yield

@patch("src.data_pipeline.index_data.BlobServiceClient")
@patch("src.data_pipeline.index_data.SearchClient")
@patch("src.data_pipeline.index_data.AzureKeyCredential")
def test_index_data_in_search(mock_azure_key_credential, mock_search_client, mock_blob_service_client):
    """Test indexing data in Azure Search using mocked Azure clients."""
    from src.data_pipeline.index_data import index_data_in_search

    # Mock Azure Key Credential
    mock_azure_key_credential.return_value = MagicMock()

    # Mock blob and search client behavior
    mock_container_client = MagicMock()
    mock_blob_client = MagicMock()
    mock_search_client_instance = MagicMock()

    # Configure the BlobServiceClient mock
    mock_blob_service_client.return_value.get_container_client.return_value = mock_container_client
    mock_container_client.list_blobs.return_value = [MagicMock(name="test_blob.json")]
    mock_container_client.get_blob_client.return_value = mock_blob_client
    
    # Configure the blob client to return sample JSON data
    mock_download_blob = MagicMock()
    mock_download_blob.readall.return_value = json.dumps({
        "id": "test_id",
        "content": "This is a test document content"
    }).encode("utf-8")
    mock_blob_client.download_blob.return_value = mock_download_blob
    
    # Configure the SearchClient mock
    mock_search_client.return_value = mock_search_client_instance
    mock_search_client_instance.upload_documents.return_value = [
        MagicMock(succeeded=True, key="test_id")
    ]

    # Run the indexing function
    index_data_in_search()

    # Assertions to verify interactions
    mock_blob_service_client.assert_called_once()
    mock_container_client.list_blobs.assert_called_once()
    mock_blob_client.download_blob.assert_called_once()
    mock_search_client_instance.upload_documents.assert_called_once()

    # Assert the document upload succeeded
    upload_call_args = mock_search_client_instance.upload_documents.call_args[1]
    documents = upload_call_args['documents']
    assert documents[0]["id"] == "test_id", "Document ID did not match expected value"
    assert documents[0]["content"] == "This is a test document content", "Document content did not match expected value"

@patch("src.data_pipeline.index_data.BlobServiceClient")
@patch("src.data_pipeline.index_data.SearchClient")
@patch("src.data_pipeline.index_data.AzureKeyCredential")
def test_empty_blob_handling(mock_azure_key_credential, mock_search_client, mock_blob_service_client):
    """Test handling of empty blobs in Azure Blob Storage."""
    from src.data_pipeline.index_data import index_data_in_search

    # Mock Azure Key Credential
    mock_azure_key_credential.return_value = MagicMock()

    # Mock blob service and container client
    mock_container_client = MagicMock()
    mock_blob_client = MagicMock()
    
    # Configure the BlobServiceClient mock to simulate an empty blob
    mock_blob_service_client.return_value.get_container_client.return_value = mock_container_client
    mock_container_client.list_blobs.return_value = [MagicMock(name="empty_blob.json")]
    mock_container_client.get_blob_client.return_value = mock_blob_client
    
    # Configure empty blob response
    mock_download_blob = MagicMock()
    mock_download_blob.readall.return_value = b""
    mock_blob_client.download_blob.return_value = mock_download_blob

    # Configure the SearchClient mock
    mock_search_client_instance = MagicMock()
    mock_search_client.return_value = mock_search_client_instance

    # Run the indexing function
    index_data_in_search()

    # Verify empty blob was skipped
    mock_blob_client.download_blob.assert_called_once()
    mock_search_client_instance.upload_documents.assert_not_called()