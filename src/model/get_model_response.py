import time
import os
import openai
import mlflow

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt, retries=3, delay=5):
    """
    Fetches a response from OpenAI API based on the prompt provided using ChatCompletion.
    Includes retry logic and delay to manage RateLimitError, with MLflow logging.

    Parameters:
    - prompt (str): The user prompt to be sent to OpenAI API.
    - retries (int): Number of retry attempts in case of a RateLimitError.
    - delay (int): Delay in seconds between retry attempts.

    Returns:
    - response (str): The generated response from OpenAI.
    """
    with mlflow.start_run(run_name="openai_response"):
        # Log input parameters
        mlflow.log_param("prompt", prompt)
        mlflow.log_param("retries", retries)
        mlflow.log_param("delay", delay)
        
        for attempt in range(retries):
            try:
                # Log retry attempt
                mlflow.log_metric("attempt", attempt + 1)
                time.sleep(1)  # Small delay before sending the request
                
                # OpenAI ChatCompletion request
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=512
                )
                
                # Log successful response
                response_content = response['choices'][0]['message']['content'].strip()
                mlflow.log_param("response", response_content)
                mlflow.log_metric("success", 1)  # Indicate success
                return response_content
            
            except openai.error.RateLimitError:
                print(f"Rate limit exceeded. Retrying in {delay} seconds (Attempt {attempt + 1} of {retries})...")
                mlflow.log_metric("rate_limit_errors", attempt + 1)
                time.sleep(delay)
        
        # If all retries fail
        mlflow.log_metric("success", 0)  # Indicate failure
        mlflow.log_param("response", "Request failed after multiple attempts due to rate limit issues.")
        return "Request failed after multiple attempts due to rate limit issues."