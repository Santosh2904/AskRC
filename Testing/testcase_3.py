import pytest
import json  
from unittest.mock import patch, MagicMock
from src.data_pipeline.index_data import index_data_in_search

@patch("src.data_pipeline.index_data.BlobServiceClient")
@patch("src.data_pipeline.index_data.SearchClient")
def test_index_data_in_search(mock_search_client, mock_blob_service_client):
    """Test indexing data in Azure Search using mocked Azure clients."""

    # Mock blob and search client behavior
    mock_container_client = MagicMock()
    mock_blob_client = MagicMock()
    mock_search_client_instance = MagicMock()

    # Configure the BlobServiceClient mock
    mock_blob_service_client.return_value.get_container_client.return_value = mock_container_client
    mock_container_client.list_blobs.return_value = [{"name": "test_blob.json"}]
    mock_container_client.get_blob_client.return_value = mock_blob_client
    
    # Configure the blob client to return sample JSON data
    mock_blob_client.download_blob().readall.return_value = json.dumps({
        "id": "test_id",
        "content": "This is a test document content"
    }).encode("utf-8")
    
    # Configure the SearchClient mock
    mock_search_client.return_value = mock_search_client_instance
    mock_search_client_instance.upload_documents.return_value = [
        MagicMock(succeeded=True, key="test_id")
    ]

    # Run the indexing function
    index_data_in_search()

    # Assertions to verify interactions
    mock_blob_service_client.assert_called_once_with(account_url="AZURE_BLOB_URL", credential="AZURE_BLOB_KEY")
    mock_container_client.list_blobs.assert_called_once()
    mock_blob_client.download_blob().readall.assert_called_once()
    mock_search_client_instance.upload_documents.assert_called_once()

    # Assert the document upload succeeded
    results = mock_search_client_instance.upload_documents.call_args[0][0]
    assert results[0]["id"] == "test_id", "Document ID did not match expected value"
    assert results[0]["content"] == "This is a test document content", "Document content did not match expected value"

@patch("src.data_pipeline.index_data.BlobServiceClient")
@patch("src.data_pipeline.index_data.SearchClient")
def test_empty_blob_handling(mock_search_client, mock_blob_service_client):
    """Test handling of empty blobs in Azure Blob Storage."""

    # Mock blob service and container client
    mock_container_client = MagicMock()
    mock_blob_client = MagicMock()
    
    # Configure the BlobServiceClient mock to simulate an empty blob
    mock_blob_service_client.return_value.get_container_client.return_value = mock_container_client
    mock_container_client.list_blobs.return_value = [{"name": "empty_blob.json"}]
    mock_container_client.get_blob_client.return_value = mock_blob_client
    mock_blob_client.download_blob().readall.return_value = b""

    # Run the indexing function
    index_data_in_search()

    # Verify empty blob was skipped
    mock_blob_client.download_blob().readall.assert_called_once()
    mock_search_client.return_value.upload_documents.assert_not_called()  # Ensure no indexing attempted
