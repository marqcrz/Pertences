from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import User, Local
from app import db

local_routes = Blueprint('local', __name__)

# Função para verificar se o usuário está autenticado
def is_authenticated():
    return session.get('authenticated', False)

# Middleware para verificar a autenticação em todas as rotas
@local_routes.before_request
def require_login():
    if not is_authenticated() and request.endpoint and not request.endpoint.startswith('user.login'):
        return redirect(url_for('user.login'))

@local_routes.route('/listar_locais')
def listar_locais():
    locais = Local.query.all()

    locais_json = []
    for local in locais:
        local_json = {
            'id': local.id,
            'nome_local': local.nome_local,  # Corrigido para 'nome_local'
        }
        locais_json.append(local_json)

    return jsonify(locais_json)  # Corrigido para retornar locais_json

# Corrigido o nome do endpoint para 'local.cadastrar_local'
@local_routes.route('/cadastrar_local', methods=['GET', 'POST'])
def cadastrar_local():
    if request.method == 'POST':
        nome_local = request.form['nome_local']

        existing_local = Local.query.filter_by(nome_local=nome_local).first()
        if existing_local:
            error_message = 'Este local já está sendo usado. Por favor, escolha outro nome.'
            return jsonify({'success': False, 'message': error_message})

        new_local = Local(nome_local=nome_local)
        db.session.add(new_local)
        db.session.commit()

        success_message = 'Local cadastrado com sucesso!'
        return jsonify({'success': True, 'message': success_message})

    elif request.method == 'GET':
        return render_template('cadastrar_locais.html')
    
@local_routes.route('/excluir_local/<int:id>', methods=['DELETE'])
def excluir_local(id):
    local = Local.query.get_or_404(id)
    db.session.delete(local)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Local excluído com sucesso'}), 200
