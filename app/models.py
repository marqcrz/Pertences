from datetime import datetime, timezone
from app import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_admissao = db.Column(db.DateTime, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    codigo_hygia = db.Column(db.Integer, nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    leito = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.String(10), nullable=False)
    pertences = db.relationship('Pertence', backref='paciente', lazy=True)

class Pertence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    entregue = db.Column(db.String(200), nullable=False)
    paciente_id = db.Column(db.String(100), db.ForeignKey('paciente.id'))

class ItemPerdido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    local = db.Column(db.String(200), nullable=False)
    encontrado = db.Column(db.String(3), nullable=False)
    categoria = db.Column(db.String(200), nullable=False)
    data_registro = db.Column(db.DateTime, nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    recebedor = db.Column(db.String(200), nullable=True)
    entregador = db.Column(db.String(200), nullable=True)
    data_devolucao = db.Column(db.DateTime, nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_local = db.Column(db.String(100), unique=True, nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_categoria = db.Column(db.String(100), unique=True, nullable=False)    

class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)   