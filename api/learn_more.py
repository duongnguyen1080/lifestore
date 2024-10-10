from flask import Blueprint, request, jsonify
from utils import get_claude_response, APILimitError, InvalidResponseError

learn_more_bp = Blueprint('learn_more', __name__)

@learn_more_bp.route('/api/learn-more', methods=['POST'])
def get_author_info():
    try:
        data = request.json  
        if not data:
            return jsonify({
                "error": "No data provided. Please try again with your query.",
                "dev_error": "No JSON data provided"
            }), 400

        authorInfo = data.get('authorInfo')
        userQuestion = data.get('userQuestion')
        quote = data.get('quote')

        if not all([authorInfo, userQuestion, quote]):
            missing = [k for k, v in {'authorInfo': authorInfo, 'userQuestion': userQuestion, 'quote': quote}.items() if not v]
            return jsonify({
                "error": "Some information is missing. Please try asking your question again.",
                "dev_error": f"Missing required fields: {', '.join(missing)}"
            }), 400

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

        content = get_claude_response(prompt, validate_quote=False)
        return jsonify({"content": content})

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