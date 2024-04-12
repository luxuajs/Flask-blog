import secrets, os
from flask import render_template, url_for, redirect, flash, request, session
# from sqlalchemy import text
from PIL import Image
from flaskblog.models import User
from flaskblog.forms import *
from flaskblog import app, db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user

# ENDPOINTS
@app.route("/")
def home():
  posts = Post.query.all()
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

  image_file = url_for('static', filename="imgs/profile_pis") + current_user.image_file
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
  return render_template("create_post.html", title="New Post", form=form)


@app.route("/post/<int:id>")
def post(id):
  post = Post.query.get_or_404(id)
  return render_template('post.html',post=post)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# QUEDAMOS AQUÍ PARA RESOLVER EL PROBLEMA DE ACTUALIZAR UNA PUBLICACIÓN
# DEBEMOS TENER EN CUENTA QUE TAMBIEN PARA PODER ACTUALIZAR UNA PUBLICACIÓN
# EL USUARIO QUE VA ACTUALIZAR DEBE SER EL MISMO QUE ESTA EN SESIÓN ACTIVA
# OJITO CON ESO OjO
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@app.route("/update/post/<int:id>", methods=["POST","GET"])
@login_required
def update_post(id):

  form = UpdatePostForm()
  post = Post.query.get_or_404(id)
  if form.validate_on_submit():
    post.title = form.title
    post.date_posted = form.date_posted
    post.co
  return render_template('update.html', form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("home"))