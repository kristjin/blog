class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = "a661XTGadfa&@BN&$@4g25uh%@#nhwrtw35mlpo"


class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"