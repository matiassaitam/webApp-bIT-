from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from trazaGreen import db
from trazaGreen.models import MiCultivo
from trazaGreen.mis_cultivos.forms import MiCultivoForm

mis_cultivos = Blueprint('mis_cultivos',__name__)

@mis_cultivos.route('/create',methods=['GET','POST'])
@login_required
def crear_cultivo():
    form = MiCultivoForm()

    if form.validate_on_submit():

        mi_cultivo = MiCultivo(nombre_cultivo =form.nombre_cultivo.data,
                             lote =form.lote.data,
                             origen =form.origen.data,
                             caracteristicas =form.caracteristicas.data,
                             user_id =current_user.id
                             )
        db.session.add(mi_cultivo)
        db.session.commit()
        flash("Su cultivo ha sido creado")
        return redirect(url_for('core.trazaCultivo'))

    return render_template('crear_cultivo.html',form=form)


# int: asegurarse que mi_cultivo_id sea pasado como un integro
# en vez de string asi se puede buscar.
@mis_cultivos.route('/<int:mi_cultivo_id>')
def mi_cultivo(mi_cultivo_id):
    # traer el cultivo por id o retornar 404
    mi_cultivo = MiCultivo.query.get_or_404(mi_cultivo_id)
    return render_template('trazaCultivo.html',nombre_cultivo=mi_cultivo.nombre_cultivo,
                            fecha=mi_cultivo.fecha,cultivo=mi_cultivo
    )

@mis_cultivos.route("/<int:mi_cultivo_id>/update", methods=['GET', 'POST'])
@login_required
def update(mi_cultivo_id):
    mi_cultivo = MiCultivo.query.get_or_404(mi_cultivo_id)
    if mi_cultivo.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = MiCultivoForm()
    if form.validate_on_submit():
        mi_cultivo.nombre_cultivo = form.nombre_cultivo.data
        mi_cultivo.lote = form.lote.data
        mi_cultivo.origen = form.origen.data
        mi_cultivo.caracteristicas = form.caracteristicas.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('mis_cultivos.crear_cultivo', mi_cultivo_id=mi_cultivo.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.nombre_cultivo.data = mi_cultivo.nombre_cultivo
        form.lote.data = mi_cultivo.lote
        form.origen.data = mi_cultivo.origen
        form.caracteristicas.data = mi_cultivo.caracteristicas
    return render_template('crear_cultivo.html', title='Update',
                           form=form)


@mis_cultivos.route("/<int:mi_cultivo_id>/delete", methods=['POST'])
@login_required
def delete_cultivo(mi_cultivo_id):
    mi_cultivo = MiCultivo.query.get_or_404(mi_cultivo_id)
    if mi_cultivo.author != current_user:
        abort(403)
    db.session.delete(mi_cultivo)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.trazaCultivo'))
