from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file, current_app
from flask_login import login_user, current_user, logout_user, login_required
from trazaGreen import db
from werkzeug.security import generate_password_hash,check_password_hash
from trazaGreen.models import User, MiCultivo
from trazaGreen.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from trazaGreen.users.picture_handler import add_profile_pic

import os

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # agarrar usuario de tabla y modelo de User
        user = User.query.filter_by(email=form.email.data).first()

        # Chequear si usuario es correcto y contraseña
        # El verify_password metodo viene del objeto User
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user is not None and user.check_password(form.password.data):
            #Inicio de sesion usuario
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('core.dashboard'))
            # Si un usuario trata de solicitar pagina que requiere login
            # flask la graba como 'next'.
            next = request.args.get('next')
            # cheqquear si next existe
            # si no visitar pagina de bienvenida.
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
        else:
            flash('Wrong email or password')
            return render_template("login.html", form=form)
    return render_template('login.html', form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.imagen_perfil = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    imagen_perfil = url_for('static', filename='profile_pics/' + current_user.imagen_perfil)
    return render_template('account.html', imagen_perfil=imagen_perfil, form=form)


@users.route("/<username>")
def user_cultivos(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    cultivos = Cultivo.query.filter_by(author=user).order_by(Cultivo.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_cultivos.html', cultivos=cultivos, user=user)

@users.route('/trazacode')
def trazacode():
    return render_template('trazacode.html')

@users.route('/converted',methods = ['POST'])
def convert():
    global tex
    tex = request.form['test']
    return render_template('converted.html')

@users.route('/download')
def download():
    qrgen(tex)
    filename = tex+'.png'
    return send_file(filename,as_attachment=True)
