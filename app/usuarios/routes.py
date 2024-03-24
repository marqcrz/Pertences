from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import User
from app import db

usuario_routes = Blueprint('user', __name__)

# Função para verificar se o usuário está autenticado
def is_authenticated():
    return session.get('authenticated', False)

# Middleware para verificar a autenticação em todas as rotas
@usuario_routes.before_request
def require_login():
    if not is_authenticated() and request.endpoint and not request.endpoint.startswith('user.login'):
        return redirect(url_for('user.login'))

@usuario_routes.route('/', methods=['GET', 'POST'])
def login():
    error_message = None  # Inicializa a mensagem de erro como None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['authenticated'] = True
            session['role'] = user.role  # Armazena o papel do usuário na sessão
            return redirect(url_for('pacientes.index'))  # Redirecionar para a página desejada após o login
        else:
            error_message = 'Nome de usuário ou senha incorretos'
    return render_template('login.html', error_message=error_message)

@usuario_routes.route('/sair')
def sair():
    session.pop('authenticated', None)
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('user.login'))

@usuario_routes.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        # Verificar se o e-mail já está em uso
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Se o e-mail já estiver em uso, exibir uma mensagem de erro
            error_message = 'Este e-mail já está sendo usado. Por favor, escolha outro.'
            return jsonify({'success': False, 'message': error_message})

        # Se o e-mail estiver disponível, criar o novo usuário
        new_user = User(username=username, name=name, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Retornar uma mensagem de sucesso
        success_message = 'Usuário cadastrado com sucesso!'
        return jsonify({'success': True, 'message': success_message})

    # Se o método não for POST, retornar uma mensagem de erro
    elif request.method == 'GET':
        return render_template('cadastrar_usuario.html')