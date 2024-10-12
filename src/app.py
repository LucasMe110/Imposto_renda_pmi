from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models.usuario import db, Usuario  # Importe a instância de db e o modelo
from forms.validators import validar_formulario, salvar_dados_na_sessao, salvar_usuario_no_bd
from services.send_verification_email import send_verification_email  # Importa corretamente a função
from config.config import Config
import random

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

# Inicialize a instância do SQLAlchemy com a aplicação Flask
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')  # Renderiza o index.html com os links

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/criar_conta")
def criar_conta():
    usuarios = Usuario.query.all()
    return render_template('criarconta.html', usuarios=usuarios)  # Redireciona para a página de criação de conta

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome-completo']
        data_nascimento = request.form['data-nascimento']
        cpf = request.form['cpf']
        celular = request.form['celular']
        email = request.form['email']
        confirmar_email = request.form['confirmar-email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar-senha']
        cep = request.form['cep']  # Captura o CEP

        # Validações
        erros = validar_formulario(nome, data_nascimento, cpf, celular, email, confirmar_email, senha, confirmar_senha, cep)

        if erros:
            return render_template('criarconta.html', erros=erros)

        # Salvando os dados se tudo estiver correto
        salvar_dados_na_sessao(nome, data_nascimento, cpf, celular, email, senha, cep)
        return redirect(url_for('verify_email'))

@app.route('/verify_email', methods=['POST', 'GET'])
def verify_email():
    if request.method == 'POST':
        # Combine os valores dos quatro campos do formulário para formar o código completo
        codigo_inserido = (request.form.get('code-1') +
                           request.form.get('code-2') +
                           request.form.get('code-3') +
                           request.form.get('code-4'))
        if codigo_inserido == session.get('codigo_aleatorio'):
            if salvar_usuario_no_bd():
                return redirect(url_for('index'))
        else:
            flash('Código de verificação incorreto.', 'error')
    else:
        email = session.get('email')
        if email:
            # Gera um código aleatório de 4 dígitos e envia por e-mail
            codigo_aleatorio = str(random.randint(1000, 9999))
            send_verification_email(email, codigo_aleatorio)
            session['codigo_aleatorio'] = codigo_aleatorio
        else:
            flash('Nenhum e-mail encontrado na sessão.', 'error')
            return redirect(url_for('index'))

    # Retorna o template 'valida_cod.html' e passa a variável 'email'
    return render_template('valida_cod.html', email=email)

if __name__ == '__main__':
    app.run(debug=True)
