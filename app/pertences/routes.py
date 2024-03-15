from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Pertence, Paciente
from app import db

pertences_routes = Blueprint('pertences', __name__)

@pertences_routes.route('/pertences')
def listar_pertences():
    pertences = Pertence.query.all()
    return render_template('listar_pertences.html', pertences=pertences)

@pertences_routes.route('/pertences/cadastrar', methods=['GET', 'POST'])
def cadastrar_pertence():
    if request.method == 'POST':
        paciente_nome = request.form['paciente_nome']
        descricao = request.form['descricao']
        estado = request.form['estado']
        entregue = request.form['entregue']

        paciente_nome = paciente_nome.upper()
        descricao = descricao.upper()
        estado = estado.upper()
        entregue = entregue.upper()

        pertence = Pertence(paciente_nome=paciente_nome, descricao=descricao, estado=estado, entregue=entregue)
        db.session.add(pertence)
        db.session.commit()
        return redirect(url_for('pertences.listar_pertences'))

    # Recupere a lista de pacientes do banco de dados
    pacientes = Paciente.query.all()
    
    # Passe a lista de pacientes para o template Jinja
    return render_template('cadastrar_pertence.html', pacientes=pacientes)