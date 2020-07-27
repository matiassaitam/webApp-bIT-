import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)

#############################################################################
############ CONFIGURACIONES (Puede ser distinto archivo separado CONFIG.PY FILE) ###############
###########################################################################

# Recordar setear variables de entorno al deployear
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
Migrate(app,db)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# Ahora podemos pasar nuestra app a login manager
login_manager.init_app(app)

# Decirles a usuarios que vista ir al hacer login
login_manager.login_view = "users.login"


###########################
#### BLUEPRINT CONFIGS #######
#########################

# Importarlos al principio si se quiere
# aqui para facilitar referencia
from trazaGreen.core.views import core
from trazaGreen.users.views import users
from trazaGreen.mis_cultivos.views import mis_cultivos
from trazaGreen.error_pages.handlers import error_pages

# Registrar las apps
app.register_blueprint(users)
app.register_blueprint(mis_cultivos)
app.register_blueprint(core)
app.register_blueprint(error_pages)
