from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from .extensions import db, migrate
from flask_cors import CORS


from .models import User, Document, Token, UserSession

from app.v1.user_view import user_bp
from app.v1.auth import auth_bp

from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SAMESITE"] = "None"
    app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    migrate.init_app(app, db)

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    CORS(app, origins="*", supports_credentials=True, expose_headers=["Set-Cookie"], allow_headers=["Content-Type", "Authorization"])

    jwt = JWTManager(app)

    return app
