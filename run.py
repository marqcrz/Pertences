from app import create_app
from flask import Flask, send_from_directory
import os

app = create_app()
app.config['SECRET_KEY'] = 'a5875d9c23a6e44ff1f3c6a58a1758a7842fb170e4d30e8a'
app.config['UPLOAD_FOLDER'] = '../app/templates/imagens/'

@app.route('/imagens/<path:filename>')
def servir_imagem(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)