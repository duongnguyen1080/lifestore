from flask import Blueprint, request, jsonify
from sib_api_v3_sdk import Configuration, ApiClient, ContactsApi, CreateContact
import os
from mixpanel_utils import mp

email_bp = Blueprint('email', __name__)

configuration = Configuration()
configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
api_client = ApiClient(configuration)
contacts_api = ContactsApi(api_client)

@email_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    try:
        create_contact = CreateContact(email=email, list_ids=[2])  
        contacts_api.create_contact(create_contact)
        mp.track(email, 'Subscribe', {
            'previous_interactions': 0
        })
        return jsonify({'message': 'Subscription successful!'}), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred. Please try again.'}), 500