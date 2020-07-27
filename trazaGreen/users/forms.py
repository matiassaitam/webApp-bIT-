# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from trazaGreen.models import User



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Ingrese un email valido")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def __init__(self,*k,**kk):
       self._user=None #para internal user storing
       super(LoginForm,self).__init__(*k,**kk)

    def validate(self):
        self._user=User.query.filter(User.email==self.email.data).first()
        return super(LoginForm,self).validate()

    def validate_email(self,field):
        if self._user is None:
            raise ValidationError(("E-Mail not recognized"))

    def validate_password(self,field):
        if self._user is None:
            raise ValidationError(("Password incorrect"))

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email(message='Enter a valid email.')])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # chequear si es None para user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Su email ya ha sido registrado!')

    def check_username(self, field):
        # chequear si es None para username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Lo siento, ese usuario ya esta tomado!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Actualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        # chequear si es None para user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Su email ya ha sido registrado!')

    def check_username(self, field):
        # chequear si es None para username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Lo siento, ese usuario ya esta tomado!')
