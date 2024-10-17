from http.server import BaseHTTPRequestHandler
import json
from utils import get_claude_response, APILimitError, InvalidResponseError

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        authorInfo = data.get('authorInfo')
        userQuestion = data.get('userQuestion')
        quote = data.get('quote')

        if not all([authorInfo, userQuestion, quote]):
            self.send_error(400, "Missing required fields")
            return

        prompt = f"""Analyze the following quote and provide detailed information about it, the author, and its relevance to the user's question:

Quote: "{quote}"
Author Information: {authorInfo}
User's Question: "{userQuestion}"

When providing information, use a conversational and engaging tone, as if you're explaining the topic to someone who is genuinely curious and seeking guidance. Make it feel personal and reflective, as if you understand the user's situation. Avoid rigid, academic language. Here's what to include:

1. About The Author:
   - Provide a brief biography of the author.
   - Focus on what makes them relatable or interesting. Make the philosopher feel like a real person, not just a historical figure.
   - Keep this section within 50 words.

2. About The Work:
   - Provide a simple, relatable overview of the mentioned work.
   - Mention the work's significance in the author's career and in the broader field of philosophy, in a way that invites curiosity.
   - Limit to 100 words.

3. How This Quote Speaks to Your Question:
   - Describe where in the mentioned work this quote is excerpted from (if known).
   - Explain the quote's meaning in everyday terms. 
   - Show empathy by connecting its wisdom directly to the user's life situation.
   - Keep this section within 100 words.
   
Use HTML tags for headings and paragraphs but focus on making the content feel human, relatable, and insightful. Use HTML tags to bold each heading and number them, too."""

        try:
            content = get_claude_response(prompt, validate_quote=False)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"content": content}).encode())

        except APILimitError as e:
            self.send_error(429, e.user_message)
        except InvalidResponseError as e:
            self.send_error(400, e.user_message)
        except Exception as e:
            self.send_error(500, "An unexpected error occurred. Please try again later.")