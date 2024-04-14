from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Explicación de este código
'''
  Basicamente este el decorador le dice a la extensión que esta es la función que permite
  obtener un usuario atraves de su ID, esto permite que lo mantengamos en sesiones largas
  de usuario, incluso cuando sin querer el usuario le da cerrar a la venta esto permite 
  que el usuario siga en sesión
'''
@login_manager.user_loader 
def login_user(user_id):
  return User.query.filter_by(id=user_id).first()

# Nota: UserMixin es para agregar unos atributos que la extensión le da a los usuarios para
# poder trabajar de una mejor manera con ellos, esos atributos son:
# is_authenticated, is_active, is_anonymous, get_id()
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
  password = db.Column(db.String(60), nullable=False)

  # Definimos una relación entre la tabla User y la tabla Post, con la línea de abajo
  # creamos esta realción, tener en cuenta que el argumento backref es similarl a crear
  # una columna llamada author en la tabla Post que se relaciona con un usuario de la 
  # tabla User, el argumento lazy=True hace que los datos relacionados no se carguen 
  # al menos que sea pidan explicitamente, esto es util ya que el usuario puede tener miles de 
  # Post o millones de post y la idea es no saturar al sistema.
  post = db.relationship("Post", backref="author", lazy=True)

  def __repr__(self):
    return f"User({self.username},{self.email},{self.image_file})"
  

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  content = db.Column(db.Text, nullable=False)

  # Aquí creamos la columna que realiza la relación entre las tablas, es importante notar que 
  # a la hora de usar el d.ForeignKey se llama a la tabla user que es de la clase User, pero por
  # defecto el nombre de la clase User se pasa a lowecase, es decir, user y para acceder a una columna
  # en este caso a la del id pues se usa el punto . ejemplo: user.id
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


  def __repr__(self):
    return f"Post({self.title},{self.date_posted})"
  