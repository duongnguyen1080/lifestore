from flask import Blueprint, request, jsonify
from utils import get_claude_response, APILimitError, InvalidResponseError

quote_bp = Blueprint('quote', __name__)

def create_prompt(user_question):
    return f"""You are a knowledgeable assistant specializing in philosophy. Your task is to provide a relevant quote from a philosopher based on the following question or topic:

"{user_question}"

Please strictly follow these guidelines:

1. Read the user's question or topic carefully.
2. Select 3 relevant quotes that must be an actual excerpt from a philosopher's or thinker's original work (e.g., book, essay, lecture) and attributed correctly to both the philosopher and the work. 
3. Each quote must be at least 20 words long.
4. Ensure at least one quote is from a philosopher who is not a Western philosopher.
5. Format each quote EXACTLY as follows:
   "[QUOTE]" - PHILOSOPHER NAME, "SOURCE", PUBLISHED YEAR (if known) -
6. Do not add any text before or after this format.
7. Do not explain, interpret, or comment on the quote.

Any deviation from the format or failure to include all required fields will result in an error."""

@quote_bp.route('/quote', methods=['POST'])
def get_quote():
    try:
        user_question = request.json['query']
        # Check if query is an object instead of string
        if isinstance(user_question, dict):
            raise InvalidResponseError("Invalid query format")
            
        if not isinstance(user_question, str) or not user_question.strip():
            raise InvalidResponseError("Query must be a non-empty string")
            
        prompt = create_prompt(user_question)
        quotes = get_claude_response(prompt)
        return jsonify({"quotes": quotes})
    
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