from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt

# 1. Define extensions FIRST
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ishi-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 2. Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    # 3. Import blueprints INSIDE the function to avoid circular errors
    from .auth import auth as auth_blueprint
    from .client import client as client_blueprint
    from .admin import admin as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(client_blueprint, url_prefix='/game')
    app.register_blueprint(admin_blueprint, url_prefix='/ishi')

    with app.app_context():
        db.create_all()

    return app