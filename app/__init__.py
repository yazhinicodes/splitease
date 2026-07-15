import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
     app = Flask(__name__)

     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

     db.init_app(app)
     jwt.init_app(app)
     bcrypt.init_app(app)

     from app import models
     from app.routes.auth import auth_bp
     from app.routes.groups import groups_bp
     from app.routes.expenses import expenses_bp
     from app.routes.balances import balances_bp

     app.register_blueprint(auth_bp, url_prefix='/auth')
     app.register_blueprint(groups_bp, url_prefix='/groups')
     app.register_blueprint(expenses_bp, url_prefix='/groups')
     app.register_blueprint(balances_bp, url_prefix='/groups')

     return app

