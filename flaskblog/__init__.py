import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

# APP
app = Flask(__name__)
app.app_context().push()
app.config.from_object("flaskblog.configs.Develoment_Config")
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = "foug gttb xkoc zhcx"
app.config["MAIL_USE_TLS"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mailbox = Mail(app)


from flaskblog.forms import *
from flaskblog.routes import *

