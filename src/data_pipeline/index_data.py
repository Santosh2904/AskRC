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
    # Initialize Blob and Search Clients
    blob_service_client = BlobServiceClient(account_url=AZURE_BLOB_URL, credential=AZURE_BLOB_KEY)
    container_client = blob_service_client.get_container_client(container_name)
    
    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=index_name,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY),
        api_version="2021-04-30-Preview"
    )

    # Loop through blobs in the specified container
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)

        # Download blob content and check if it's empty
        json_data = blob_client.download_blob().readall().decode("utf-8").strip()
        if not json_data:
            print(f"Warning: Blob {blob.name} is empty and will be skipped.")
            continue  # Skip this blob if it's empty

        try:
            # Load JSON document from blob content
            document = json.loads(json_data)
            
            # Check for large content fields
            if len(document.get("content", "").encode('utf-8')) > 32766:
                print(f"Warning: Document ID {document['id']} has a content field exceeding the max term size. Consider splitting it.")
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
        except Exception as e:
            print(f"Error indexing document from blob {blob.name}: {str(e)}")

if __name__ == "__main__":
    index_data_in_search()
