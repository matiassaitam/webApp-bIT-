from trazaGreen import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# UserMixin:
# atributos para invocar en views
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# user_loader permite que flask-login conecte al current user
# y tome su id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Crear tabla en db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    imagen_perfil = db.Column(db.String(20), nullable=False, default='default_perfil.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # esto conecta misCultivos con el User conectado.
    cultivos = db.relationship('MiCultivo', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

class MiCultivo(db.Model):
    # Setup para relacionar MiCultivo con User table
    users = db.relationship(User)

    # modelo para mis Cultivos en website
    id = db.Column(db.Integer, primary_key=True)
    # conectar mi_cultivo con el autor en particular
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nombre_cultivo = db.Column(db.Text, nullable=False)
    lote = db.Column(db.Text, nullable=False)
    origen = db.Column(db.String(140), nullable=False)
    caracteristicas = db.Column(db.Text, nullable=False)


    def __init__(self, nombre_cultivo, lote, origen, caracteristicas, user_id):
        self.nombre_cultivo = nombre_cultivo
        self.lote = lote
        self.origen = origen
        self.caracteristicas = caracteristicas
        self.user_id =user_id


    def __repr__(self):
        return f"Cultivo Id: {self.id} --- Fecha: {self.fecha} --- Nombre de Cultivo: {self.nombre_cultivo}"
