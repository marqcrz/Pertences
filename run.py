from app import create_app
from flask import Flask, send_from_directory
import os

app = create_app()

app.secret_key = 'segredo'

app.config['UPLOAD_FOLDER'] = '../app/templates/imagens/'

@app.route('/imagens/<path:filename>')
def servir_imagem(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)