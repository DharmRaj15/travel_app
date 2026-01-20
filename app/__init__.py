import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    """Application factory function"""
    # Use absolute paths for template and static folders
    basedir = os.path.dirname(__file__)
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Load configuration
    if config is None:
        from config import Config
        app.config.from_object(Config)
    else:
        app.config.update(config)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    app.secret_key="SOME KEY"

    # Register blueprints/routes
    from app.routes import register_routes
    register_routes(app)
    
    return app
