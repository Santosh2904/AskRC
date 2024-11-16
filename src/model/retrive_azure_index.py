from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import mlflow

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


def search_azure_index(query, top=8):
    """
    Retrieves top relevant documents from Azure Search and prepares them for OpenAI prompt.
    Logs query details and results using MLflow.
    
    Parameters:
    - query (str): The search query to look up in Azure Search.
    - top (int): Number of top results to fetch (default is 8).
    
    Returns:
    - context (str): A concatenated string of relevant document contents or an appropriate message if no results are found.
    """
    with mlflow.start_run(run_name="retrieve_azure_index"):
        mlflow.log_param("question", query)
        mlflow.log_metric("top", top)

        try:
            # Retrieve search results from Azure Search
            results = search_client.search(search_text=query, top=top)

            # Convert SearchItemPaged to a list for processing
            results_list = list(results)

            # Extract content from search results if available
            if results_list:
                context = "\n\n".join([doc.get('content', '') for doc in results_list])
                mlflow.log_param("response_count", len(results_list))
            else:
                context = "No relevant information found."
                mlflow.log_param("response_count", 0)

            # Log the response content length for monitoring
            mlflow.log_metric("context_length", len(context))

        except Exception as e:
            # Log error details and re-raise the exception
            mlflow.log_param("error", str(e))
            raise

    return context