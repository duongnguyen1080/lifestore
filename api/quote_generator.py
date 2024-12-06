from flask import Blueprint, request, jsonify
from utils import get_claude_response, APILimitError, InvalidResponseError, is_valid_quote, query_all_airtable_books

quote_bp = Blueprint('quote', __name__)

def create_prompt(user_question):
    book_titles = query_all_airtable_books()
    book_list = ", ".join([f'"{book.strip()}"' for book in book_titles])
    return f"""You are a knowledgeable assistant specializing in philosophy. Your task is to provide a relevant quote from a philosopher based on the following question or topic:

"{user_question}"

Please strictly follow these guidelines:

1. Read the user's question or topic carefully.
2. Provide 5 quotes from the following books: {book_list}.
3. Each quote must be a JSON array. Each object should include:
- "quote": The exact text of the quote.
- "philosopher": The name of the philosopher or thinker.
- "book_title": The title of the book or source (must match one of the provided titles exactly).
- "year": The year of publication (leave it blank if unknown).
- "Amazon Link": The Amazon link to the book (leave it blank if unknown).
5. Do not include any text or explanation outside of the JSON array.
6. Ensure that all book titles match exactly with those in the provided list. Failure to do so will cause the response to be rejected.
7. Any deviation from the format or failure to include all required fields will result in an error."""

@quote_bp.route('/quote', methods=['POST'])
def get_quote():
    user_question = request.json['query']
    prompt = create_prompt(user_question)
    
    try:
        quote = get_claude_response(prompt)
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