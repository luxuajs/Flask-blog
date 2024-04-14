from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flaskblog.models import User, Post
from wtforms import StringField, SubmitField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired, Email, EqualTo, ValidationError
from flaskblog.forms.custom_validators import verify_password, validate_username_reg, validate_email_reg

# The min and max length for password
min=8
max=16

class RegistrationForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(message="Please, give a username"), Length(min=2, max=50, message="Username between 2 and 50 characters"),
                                                 validate_username_reg])
  email = EmailField("Email", validators=[DataRequired(message="Please, enter a email"), Email(message="Invalid email, check and try again"), validate_email_reg])
  password = PasswordField("Password", 
                           validators=[DataRequired(message="Please enter a password"),Length(min=min, max=max, 
                                              message=f"Remind the length of your \
                                              password must be among {min} and {max} characters"),
                                              verify_password])
  confirm = PasswordField("Confirm password", validators=[InputRequired(message="Please confirm your password"),EqualTo('password', message="Passwords must match")])
  submit = SubmitField("Sing up")




class LoginForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired("Please, enter a email"), Email(message="Invalid email, check and try again")])
  password = PasswordField("Password", 
                           validators=[DataRequired(message="Please enter a password"),Length(min=8, max=16, 
                                              message=f"Remind the length of your \
                                              password must be among {min} and {max} characters.")])

  remember = BooleanField("Remember me") # If the user wants the current login to be maintained over time.
  submit = SubmitField("Log in")



class UpdateAccountForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(message="Please, give a username"), Length(min=2, max=50, message="Username between 2 and 50 characters")])
  email = EmailField("Email", validators=[DataRequired(message="Please, enter a email"), Email(message="Invalid email, check and try again")])
  image = FileField("Update your profile picture", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
  submit = SubmitField("Update")

  def validate_username(form, field):
    name = field.data
    if name != current_user.username:
      if User.query.filter_by(username=name).first():
        raise ValidationError("This username is taken, please choose other one.")
    
  def validate_email(form, field):
    email = field.data
    if email != current_user.email:
      if User.query.filter_by(email=email).first():
        raise ValidationError("This emial is taken, please choose other one.")
      

class PostForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired("Please, enter a title"), Length(min=3, max=50, message="Your title must be between 3 and 50 character.")])
  content = TextAreaField("Content", validators=[DataRequired("Please, enter a content"), Length(min=2, message="Your content almost must has 2 character")])
  submit = SubmitField("Post")
