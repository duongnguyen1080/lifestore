from flask import Blueprint, request, jsonify
from utils import get_claude_response, APILimitError, InvalidResponseError, is_valid_quote

quote_bp = Blueprint('quote', __name__)

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

@quote_bp.route('/api/quote', methods=['POST'])
def get_quote():
    user_question = request.json['query']
    prompt = create_prompt(user_question)
    
    try:
        quote = get_claude_response(prompt)
        
        if not is_valid_quote(quote):
            raise InvalidResponseError("Invalid quote format or length")
        
        return jsonify({"quote": quote})
    
    except APILimitError as e:
        return jsonify({
            "error": e.user_message,
            "dev_error": e.dev_message
        }), 429
    
    except InvalidResponseError as e:
        return jsonify({
            "error": e.user_message,
            "dev_error": e.dev_message
        }), 400
    
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred. Please try again later.",
            "dev_error": str(e)
        }), 500