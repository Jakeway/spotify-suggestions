import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24).encode('hex')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SPOTIFY_ID = os.environ['SPOTIFY_ID']
    SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']
    REDIRECT_URI = os.environ['REDIRECT_URI']
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']
    REDIS_PASSWORD = os.environ['REDIS_PASSWORD']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/test"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
