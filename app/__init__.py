from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pertences.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Registrar blueprints
    from app.pacientes.routes import pacientes_routes
    app.register_blueprint(pacientes_routes)

    from app.pertences.routes import pertences_routes
    app.register_blueprint(pertences_routes)

    from app.itens_perdidos.routes import itens_perdidos_routes
    app.register_blueprint(itens_perdidos_routes)

    from app.usuarios.routes import usuario_routes
    app.register_blueprint(usuario_routes)

    # Criar tabelas no banco de dados
    with app.app_context():
        db.create_all()

    return app
