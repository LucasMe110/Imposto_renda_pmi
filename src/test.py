import re
import random
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from send_verification_email import send_verification_email
from cpf_validator import cpf_validador  # Importa a função de validação de CPF
import asyncio

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/Teste'
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
    return render_template('index.html', usuarios=usuarios)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        celular = request.form['celular']
        email = request.form['email']
        cpf = request.form['cpf']

        # Validar o email com regex
        email_erro = ''
        if not re.match(r'.*@.*.(com|edu|gov|org)(\.br)?$', email):
            email_erro = "E-mail inválido"
            return render_template('index.html', email_erro=email_erro)

        # Validar o CPF usando a função cpf_validador
        cpf_invalido = ''
        cpf_valido = cpf_validador(cpf)
        if not cpf_valido:
            cpf_invalido = "CPF invalido"
            return render_template('index.html', cpf_invalido=cpf_invalido)

        # Verificar se já existe um usuário com o mesmo CPF
        usuario_existente = Usuario.query.filter_by(cpf=cpf).first()
        cpf_existente = ''
        if usuario_existente:
            cpf_existente = "Esse CPF já foi usado"
            return render_template('index.html', cpf_existente=cpf_existente)

        # Gerar o código de verificação
        codigo_aleatorio = str(random.randint(1000, 9999))
        
        # Armazenar o código de verificação na sessão
        session['codigo_verificacao'] = codigo_aleatorio
        session['email_verificacao'] = email

        # Enviar o e-mail de verificação se ainda não foi enviado
        if not session.get('verificacao_enviada', False):
            asyncio.run(send_verification_email(email, codigo_aleatorio))
            session['verificacao_enviada'] = True

        # Redirecionar para a página de verificação de email
        return render_template('verify_email.html', email=email, nome=nome, senha=senha, celular=celular, cpf=cpf)

    return render_template('test.html')

@app.route('/verify_email', methods=['POST', 'GET'])
def verify_email():
    if request.method == 'POST':
        email = session.get('email_verificacao')
        codigo_inserido = request.form['codigo']
        codigo_esperado = session.get('codigo_verificacao')

        if codigo_inserido == codigo_esperado:
            nome = request.form['nome']
            senha = request.form['senha']
            celular = request.form['celular']
            cpf = request.form['cpf']

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
                flash('Usuário cadastrado com sucesso!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Erro ao salvar o usuário no banco de dados!', 'error')

            # Limpar o código de verificação da sessão
            session.pop('codigo_verificacao', None)
            session.pop('email_verificacao', None)
            session.pop('verificacao_enviada', None)
            # Redirecionar para a página test.html após tentativa de verificação
            return redirect(url_for('test'))
        else:
            flash('Código de verificação incorreto.', 'error')
            # Redirecionar para a página test.html após tentativa de verificação
            return redirect(url_for('test'))

    return render_template('verify_email.html')

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)







#============================================================================================================

    import smtplib
import asyncio
from email.message import EmailMessage

async def send_verification_email(email, codigo_aleatorio):
    msg = EmailMessage()
    msg['Subject'] = 'Código de Verificação'
    msg['From'] = 'lucasmellomo@gmail.com'  
    msg['To'] = email  

    html_content = f"""
    <html>
        <body>
            <p>Oi! Seu código de verificação é: <b style="font-size: 24px;">{codigo_aleatorio}</b></p>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'lucasmellomo@gmail.com'  
        smtp_password = 'xazg ocoq ywil ropc'  # Senha de aplicativo

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(smtp_username, smtp_password)

        server.send_message(msg)

        server.quit()
        
        print(f'E-mail enviado para {email} com sucesso.')

    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')


#1 xazg ocoq ywil ropc
#2 xoyn qqhd svka tynf

#gabrielbion276@gmail.com

