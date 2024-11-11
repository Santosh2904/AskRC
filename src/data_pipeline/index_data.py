import os
import json
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchFieldDataType, SimpleField,
    SearchIndexer, SearchIndexerDataSourceConnection
)
from azure.core.exceptions import ResourceExistsError, HttpResponseError, ResourceNotFoundError


# Azure configuration
AZURE_BLOB_URL = os.getenv("AZURE_BLOB_STORAGE_URL")
AZURE_BLOB_KEY = os.getenv("AZURE_BLOB_KEY")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_CONTAINER_NAME = "preprocessed-data"
AZURE_INDEX_NAME = "mlops"

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials and configuration from environment variables
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret_value = os.getenv('AZURE_CLIENT_SECRET_VALUE')
tenant_id = os.getenv('AZURE_TENANT_ID')
search_service_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
search_api_key = os.getenv('AZURE_SEARCH_API_KEY')
blob_connection_string = os.getenv('AZURE_BLOB_CONNECTION_STRING')
blob_container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')
index_name = os.getenv('AZURE_INDEX_NAME')

# Initialize Azure AD credentials
credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret_value, tenant_id=tenant_id)

# Initialize Azure Search clients
index_client = SearchIndexClient(endpoint=search_service_endpoint, credential=AzureKeyCredential(search_api_key))
indexer_client = SearchIndexerClient(endpoint=search_service_endpoint, credential=AzureKeyCredential(search_api_key))

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, HttpResponseError

def create_data_source():
    data_source_name = "blob-datasource"
    try:
        # Try to get the existing data source
        data_source = indexer_client.get_data_source_connection(data_source_name)
        print(f"Data source '{data_source_name}' already exists.")
        
    except ResourceNotFoundError:
        # Data source does not exist, so we create it
        try:
            data_source = SearchIndexerDataSourceConnection(
                name=data_source_name,
                type="azureblob",
                connection_string=blob_connection_string,
                container={"name": blob_container_name}
            )
            indexer_client.create_data_source_connection(data_source)
            print(f"Data source '{data_source_name}' created successfully.")
        
        except HttpResponseError as e:
            print(f"An error occurred while creating the data source: {e.message}")
    
    except HttpResponseError as e:
        print(f"An error occurred while checking data source: {e.message}")

# Step 2: Create Search Index
def create_search_index():
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="content", type=SearchFieldDataType.String, searchable=True)
    ]
    index = SearchIndex(name=index_name, fields=fields)

    try:
        index_client.create_or_update_index(index)
        print(f"Index '{index_name}' created or updated successfully.")
    except HttpResponseError as e:
        print(f"An error occurred while creating or updating the index: {e.message}")

# Step 3: Create Indexer
def create_indexer(indexer_name):
    indexer = SearchIndexer(
        name=indexer_name,
        data_source_name="blob-datasource",
        target_index_name=index_name,
        field_mappings=[
            {"sourceFieldName": "metadata_storage_path", "targetFieldName": "id"},
            {"sourceFieldName": "content", "targetFieldName": "content"}
        ]
    )
    try:
        indexer_client.create_indexer(indexer)
        print(f"Indexer '{indexer_name}' created successfully.")
    except ResourceExistsError:
        print(f"Indexer '{indexer_name}' already exists.")
    except HttpResponseError as e:
        print(f"An error occurred while creating the indexer: {e.message}")

# Step 4: Update Indexer
def update_indexer(indexer_name):
    indexer = SearchIndexer(
        name=indexer_name,
        data_source_name="blob-datasource",
        target_index_name=index_name,
        field_mappings=[
            {"sourceFieldName": "metadata_storage_path", "targetFieldName": "id"},
            {"sourceFieldName": "content", "targetFieldName": "content"}
        ]
    )
    try:
        indexer_client.create_or_update_indexer(indexer)
        print(f"Indexer '{indexer_name}' updated successfully.")
    except ResourceNotFoundError:
        print(f"Indexer '{indexer_name}' not found.")
    except HttpResponseError as e:
        print(f"An error occurred while updating the indexer: {e.message}")

# Step 5: Run Indexer
def run_indexer(indexer_name):
    try:
        indexer_client.run_indexer(indexer_name)
        print(f"Indexer '{indexer_name}' is running.")
    except ResourceNotFoundError:
        print(f"Indexer '{indexer_name}' not found.")
    except HttpResponseError as e:
        print(f"An error occurred while running the indexer: {e.message}")
