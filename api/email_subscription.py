from http.server import BaseHTTPRequestHandler
import json
import os
from sib_api_v3_sdk import Configuration, ApiClient, ContactsApi, CreateContact

configuration = Configuration()
configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
api_client = ApiClient(configuration)
contacts_api = ContactsApi(api_client)

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
        
        email = data.get('email')
        if not email:
            self.send_error(400, "Email is required")
            return

        try:
            create_contact = CreateContact(email=email, list_ids=[2])
            contacts_api.create_contact(create_contact)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Subscription successful!"}).encode())
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            self.send_error(500, "An error occurred. Please try again.")


