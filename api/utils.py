import os
import requests
import time
import json
from http.server import BaseHTTPRequestHandler

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
    # Get Claude API response and check valid quote
    
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

def rate_limit(handler_instance):
    client_ip = handler_instance.client_address[0]
    current_time = time.time()
    
    # This is a simple in-memory rate limit. For production, use a distributed cache like Redis
    if not hasattr(handler_instance, 'rate_limit_data'):
        handler_instance.rate_limit_data = {}
    
    if client_ip in handler_instance.rate_limit_data:
        last_request_time, count = handler_instance.rate_limit_data[client_ip]
        if current_time - last_request_time < 60:  # 1 minute window
            if count >= 10:  # 10 requests per minute
                return False
            handler_instance.rate_limit_data[client_ip] = (last_request_time, count + 1)
        else:
            handler_instance.rate_limit_data[client_ip] = (current_time, 1)
    else:
        handler_instance.rate_limit_data[client_ip] = (current_time, 1)
    
    return True

# New error handling function
def handle_error(handler_instance, status_code, message):
    handler_instance.send_response(status_code)
    handler_instance.send_header('Content-type', 'application/json')
    handler_instance.end_headers()
    handler_instance.wfile.write(json.dumps({"error": message}).encode())

# New wrapper for request handling
def handle_request(handler_class):
    original_do_POST = handler_class.do_POST
    
    def wrapped_do_POST(self):
        if not rate_limit(self):
            handle_error(self, 429, "Rate limit exceeded")
            return
        
        try:
            original_do_POST(self)
        except Exception as e:
            handle_error(self, 500, str(e))
    
    handler_class.do_POST = wrapped_do_POST
    return handler_class