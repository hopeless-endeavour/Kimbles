class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret key to be changed as soon as possible"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgres://ysfcykvennnxov:e911f42296ffa7b2d0477cc1fd60bb248ad149ee6e1513a9fe52e9f84ce57a7c@ec2-54-228-243-238.eu-west-1.compute.amazonaws.com:5432/depivghlt560jh'

    # Flask-User config
    USER_APP_NAME = "Kimbles Flask APP"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
