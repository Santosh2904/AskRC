from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables for Azure
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_INDEX_NAME = "askrcindex"

# Configure Search Client for Azure
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

def search_azure_index(query):
    """Retrieves top relevant documents from Azure Search and prepares them for OpenAI prompt."""
    results = search_client.search(search_text=query, top=3)
    # Extract relevant information from search results
    context = "\n\n".join([doc['content'] for doc in results if 'content' in doc]) if results else "No relevant information found."
    # Return the extracted context
    return context
