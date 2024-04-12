from wtforms.validators import ValidationError
from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from flaskblog.models import User

# FOR REGISTER FORM
def verify_password(form, field):
  if not any(list(filter(lambda x: x in field.data, ascii_lowercase))) or\
     not any(list(filter(lambda x: x in field.data, ascii_uppercase))) or\
     not any(list(filter(lambda x: x in field.data, punctuation))) or\
     not any(list(filter(lambda x: x in field.data, digits))):
    message="Your password must contain at least one uppercase, lowecase, number and special character."
    raise ValidationError(message)
  
def validate_username_reg(form, field):
  name = field.data

  if User.query.filter_by(username=name).first():
    raise ValidationError("This username is taken, please choose other one.")
    

def validate_email_reg(form, field):
  email = field.data

  if User.query.filter_by(email=email).first():
    raise ValidationError("This emial is taken, please choose other one.")

