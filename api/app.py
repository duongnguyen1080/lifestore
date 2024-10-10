from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from quote_generator import quote_bp
from learn_more import learn_more_bp
from email_subscription import email_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    app.register_blueprint(quote_bp)
    app.register_blueprint(learn_more_bp)
    app.register_blueprint(email_bp)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify(error="Rate limit exceeded. Please try again later."), 429

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(error="An unexpected error occurred. Please try again later."), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)