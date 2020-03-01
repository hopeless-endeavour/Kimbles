from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User

def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object('app.config.ProductionConfig')
    elif app.config["ENV"] == "development":
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)

    login = LoginManager(app)
    login.login_view = 'auth.login'
    login.init_app(app)

    @login.user_loader
    def load_user(id):

        return User.query.get(int(id))

    from app.auth.routes import auth
    from app.main.routes import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
