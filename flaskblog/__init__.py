from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_login import LoginManager

# APP
app = Flask(__name__)
app.app_context().push()
app.config.from_object("flaskblog.configs.Develoment_Config")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from flaskblog.forms import *
from flaskblog.routes import *

