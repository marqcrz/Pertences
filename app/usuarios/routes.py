from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from app.models import User
from app import db
import hashlib

usuario_routes = Blueprint('user', __name__)

@usuario_routes.route('/')
def login():
    return render_template('login.html')

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from app.models import User
from app import db
import hashlib

usuario_routes = Blueprint('user', __name__)

@usuario_routes.route('/')
def login():
    return render_template('login.html')

@usuario_routes.route('/validar', methods=['POST'])
def validar():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Consultar o banco de dados para encontrar o usuário com o nome fornecido
        user = User.query.filter_by(username=username).first()

        # Verificar se o usuário existe e se a senha fornecida corresponde à senha armazenada no banco de dados
        if user and user.password == password:
            # Se as credenciais estiverem corretas, armazenar o nome de usuário na sessão
            session['user'] = user.username
            # Redirecionar para a página desejada após o login
            return redirect(url_for('pacientes.index'))  # Redirecionar para a página desejada após o login
        else:
            # Se as credenciais estiverem incorretas, retornar uma mensagem de erro em formato JSON
            return jsonify({'success': False, 'message': 'Nome de usuário ou senha incorretos'})


@usuario_routes.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        username = request.form['username']
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
        new_user = User(username=username, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Retornar uma mensagem de sucesso
        success_message = 'Usuário cadastrado com sucesso!'
        return jsonify({'success': True, 'message': success_message})

    # Se o método não for POST, retornar uma mensagem de erro
    else:
        return jsonify({'success': False, 'message': 'Método não permitido'})
