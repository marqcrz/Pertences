from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Paciente, ItemPerdido, Pertence
from app import db
from datetime import datetime

pacientes_routes = Blueprint('pacientes', __name__)

@pacientes_routes.route('/index')
def index():
    total_pacientes = Paciente.query.count()
    total_pertences = Pertence.query.count()
    total_itens_perdidos = ItemPerdido.query.count()
    devolvido_itens_perdidos = ItemPerdido.query.filter_by(encontrado='SIM').count()
    nao_devolvido_itens_perdidos = ItemPerdido.query.filter_by(encontrado='NÃO').count()
    return render_template('index.html', total_pacientes=total_pacientes, total_itens_perdidos=total_itens_perdidos,total_pertences=total_pertences, devolvido_itens_perdidos=devolvido_itens_perdidos, nao_devolvido_itens_perdidos=nao_devolvido_itens_perdidos)


@pacientes_routes.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('listar_pacientes.html', pacientes=pacientes)

@pacientes_routes.route('/pacientes/cadastrar', methods=['GET', 'POST'])
def cadastrar_paciente():
    if request.method == 'POST':
        data_admissao_str = request.form['data_admissao']
        try:
            # Ajuste o formato de acordo com o formato enviado pelo formulário
            data_admissao = datetime.strptime(data_admissao_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            # Se houver um erro de conversão, lide com ele aqui (por exemplo, imprima uma mensagem de erro)
            print("Erro: Formato de data e hora inválido.")
        nome = request.form['nome'] 
        codigo_hygia = request.form['codigo_hygia']
        setor = request.form['setor']
        leito = request.form['leito']
        ativo = request.form['ativo']

        nome = nome.upper()
        setor = setor.upper()
        leito = leito.upper()
        ativo = ativo.upper()

        paciente = Paciente(data_admissao=data_admissao, nome=nome, codigo_hygia=codigo_hygia, setor=setor, leito=leito, ativo=ativo)
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('pacientes.listar_pacientes'))
    return render_template('cadastrar_paciente.html')
