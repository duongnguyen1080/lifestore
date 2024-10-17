from http.server import BaseHTTPRequestHandler
from utils import get_claude_response, APILimitError, InvalidResponseError, is_valid_quote
import json

def create_prompt(user_question):
    return f"""You are a knowledgeable assistant specializing in philosophy. Your task is to provide a relevant quote from a philosopher based on the following question or topic:

"{user_question}"

Please strictly follow these guidelines:

1. Read the user's question or topic.
2. Select a relevant quote from a philosopher, ensuring diversity by including philosophers amd thinkers from various cultural backgrounds (e.g., Western, Eastern, African, Indigenous, etc.)
3. Ensure the quote is from a work published before 1928.
4. Format your response EXACTLY as follows:
   "[QUOTE]" - PHILOSOPHER NAME, SOURCE, PUBLISHED YEAR (if known)
5. Do not add any text before or after this format.
6. Do not explain, interpret, or comment on the quote.
7. Keep the quote within 100 words.

Failure to follow this format exactly will be considered an error."""

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        user_question = data['query']
        prompt = create_prompt(user_question)
        
        try:
            quote = get_claude_response(prompt)
            
            if not is_valid_quote(quote):
                raise InvalidResponseError("Invalid quote format or length")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"quote": quote}).encode())
        
        except APILimitError as e:
            self.send_error(429, e.user_message)
        
        except InvalidResponseError as e:
            self.send_error(400, e.user_message)
        
        except Exception as e:
            self.send_error(500, "An unexpected error occurred. Please try again later.")