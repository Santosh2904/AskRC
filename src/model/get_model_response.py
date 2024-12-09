import time
import os
import openai

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt, retries=5, delay=10):
    """
    Fetches a response from the OpenAI API using the ChatCompletion endpoint.
    
    Args:
        prompt (str): The user input or query.
        retries (int): Number of retries in case of a RateLimitError. Default is 3.
        delay (int): Delay in seconds between retry attempts. Default is 5 seconds.

    Returns:
        str: The AI-generated response from OpenAI.

    Raises:
        Exception: If the request fails after all retries.
    """
    for attempt in range(1, retries + 1):
        try:
            # Delay between retries (only for retries, not the first attempt)
            if attempt > 1:
                time.sleep(delay)

            # OpenAI ChatCompletion request
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
            )
            
            # Return the AI-generated response
            return response['choices'][0]['message']['content'].strip()

        except openai.error.RateLimitError:
            print(f"Rate limit exceeded. Retrying in {delay} seconds (Attempt {attempt} of {retries})...")
        
        except openai.error.OpenAIError as e:
            # Handle generic OpenAI API errors
                print(f"An error occurred: {str(e)}")
                break
 
    # If retries are exhausted
    return "Request failed after multiple attempts due to rate limit or API issues."
