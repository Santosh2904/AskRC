import time
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

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