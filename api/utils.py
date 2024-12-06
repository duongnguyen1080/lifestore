import os
import requests
import time
import json
from http.server import BaseHTTPRequestHandler
from pyairtable import Api 


CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')  
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')  
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")


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

def is_valid_quote(quote_data):
    required_fields = {"quote", "philosopher", "book_title", "year"}

    if not required_fields.issubset(quote_data.keys()):
        return False

    return all(quote_data.get(field, "").strip() for field in required_fields)

def query_all_airtable_books():
    airtable = Api(AIRTABLE_API_KEY).table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
    try:
        records = airtable.all()
        return [record['fields']['Book Title'] for record in records]
    except Exception as e:
        raise InvalidResponseError(f"Error fetching book titles from Airtable: {str(e)}")      

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
        airtable_books = query_all_airtable_books()
        print("Books in Airtable:", airtable_books) #debug

        response = requests.post(CLAUDE_API_URL, json=data, headers=headers)
        response.raise_for_status()
        
        claude_response = response.json()
        print("Claude API Response:", claude_response) #debug
        
        if 'error' in claude_response:
            if 'rate limit' in claude_response['error'].lower():
                raise APILimitError()
            else:
                raise InvalidResponseError(f"API error: {claude_response['error']}")
        
        quotes = claude_response.get('content', [])[0]['text']
        print("Raw Quotes from API:", quotes) #debug
        try:
            quotes_list = json.loads(quotes)
            if not isinstance(quotes_list, list):
                raise InvalidResponseError("API response is not a list of quotes")
        except json.JSONDecodeError:
            raise InvalidResponseError("Failed to parse API response as JSON")
        
        def validate_and_return_quote(item):
            if not is_valid_quote(item):
                raise InvalidResponseError("Invalid quote format")
            print ("Processing quote:", item) #debug

            book_title = item["book_title"].strip().lower()
            airtable_books_normalized = [title.strip().lower() for title in airtable_books]
            if book_title not in airtable_books_normalized:
                raise InvalidResponseError(f"Book not found in Airtable: {book_title}")
            
            original_title_index = airtable_books_normalized.index(book_title)

            return {
                    "quote": item["quote"],
                    "philosopher": item["philosopher"],
                    "book_title": airtable_books[original_title_index],
                    "year": item["year"],
                    "Amazon Link": item.get("Amazon Link")
                }
        
        return [validate_and_return_quote(item) for item in quotes_list]
    
    except requests.exceptions.RequestException as e:
        raise InvalidResponseError(f"Request failed: {str(e)}")
    
    except (KeyError, IndexError) as e:
        raise InvalidResponseError(f"Failed to parse API response: {str(e)}")
    
    except (APILimitError, InvalidResponseError):
        raise
    
    except Exception as e:
        raise InvalidResponseError(f"Unexpected error: {str(e)}")

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