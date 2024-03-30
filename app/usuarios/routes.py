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
            session['user_id'] = user.id 
            session['name'] = user.name 
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
    
@usuario_routes.route('/cadastrar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(username):

    usuario = username.query.get_or_404(username)
    
    if request.method == 'POST':
        # Atualizar os dados do item perdido
        usuario.username = request.form['username'] 
        usuario.name = request.form['name'] 
        usuario.password = request.form['password'] 
        usuario.email = request.form['email'] 
        usuario.role = request.form['role'] 

        usuario.username = usuario.username.upper()
        usuario.name = usuario.name.upper()
        usuario.password = usuario.password.upper() 
        usuario.email = usuario.email.upper() 
        usuario.role = usuario.role.upper() 

        db.session.commit()
        
        return redirect(url_for('usuario.cadastrar_usuario'))
    
    return render_template('cadastrar_usuario.html', usuario=usuario)

@usuario_routes.route('/listar_usuarios')
def listar_usuarios():
    # Consulte o banco de dados para obter todos os usuários cadastrados
    usuarios = User.query.all()

    # Formate os dados dos usuários em um formato JSON
    usuarios_json = []
    for usuario in usuarios:
        usuario_json = {
            'id': usuario.id,
            'username': usuario.username,
            'name': usuario.name,
            'email': usuario.email,
            # Adicione outros atributos do usuário conforme necessário
        }
        usuarios_json.append(usuario_json)

    # Retorne os dados dos usuários como uma resposta JSON
    return jsonify(usuarios_json)

@usuario_routes.route('/excluir_usuario/<int:id>', methods=['DELETE'])
def excluir_usuario(id):

    # Verificar se há um usuário autenticado na sessão
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Nenhum usuário autenticado encontrado.'}), 401

    # Obter o ID do usuário atualmente autenticado na sessão
    id_usuario_autenticado = session['user_id']

    # Verificar se o ID do usuário sendo excluído é o mesmo que o ID do usuário autenticado
    if id == id_usuario_autenticado:
        return jsonify({'success': False, 'message': 'Você não pode excluir a si mesmo.'}), 403

    # Proceder com a exclusão do usuário normalmente
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuário excluído com sucesso'}), 200

@usuario_routes.route('/admin')
def admin():
    # Renderiza o template admin.html
    return render_template('admin.html')

    # O código abaixo estava fora da função admin(), corrigido para estar dentro dela
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuário excluído com sucesso'})


