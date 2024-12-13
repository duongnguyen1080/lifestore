import os
import requests
import time
import json
from http.server import BaseHTTPRequestHandler
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

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

def is_valid_quote(quote_text):
    """Validate quote format: "[QUOTE]" - PHILOSOPHER NAME, "SOURCE", YEAR"""
    if not isinstance(quote_text, str):
        return False
        
    # Check basic structure
    if not (quote_text.startswith('"') and '" -' in quote_text):
        return False
    
    # Check if has philosopher and source
    parts = quote_text.split('" -')
    if len(parts) != 2 or ',' not in parts[1]:
        return False
        
    return True

def get_claude_response(prompt, content_type='quote'):
    if not CLAUDE_API_KEY:
        raise InvalidResponseError("Claude API key is not set")
        
    headers = {
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "x-api-key": CLAUDE_API_KEY
    }
    
    print(f"Using API key: {CLAUDE_API_KEY[:8]}...") # Only print first 8 chars for security
    
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
        print("Claude Response:", claude_response)
        
        if 'error' in claude_response:
            if 'rate limit' in claude_response['error'].lower():
                raise APILimitError()
            else:
                raise InvalidResponseError(f"API error: {claude_response['error']}")
        
        content = claude_response.get('content', [])[0]['text']
        print("Raw Content:", content)

        if content_type == 'html':
            return content  # Return HTML content directly
        
        # For quote type, continue with quote validation
        quotes = [q.strip() for q in content.split('\n') if q.strip()]
        print("Split Quotes:", quotes)
        
        valid_quotes = []
        for quote in quotes:
            print("Checking quote:", quote)
            if is_valid_quote(quote):
                valid_quotes.append(quote)
            else:
                print("Invalid quote format:", quote)
        
        print("Valid Quotes:", valid_quotes)
        return valid_quotes if content_type == 'quote' else content
        
    except requests.exceptions.RequestException as e:
        raise InvalidResponseError(f"Request failed: {str(e)}")
    
    except (KeyError, IndexError) as e:
        raise InvalidResponseError(f"Failed to parse response: {str(e)}")
    
    except (APILimitError, InvalidResponseError):
        raise
    
    except Exception as e:
        raise InvalidResponseError(f"Unexpected error: {str(e)}")

def rate_limit(handler_instance):
    client_ip = handler_instance.client_address[0]
    current_time = time.time()
    
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

def handle_error(handler_instance, status_code, message):
    handler_instance.send_response(status_code)
    handler_instance.send_header('Content-type', 'application/json')
    handler_instance.end_headers()
    handler_instance.wfile.write(json.dumps({"error": message}).encode())

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