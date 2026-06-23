"""
Flask application factory.
"""
import os
from flask import Flask

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static"),
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"),
    )

    app.config["SECRET_KEY"] = "dev-key"
    app.config["UPLOAD_FOLDER"] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "static", "uploads"
    )
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
