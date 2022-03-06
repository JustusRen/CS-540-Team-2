from flask import Flask
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.run(debug=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.DB_CONNECTION}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app