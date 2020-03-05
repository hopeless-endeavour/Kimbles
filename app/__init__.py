from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_user import UserManager
from .models import db, User

def create_app():
    """ Initialise and configure flask app """

    app = Flask(__name__)

    # use required config settings depending on stage of the program
    if app.config["ENV"] == "production":
        app.config.from_object('app.config.ProductionConfig')
    elif app.config["ENV"] == "development":
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)

    # initialise flask login manager
    login = LoginManager(app)
    login.login_view = 'auth.login'
    login.init_app(app)

    # initialise flask user manager
    user_manager = UserManager(app, db, User)

    
    @login.user_loader
    def load_user(id):

        return User.query.get(int(id))

    from app.auth.routes import auth
    from app.main.routes import main

    # register two blueprints to flask app
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
