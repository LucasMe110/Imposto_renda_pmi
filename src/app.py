# src/app.py

from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models.usuario import db, Usuario  # Importe a instância de db e o modelo
from forms.validators import validar_formulario, salvar_dados_na_sessao, salvar_usuario_no_bd
from services.send_verification_email import send_verification_email  # Importa corretamente a função
from config.config import Config
import random

app = Flask(__name__, template_folder='templates')
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Nicolas12345@localhost:1433/pmifinal?driver=ODBC+Driver+17+for+SQL+Server'
app.secret_key = 'sua_chave_secreta'  # Necessário para utilizar o flash
=======
app.config.from_object(Config)
>>>>>>> bfdc1450f9489a7ebf2eb575beb9151ba806d9fb

# Inicialize a instância do SQLAlchemy com a aplicação Flask
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template('user_creat.html', usuarios=usuarios)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        celular = request.form['celular']
        email = request.form['email']
        cpf = request.form['cpf']

        erros = validar_formulario(nome, senha, celular, email, cpf)

        if erros:
            return render_template('user_creat.html', **erros)

        salvar_dados_na_sessao(nome, senha, celular, email, cpf)
        return redirect(url_for('verify_email'))

@app.route('/verify_email', methods=['POST', 'GET'])
def verify_email():
    if request.method == 'POST':
        codigo_inserido = request.form['codigo']
        if codigo_inserido == session.get('codigo_aleatorio'):
            if salvar_usuario_no_bd():
                return redirect(url_for('index'))
        else:
            flash('Código de verificação incorreto.', 'error')
    else:
        email = session.get('email')
        if email:
            codigo_aleatorio = str(random.randint(1000, 9999))
            send_verification_email(email, codigo_aleatorio)
            session['codigo_aleatorio'] = codigo_aleatorio
        else:
            flash('Nenhum e-mail encontrado na sessão.', 'error')
            return redirect(url_for('index'))

    return render_template('valida_cod.html')


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
