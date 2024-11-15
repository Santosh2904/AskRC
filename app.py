import os
import openai
import time
import streamlit as st
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from src.model.retrive_azure_index import search_azure_index
from src.model.system_prompt import create_system_prompt
from src.model.get_model_response import get_openai_response
from src.evaluation.user_question_bias import check_bias_in_user_question
from src.evaluation.model_response_bias import check_bias_in_model_response
from src.evaluation.answer_validation import key_concept_match 

# Load environment variables from .env file
load_dotenv()

def main():
    st.set_page_config(page_title="AskRC", page_icon="🎓")
    st.header("AskRC 🎓")

    user_question = st.text_input("Ask a Question")

    if st.button("Get Answer"):
        with st.spinner("Processing..."):
            # Step 1: Check for bias in the user question
            user_question_clean, bias_message = check_bias_in_user_question(user_question)
            
            if bias_message:
                # Display rephrase suggestion if bias is detected
                st.warning(bias_message)
            else:
                # Step 2: Retrieve context from Azure Search
                context = search_azure_index(user_question_clean)
                
                # Step 3: Create the system prompt
                system_prompt = create_system_prompt(context, user_question_clean)
                
                # Step 4: Get response from OpenAI API
                answer = get_openai_response(system_prompt)
                
                # Step 5: Check for bias in the model response
                answer_clean, response_bias_message = check_bias_in_model_response(answer)
                
                # Step 6: Validate answer relevance using key concept match
                if key_concept_match(answer_clean, context):
                    st.write(answer_clean)
                    if response_bias_message:
                        st.warning(response_bias_message)
                    else:
                        st.success("Answer provided.")
                else:
                    st.warning("The answer lacks sufficient contextual relevance.")

# Run the app
if __name__ == "__main__":
    main()
