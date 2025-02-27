from flask import Flask
from .extensions import db, migrate
from .models import User, Document, Token, UserSession
from app.v1.user_view import user_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    migrate.init_app(app, db)

    app.register_blueprint(user_bp)

    return app
