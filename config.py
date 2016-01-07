import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/test"


class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SPOTIFY_ID = os.environ['SPOTIFY_ID']
    SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']
    REDIRECT_URI = os.environ['REDIRECT_URI']


class ProductionConfig(DeploymentConfig):
    DEBUG = False


class DevelopmentConfig(DeploymentConfig):
    DEVELOPMENT = True
    DEBUG = True
