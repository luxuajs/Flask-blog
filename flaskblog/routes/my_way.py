from flask import render_template, url_for, redirect, session, flash
from flaskblog.models import User, Post
from flaskblog.forms import *
from flaskblog import app, db, bcrypt


def unique_values(form):
  if (User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.email.data).first()):    
    return False
  return True

# I've created a post dictionary
posts = [
    {
      "author": "Juan",
      "title": "Integer numbers",
      "content": "An integer is the number zero, a positive natural number or a negative integer. The negative numbers are the additive inverses of the corresponding positive numbers.",
      "date_posted": "January 15 2018"
    },
    { "author": "María",
      "title": "Elements for a paceful life",
      "content": "An integer is the number zero, a positive natural number or a negative integer. The negative numbers are the additive inverses of the corresponding positive numbers.",
      "date_posted": "January 18 2018"
    },
    { "author": "Fernanda",
      "title": "How do you cook arepas?",
      "content": "An integer is the number zero, a positive natural number or a negative integer. The negative numbers are the additive inverses of the corresponding positive numbers.",
      "date_posted": "February 21 2018"
    }
]


# ENDPOINTS
@app.route("/")
def home():
  return render_template("index.html", posts=posts, title="Home", name=session.get("username"))



@app.route("/about")
def about():
  return render_template("about.html", title="About")



@app.route("/login", methods=["POST", "GET"])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if bcrypt.check_password_hash(user.password, form.password.data):
      session["username"] = user.username # Here i've created a cookie
      flash(f"User logged in", "success")
      return redirect(url_for("home")) 
    else:
      flash(f"Invalid password", "info")
      return redirect(url_for("login")) 
  
  return render_template("login.html", form=form, title="Register")
  



@app.route("/register", methods=["POST", "GET"])
def register():

  form = RegistrationForm()

  if form.validate_on_submit() and unique_values(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {(form.username.data)} registered successfully", "success")
    return redirect(url_for("home")) 
  
  elif not unique_values(form):
    flash(f"This username or email is taken.", "info")
    return render_template("register.html", form=form, title="Register")
  else:
    return render_template("register.html", form=form, title="Register")
  


@app.route("/logout")
def logout():
  session.pop("username", None)
  return redirect(url_for("home"))