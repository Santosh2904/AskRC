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
