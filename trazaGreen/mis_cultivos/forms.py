from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MiCultivoForm(FlaskForm):
    # no es posible contener titulos o textos vacios
    # agarraremos la fecha automaticamente por el Model
    nombre_cultivo = StringField('Nombre de Cultivo', validators=[DataRequired()])
    lote = StringField('Lote', validators=[DataRequired()])
    origen = TextAreaField('Origen', validators=[DataRequired()])
    caracteristicas = TextAreaField('Caracteristicas', validators=[DataRequired()])
    submit = SubmitField('MiCultivo')
