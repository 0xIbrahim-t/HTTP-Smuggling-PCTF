from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

# Initialize SQLAlchemy with null app
db = SQLAlchemy(session_options={"expire_on_commit": False})

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)

    # Import and register blueprints
    from .routes import blog, admin, auth
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app