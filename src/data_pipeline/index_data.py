import os
import json
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Azure configuration
AZURE_BLOB_URL = os.getenv("AZURE_BLOB_STORAGE_URL")
AZURE_BLOB_KEY = os.getenv("AZURE_BLOB_KEY")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_CONTAINER_NAME = "preprocessed-data"
AZURE_INDEX_NAME = "askrcindex"

def index_data_in_search(container_name=AZURE_CONTAINER_NAME, index_name=AZURE_INDEX_NAME):
    """
    Index data from Azure Blob Storage into Azure Cognitive Search.
    
    Args:
        container_name (str): Name of the Azure Blob container
        index_name (str): Name of the Azure Search index
        
    Raises:
        ValueError: If required environment variables are not set
        Exception: For various Azure operations failures
    """
    # Validate environment variables
    if not all([AZURE_BLOB_URL, AZURE_BLOB_KEY, AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY]):
        raise ValueError("Required Azure environment variables are not set")

    try:
        # Initialize Blob and Search Clients
        blob_service_client = BlobServiceClient(
            account_url=AZURE_BLOB_URL,
            credential=AZURE_BLOB_KEY
        )
        container_client = blob_service_client.get_container_client(container_name)
        
        search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=index_name,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY),
            api_version="2021-04-30-Preview"
        )

        # Loop through blobs in the specified container
        for blob in container_client.list_blobs():
            try:
                blob_client = container_client.get_blob_client(blob)

                # Download blob content and check if it's empty
                blob_content = blob_client.download_blob().readall()
                json_data = blob_content.decode("utf-8").strip()
                
                if not json_data:
                    print(f"Warning: Blob {blob.name} is empty and will be skipped.")
                    continue  # Skip this blob if it's empty

                # Load JSON document from blob content
                document = json.loads(json_data)
                
                # Validate document structure
                if not isinstance(document, dict) or 'id' not in document:
                    print(f"Warning: Blob {blob.name} has invalid document structure. Skipping.")
                    continue

                # Check for large content fields
                content_size = len(document.get("content", "").encode('utf-8'))
                if content_size > 32766:  # Azure Search term size limit
                    print(f"Warning: Document ID {document['id']} has a content field exceeding "
                          f"the max term size ({content_size} bytes). Consider splitting it.")
                    continue  # Skip this document if it's too large
                
                # Index the document
                response = search_client.upload_documents(documents=[document])

                # Log indexing results
                for result in response:
                    if result.succeeded:
                        print(f"Successfully indexed document ID {result.key}")
                    else:
                        print(f"Failed to index document ID {result.key}: {result.error_message}")

            except json.JSONDecodeError as e:
                print(f"JSONDecodeError for blob {blob.name}: {str(e)}")
                continue
            except Exception as e:
                print(f"Error processing blob {blob.name}: {str(e)}")
                continue

    except Exception as e:
        error_message = f"Fatal error in index_data_in_search: {str(e)}"
        print(error_message)
        raise Exception(error_message)

    return True  # Return True if execution completes successfully

if __name__ == "__main__":
    index_data_in_search()