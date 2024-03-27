from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, session
from app.models import ItemPerdido, Local, Categoria
from app import db
import os
from werkzeug.utils import secure_filename

# Diretório onde as imagens serão salvas
UPLOAD_FOLDER = f"pertences/app/templates/imagens"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

itens_perdidos_routes = Blueprint('itens_perdidos', __name__)

def is_authenticated():
    return session.get('authenticated', False)

# Middleware para verificar a autenticação em todas as rotas
@itens_perdidos_routes.before_request
def require_login():
    if not is_authenticated() and request.endpoint and not request.endpoint.startswith('user.login'):
        # Se o usuário não estiver autenticado e tentar acessar qualquer rota que não seja a de login,
        # ele será redirecionado para a página de login
        return redirect(url_for('user.login'))

@itens_perdidos_routes.route('/itens_perdidos')
def listar_itens_perdidos():
    data_atual = datetime.now()
    itens_perdidos = ItemPerdido.query.filter_by(encontrado='NÃO').all()
    return render_template('listar_itens_perdidos.html', itens_perdidos=itens_perdidos, data_atual=data_atual)

@itens_perdidos_routes.route('/itens_perdidos/registrar', methods=['GET', 'POST'])
def registrar_item_perdido():
    locais = Local.query.all()  # Mova essa linha para fora do bloco de condição
    categorias = Categoria.query.all()  # Mova essa linha para fora do bloco de condição

    if request.method == 'POST':
        # Obter os dados do formulário
        data_registro_str = request.form['data_registro']
        try:
            # Ajuste o formato de acordo com o formato enviado pelo formulário
            data_registro = datetime.strptime(data_registro_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            # Se houver um erro de conversão, lide com ele aqui (por exemplo, imprima uma mensagem de erro)
            print("Erro: Formato de data e hora inválido.")
        
        descricao = request.form['descricao']
        local = request.form['local']
        encontrado = request.form['encontrado']
        categoria = request.form['categoria']
        imagem = request.files['imagem']
        entregador = ''
        recebedor = ''

        descricao = descricao.upper()
        local = local.upper()
        encontrado = encontrado.upper()
        categoria = categoria.upper()

        # Salvar a imagem em algum lugar
        caminho_imagem = None
        if imagem:
            nome_arquivo = secure_filename(imagem.filename)  # Garante que o nome do arquivo é seguro
            caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            imagem.save(caminho_imagem)

        # Criar um novo item perdido
        novo_item_perdido = ItemPerdido(data_registro=data_registro, descricao=descricao, local=local, encontrado=encontrado, categoria=categoria, imagem=nome_arquivo, entregador=entregador, recebedor=recebedor)
        db.session.add(novo_item_perdido)
        db.session.commit()
        
        return redirect(url_for('itens_perdidos.listar_itens_perdidos'))

    return render_template('registrar_item_perdido.html', locais=locais, categorias=categorias)

@itens_perdidos_routes.route('/itens_perdidos/editar_item_perdido/<int:id>', methods=['GET', 'POST'])
def editar_item_perdido(id):
    item_perdido = ItemPerdido.query.get_or_404(id)
    
    if request.method == 'POST':
        # Atualizar os dados do item perdido
        item_perdido.data_registro_str = request.form['data_registro'] 
        item_perdido.data_registro = datetime.strptime(item_perdido.data_registro_str, '%Y-%m-%dT%H:%M')
        item_perdido.descricao = request.form['descricao'] 
        item_perdido.local = request.form['local'] 
        item_perdido.categoria = request.form['categoria'] 
        item_perdido.encontrado = request.form['encontrado'] 

        item_perdido.descricao = item_perdido.descricao.upper()
        item_perdido.local = item_perdido.local.upper()
        item_perdido.categoria = item_perdido.categoria.upper()
        item_perdido.encontrado = item_perdido.encontrado.upper()

        db.session.commit()
        
        return redirect(url_for('itens_perdidos.listar_itens_perdidos'))
    
    return render_template('editar_item_perdido.html', item_perdido=item_perdido)

@itens_perdidos_routes.route('/itens_perdidos/excluir_item_perdido/<int:id>', methods=['GET', 'POST'])
def excluir_item_perdido(id):
    item_perdido = ItemPerdido.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(item_perdido)

        db.session.commit()

        return jsonify({'message': 'Item excluído com sucesso'})
    
    return render_template('confirmar_exclusao.html', item_perdido=item_perdido)

@itens_perdidos_routes.route('/itens_perdidos/devolver_item_perdido/<int:id>', methods=['GET', 'POST'])
def devolver_item_perdido(id):
    item_perdido = ItemPerdido.query.get_or_404(id)
    return render_template('devolver_item_perdido.html', item_perdido=item_perdido)

@itens_perdidos_routes.route('/itens_perdidos/devolver/<int:id>', methods=['GET', 'POST'])
def devolver(id):
    item_perdido = ItemPerdido.query.get_or_404(id)
    if request.method == 'POST':
        item_perdido.encontrado = 'SIM'
        item_perdido.entregador = request.form['entregador']
        item_perdido.recebedor = request.form['recebedor']
        data_devolucao_str = request.form['data_devolucao']
        item_perdido.data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%dT%H:%M')
        item_perdido.entregador = item_perdido.entregador.upper()
        item_perdido.recebedor = item_perdido.recebedor.upper()

        db.session.commit()

        devolvido = True  # Define a variável indicando que o item foi devolvido

    else:
        devolvido = False  # Se não for uma solicitação POST, o item não foi devolvido ainda

    return render_template('devolver_item_perdido.html', item_perdido=item_perdido, devolvido=devolvido)

@itens_perdidos_routes.route('/toggle_devolvidos', methods=['POST'])
def toggle_devolvidos():
    # Lógica para mostrar ou ocultar os itens devolvidos (deixe a implementação dessa lógica para a próxima parte)
    # Certifique-se de enviar uma resposta apropriada para a solicitação AJAX, por exemplo, retornando um código de status HTTP 204 (No Content)
    return '', 204