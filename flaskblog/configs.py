#  In this module i've put all configuration for the flask app.
import os

from flaskblog.secret_keys import secret_key, wtf_csrf_secret_key

class Config(object):
  HOST = "0.0.0.0"
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("./flaskblog/database") + "/my_database.db"
  DEBUG = False
  SECRET_KEY = secret_key
  WTF_CSRF_SECRET_KEY = wtf_csrf_secret_key

class Develoment_Config(Config):
  DEBUG = True

class Production_Config(Config):
  pass