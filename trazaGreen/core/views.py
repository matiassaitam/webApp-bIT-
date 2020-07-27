from flask import render_template,request,Blueprint
from trazaGreen.models import MiCultivo
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3
from flask_wtf import FlaskForm
from wtforms import Form

core = Blueprint('core',__name__)

@core.route('/trazaCultivo')
def trazaCultivo():
    '''
    Esta es la vista para los cultivos.
    Notese como usa la paginacion para mostrat un numero limitado de cultivos,
    limitando el tamaño de la query y luego llamando paginate
    '''
    page = request.args.get('page', 1, type=int)
    mis_cultivos = MiCultivo.query.order_by(MiCultivo.fecha.desc()).paginate(page=page, per_page=10)
    return render_template('trazaCultivo.html',mis_cultivos=mis_cultivos)

@core.route('/dashboard')
@login_required
def dashboard():
    '''

    '''
    return render_template('dashboard.html', name=current_user.username)

@core.route('/')
def index():
    '''

    '''
    return render_template('index.html')

@core.route('/precios')
def precios():
    '''

    '''
    return render_template('prices.html')


@core.route('/info')
def info():
    '''

    '''
    return render_template('info.html')
