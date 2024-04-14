import secrets, os
from flask import render_template, url_for, redirect, flash, request, session, abort
# from sqlalchemy import text
from PIL import Image
from flaskblog.models import User, Post
from flaskblog.forms import *
from flaskblog import app, db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user


@app.errorhandler(403)
def error_403(err):
  return render_template("error_403.html"), 403



# ENDPOINTS
@app.route("/home")
@app.route("/")
def home():
  page = request.args.get("page", 1, type=int)
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
  return render_template("index.html", posts=posts, title="Home")



@app.route("/about")
def about():
  return render_template("about.html", title="About")



@app.route("/login", methods=["POST", "GET"])
def login():  
  form = LoginForm()

  if request.method == 'POST':
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      flash("User logged in successfully", "success")
      next_page = session.get('next_page')
      return redirect(next_page) if next_page else redirect(url_for("home"))
    else:
      flash("Password or email invalid, check and try again.", "warning")     
  session["next_page"] = request.args.get('next')
  return render_template("login.html", title="login", form=form)



@app.route("/register", methods=["POST", "GET"])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {(form.username.data)} registered successfully", "success")
    return redirect(url_for("home")) 
  else:
    return render_template("register.html", form=form, title="Register")



def save_image(form_image):
  name = secrets.token_hex()
  _, f_ext = form_image.filename.split('.')
  name_file = name + '.' + f_ext
  url = os.path.join(app.root_path, 'static/imgs/profile_pics', name_file)

  # Using Pillow to save a smaller image as a photo account.
  image_size = (125,125)
  my_image = Image.open(form_image)
  my_image.thumbnail(image_size)

  my_image.save(url) # Here i've saved the image in the database
  return name_file


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
  form = UpdateAccountForm()

  if form.validate_on_submit():
    
    # <<<<< NOTA ESTA ES LA FORMA EN COMO IBA HACERLO Y FUNCIONA OJITO A ESO >>>>>
    # db.session.execute(text(f'''UPDATE user
    #                         SET username='{form.username.data}', email='{form.email.data}'
    #                         WHERE id={current_user.id}
    #                    '''))

    # <<<<< NOTA ESTA ES LA FORMA MÁS SENCILLA DE HACERLO >>>>>
    #########
    if form.image.data:
      image_file = save_image(form.image.data) # Note: save_image return a file name, see line 58-70
      current_user.image_file = image_file

    current_user.username = form.username.data # Estas tres lineas actualizan los datos del usuario
    current_user.email = form.email.data       # solo con current_user (usuario actual) podemos cambiar sus valores

    db.session.commit()                        # y con session.commit() actualizamos los valores en el databases
    #########
    flash("Your account has been updated.", 'success')
    return redirect(url_for('account'))
  
  elif request.method == "GET":
    form.username.data = current_user.username
    form.email.data = current_user.email

  image_file = url_for('static', filename="imgs/profile_pics/") + current_user.image_file
  return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():

  form = PostForm()
  if form.validate_on_submit():
    flash("Your post has been created", "success")
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('home'))
  
  return render_template("create_post.html", title="New Post", form=form, legend="New Post")


@app.route("/post/<int:post_id>", methods=["GET","POST"])
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', title=post.title, post=post)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@app.route("/post/<int:post_id>/update", methods=["POST","GET"])
@login_required
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)

  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash("Your post has been update!", "success")
    return redirect(url_for("post", post_id=post.id))
  
  elif request.method == "GET":
    form.title.data = post.title
    form.content.data = post.content
  return render_template('update.html', form=form, title="Update Post", post=post, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)

  if(current_user != post.author):
    abort(403)

  db.session.delete(post)
  db.session.commit()
  flash('Your post has been deleted!', 'success')
  return redirect(url_for("home"))



@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("home"))




@app.route("/user/<int:user_id>")
def user_post(user_id):
  user = User.query.filter_by(id=user_id).first_or_404()
  page = request.args.get("page", 1, type=int)
  posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
  return render_template("user_post.html", posts=posts, title="Home", user=user)