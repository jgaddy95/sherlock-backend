from flask import Flask
from flask_cors import CORS
from .routes import upload_bp, file_bp, chat_bp, scan_bp


def create_app():
    app = Flask(__name__)
    CORS(app,resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Set the upload folder path here

    # Register blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(scan_bp)

    return app

# # If you're using this file as the entry point
# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)

# from flask import Flask
# from flask_cors import CORS
# from .routes import upload_bp, scan_bp, chat_bp

# def create_app():
#     app = Flask(__name__)
#     CORS(app)  # Enable CORS for all domains on all routes

#     # Register blueprints
#     app.register_blueprint(upload_bp)
#     app.register_blueprint(scan_bp)
#     app.register_blueprint(chat_bp)

#     return app