import re
import random
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from send_verification_email import send_verification_email
from cpf_validator import cpf_validador  # Importa a função de validação de CPF
from senha_valida import validar_senha

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Nicolas12345@localhost:1433/pmifinal?driver=ODBC+Driver+17+for+SQL+Server'
app.secret_key = 'sua_chave_secreta'  # Necessário para utilizar o flash

db = SQLAlchemy(app)

class Usuario(db.Model):
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    senha = db.Column(db.String(150))
    celular = db.Column(db.VARCHAR(17))
    email = db.Column(db.String(150))
    cpf = db.Column(db.String(150), unique=True)

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

        # Validar o email com regex
        if not re.match(r'.*@.*\.(com|edu|gov|org)(\.br)?$', email):
            return render_template('user_creat.html', email_erro="E-mail inválido")

        # Validar o CPF usando a função cpf_validador
        if not cpf_validador(cpf):
            return render_template('user_creat.html', cpf_invalido="CPF inválido")

        # Verificar se já existe um usuário com o mesmo CPF
        if Usuario.query.filter_by(cpf=cpf).first():
            return render_template('user_creat.html', cpf_existente="Esse CPF já foi usado")

        if not validar_senha(senha):
            return render_template('user_creat.html', senha_erro="Senha não atende os criterios de segurança ")
        
        # Salvar dados na sessão
        session['nome'] = nome
        session['senha'] = senha
        session['celular'] = celular
        session['email'] = email
        session['cpf'] = cpf

        # Redirecionar para a página de verificação de email
        return redirect(url_for('verify_email'))

@app.route('/verify_email', methods=['POST', 'GET'])
def verify_email():
    if request.method == 'POST':
        email = session.get('email')
        codigo_aleatorio = session.get('codigo_aleatorio')
        codigo_inserido = request.form['codigo']

        if codigo_inserido == codigo_aleatorio:
            nome = session.get('nome')
            senha = session.get('senha')
            celular = session.get('celular')
            cpf = session.get('cpf')

            usuario = Usuario(
                nome=nome,
                senha=senha,
                celular=celular,
                email=email,
                cpf=cpf
            )

            db.session.add(usuario)
            try:
                db.session.commit()
                flash("Usuário cadastrado com sucesso!", 'success')
                return redirect(url_for('index'))
            except IntegrityError:
                db.session.rollback()
                flash("Erro ao cadastrar usuário.", 'error')

        else:
            flash('Código de verificação incorreto.', 'error')

    else:
        email = session.get('email')
        nome = session.get('nome')
        senha = session.get('senha')
        celular = session.get('celular')
        cpf = session.get('cpf')
        codigo_aleatorio = str(random.randint(1000, 9999))
        send_verification_email(email, codigo_aleatorio)  # Chamada síncrona
        session['codigo_aleatorio'] = codigo_aleatorio

    return render_template('verify_email.html', email=email, nome=nome, senha=senha, celular=celular, cpf=cpf)

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
