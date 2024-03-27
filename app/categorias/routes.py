from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import User, Categoria
from app import db

categoria_routes = Blueprint('categoria', __name__)

# Função para verificar se o usuário está autenticado
def is_authenticated():
    return session.get('authenticated', False)

# Middleware para verificar a autenticação em todas as rotas
@categoria_routes.before_request
def require_login():
    if not is_authenticated() and request.endpoint and not request.endpoint.startswith('user.login'):
        return redirect(url_for('user.login'))

@categoria_routes.route('/listar_categorias')
def listar_categorias():
    categorias = Categoria.query.all()

    categorias_json = []
    for categoria in categorias:
        categoria_json = {
            'id': categoria.id,
            'nome_categoria': categoria.nome_categoria,  # Corrigido para 'nome_local'
        }
        categorias_json.append(categoria_json)

    return jsonify(categorias_json)  # Corrigido para retornar locais_json

# Corrigido o nome do endpoint para 'local.cadastrar_local'
@categoria_routes.route('/cadastrar_categoria', methods=['GET', 'POST'])
def cadastrar_categoria():
    if request.method == 'POST':
        nome_categoria = request.form['nome_categoria']

        existing_categoria = Categoria.query.filter_by(nome_categoria=nome_categoria).first()
        if existing_categoria:
            error_message = 'Este categoria já está sendo usada. Por favor, escolha outro nome.'
            return jsonify({'success': False, 'message': error_message})

        new_cat = Categoria(nome_categoria=nome_categoria)
        db.session.add(new_cat)
        db.session.commit()

        success_message = 'Categoria cadastrada com sucesso!'
        return jsonify({'success': True, 'message': success_message})

    elif request.method == 'GET':
        return render_template('cadastrar_categorias.html')
    
@categoria_routes.route('/excluir_categoria/<int:id>', methods=['DELETE'])
def excluir_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Categoria excluída com sucesso'}), 200
