import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

class BaseCustomError(Exception):
    def __init__(self, user_message, dev_message):
        self.user_message = user_message
        self.dev_message = dev_message
        super().__init__(self.dev_message)

class APILimitError(BaseCustomError):
    def __init__(self):
        super().__init__(
            user_message="We're experiencing high demand. Please try again in a few minutes.",
            dev_message="API rate limit exceeded"
        )

class InvalidResponseError(BaseCustomError):
    def __init__(self, dev_message):
        super().__init__(
            user_message="We couldn't generate a proper response. Please try again or rephrase your query.",
            dev_message=dev_message
        )

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_claude_response(prompt, validate_quote=True):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(CLAUDE_API_URL, json=data, headers=headers)
        response.raise_for_status()
        
        claude_response = response.json()
        
        if 'error' in claude_response:
            if 'rate limit' in claude_response['error'].lower():
                raise APILimitError()
            else:
                raise InvalidResponseError(f"API error: {claude_response['error']}")
        
        content = claude_response['content'][0]['text'].strip()
        
        if validate_quote and not is_valid_quote(content):
            raise InvalidResponseError("Invalid quote format")
        
        return content
    
    except requests.exceptions.RequestException as e:
        raise InvalidResponseError(f"Request failed: {str(e)}")
    
    except (KeyError, IndexError) as e:
        raise InvalidResponseError(f"Failed to parse API response: {str(e)}")
    
    except (APILimitError, InvalidResponseError):
        raise
    
    except Exception as e:
        raise InvalidResponseError(f"Unexpected error: {str(e)}")

def is_valid_quote(quote):
    return len(quote) >= 50 and quote.startswith('"') and quote.count('"') >= 2 and ' - ' in quote