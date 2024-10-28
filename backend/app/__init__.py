from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)

    with app.app_context():
        # Import routes here to avoid circular imports
        from .routes import blog, admin, auth
        
        # Register blueprints
        app.register_blueprint(blog.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(auth.bp)

        # Create database tables
        db.create_all()

        return app