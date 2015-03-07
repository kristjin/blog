print("NOW IMPORTING: "+__name__)
from . import keys

key = keys.BLOGFUL_SECRET_KEY

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = key