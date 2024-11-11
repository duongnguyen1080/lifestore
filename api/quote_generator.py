from flask import Blueprint, request, jsonify
from .utils import get_claude_response, APILimitError, InvalidResponseError, is_valid_quote

quote_bp = Blueprint('quote', __name__)

def create_prompt(user_question):
    return f"""You are a knowledgeable assistant specializing in philosophy. Your task is to provide a relevant quote from a philosopher based on the following question or topic:

"{user_question}"

Please strictly follow these guidelines:

1. Read the user's question or topic.
2. Select a relevant quote from a philosopher or thinker.
3. The quote must be an actual excerpt from the philosopher’s or thinker's original work (e.g., book, essay, lecture) and attributed correctly to both the philosopher and the work. 
4. If the quote is attributed correctly to a philosopher but the exact work where the quote is excerpted cannot be verified or found, find a new, correctly attributed quote.
5. Choose philosophers amd thinkers from various cultural backgrounds (e.g., Western, Eastern, African, Indigenous, etc.)
6. Format your response EXACTLY as follows:
   "[QUOTE]" - PHILOSOPHER NAME, SOURCE, PUBLISHED YEAR (if known)
7. Do not add any text before or after this format.
8. Do not explain, interpret, or comment on the quote.
9. Keep the quote within 100 words.
10. Longer quotes are more favorable.

Failure to follow this format exactly will be considered an error."""

@quote_bp.route('/quote', methods=['POST'])
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