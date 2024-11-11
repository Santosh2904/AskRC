import os
import openai
import time
import streamlit as st
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure Search setup
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_INDEX_NAME = "askrcindex"

# Configure Search Client for Azure
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

def create_system_prompt(context, question):
    """Creates a structured system prompt for OpenAI based on retrieved context and user question."""
    return f"""
    Human: Use the following pieces of context to provide a concise answer to the question at the end. Summarize with 250 words and include detailed explanations. 
    If you don't know the answer, just say that you don't know; don't try to make up an answer.

    <context>
    {context}
    </context>

    Question: {question}

    Assistant:
    """

def get_openai_response(prompt, retries=3, delay=5):
    """Fetches a response from OpenAI API based on the prompt provided using ChatCompletion.
    Includes retry logic and delay to manage RateLimitError."""
    for attempt in range(retries):
        try:
            # Delay between retries
            time.sleep(1)  # Adjust to manage rate limits
            
            # OpenAI ChatCompletion request
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Using gpt-3.5-turbo as per the updated requirement
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512
            )
            return response['choices'][0]['message']['content'].strip()
        
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded. Retrying in {delay} seconds (Attempt {attempt + 1} of {retries})...")
            time.sleep(delay)
    
    return "Request failed after multiple attempts due to rate limit issues."

def search_azure_index(query):
    """Retrieves top relevant documents from Azure Search and prepares them for OpenAI prompt."""
    # Use search_text instead of query
    results = search_client.search(search_text=query, top=3)
    # Extract the content fields from search results
    context = "\n\n".join([doc['content'] for doc in results if 'content' in doc]) if results else "No relevant information found."
    return context

def main():
    # Update Streamlit app UI
    st.set_page_config(page_title="AskRC", page_icon="🎓")
    
    st.header("AskRC 🎓")

    user_question = st.text_input("Ask a Question")

    if st.button("Get Answer"):
        with st.spinner("Processing..."):
            # Retrieve context from Azure Search index
            context = search_azure_index(user_question)
            # Create system prompt
            system_prompt = create_system_prompt(context, user_question)
            # Generate response using OpenAI
            answer = get_openai_response(system_prompt)
            # Display answer
            st.write(answer)
            st.success("Done")

if __name__ == "__main__":
    main()

