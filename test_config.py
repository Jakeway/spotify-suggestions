class TestingConfig(object):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/test"