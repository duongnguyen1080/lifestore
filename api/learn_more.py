from flask import Blueprint, request, jsonify
from .utils import get_claude_response, APILimitError, InvalidResponseError 
import logging

learn_more_bp = Blueprint('learn_more', __name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@learn_more_bp.route('/learn-more', methods=['POST'])
def get_author_info():
    print("=== Learn More API Called ===")
    print("Request Headers:", request.headers)
    print("Request Data:", request.get_json())
    try:
        logger.debug("Received learn-more request")
        data = request.json  
        logger.debug(f"Request data: {data}")

        if not data:
            logger.error("No data provided in request")
            return jsonify({
                "error": "No data provided. Please try again with your query.",
                "dev_error": "No JSON data provided"
            }), 400

        quote_text = data.get('quote')
        philosopher = data.get('philosopher')
        source = data.get('source')
        year = data.get('year')
        user_question = data.get('userQuestion')

        logger.debug(f"""
            Parsed data:
            quote: {quote_text}
            philosopher: {philosopher}
            source: {source}
            year: {year}
            user_question: {user_question}
        """)

        if not all([quote_text, philosopher, source, user_question]):
            logger.error(f"Missing required fields: {[k for k, v in {'quote': quote_text, 'philosopher': philosopher, 'source': source, 'userQuestion': user_question}.items() if not v]}")
            missing = [k for k, v in {
                'quote': quote_text, 
                'philosopher': philosopher, 
                'source': source, 
                'userQuestion': user_question
            }.items() if not v]
            return jsonify({
                "error": "Some information is missing. Please try asking your question again.",
                "dev_error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        prompt = f"""Analyze the following quote and provide detailed information about it, the author, and its relevance to the user's question:

Quote: "{quote_text}"
Author: {philosopher}
Source: {source} {f'({year})' if year else ''}
User's Question: "{user_question}"

When providing information, use a conversational and engaging tone, as if you're explaining the topic to someone who is genuinely curious and seeking guidance. Make it feel personal and reflective, as if you understand the user's situation. Avoid rigid, academic language. Here's what to include:

1. About The Author:
   - Provide a brief biography of {philosopher}.
   - Focus on what makes them relatable or interesting. Make the philosopher feel like a real person, not just a historical figure.
   - Keep this section within 50 words.

2. About The Work:
   - Provide a simple, relatable overview of {source}.
   - Mention the work's significance in {philosopher}'s career and in the broader field of philosophy, in a way that invites curiosity.
   - Limit to 100 words.

3. How This Quote Speaks to Your Question:
   - Describe where in {source} this quote is excerpted from (if known).
   - Explain the quote's meaning in everyday terms. 
   - Show empathy by connecting its wisdom directly to the user's life situation.
   - Keep this section within 100 words.
   
Use HTML tags for headings and paragraphs but focus on making the content feel human, relatable, and insightful. Use HTML tags to bold each heading and number them, too."""

        logger.debug("Sending prompt to Claude")
        content = get_claude_response(prompt, content_type='html')
        logger.debug(f"Received response from Claude: {content[:200]}...")
        return jsonify({"content": content})

    except APILimitError as e:
        logger.error(f"API Limit Error: {e.dev_message}")
        return jsonify({ 
            "error": e.user_message,
            "dev_error": e.dev_message
        }), 429 

    except InvalidResponseError as e:
        logger.error(f"Invalid Response Error: {e.dev_message}")
        return jsonify({
            "error": e.user_message,
            "dev_error": e.dev_message
        }), 400

    except Exception as e: 
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "An unexpected error occurred. Please try again later.",
            "dev_error": str(e)
        }), 500