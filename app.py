from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from src.models.usuario import Usuario, db  # Corrigido para incluir o prefixo 'src'
from src.forms.validators import validar_formulario, salvar_dados_na_sessao, salvar_usuario_no_bd  # Corrigido para incluir o prefixo 'src'
from src.services.send_verification_email import send_verification_email  # Corrigido para incluir o prefixo 'src'
from src.config.config import Config
import random

app = Flask(__name__, static_folder='src/static', template_folder='src/templates')
lm = LoginManager(app)
lm.login_view = 'login'
app.config.from_object(Config)

db.init_app(app)


@app.route("/front")
def front():
    return render_template('')


@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

with app.app_context():
    db.create_all()

@app.route('/logout')
@login_required  
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/test")
@login_required
def test():
    print(current_user)
    return render_template('test.html')

@app.route("/")
def index():
    return render_template('index.html')  # Renderiza o index.html com os links

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('emailForm')  # Use get para evitar o erro
        senha = request.form.get('senhaForm')   # Use get para evitar o erro

        user = db.session.query(Usuario).filter_by(email=email, senha=senha).first()
        if not user:
            error_message = "Email ou senha incorretos"
            return render_template('login.html', error_message=error_message)

        login_user(user)
        return redirect(url_for('test'))  # Assegure-se de que 'test' é um endpoint válido

@app.route("/criar_conta")
def criar_conta():
    usuarios = Usuario.query.all()
    return render_template('criarconta.html', usuarios=usuarios)  # Redireciona para a página de criação de conta

@app.route('/add', methods=['POST', 'GET'])
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
        
        print(erros)  # <-- Adicione aqui para verificar os erros
      
        if erros:
            return render_template('criarconta.html', erros=erros)

        # Salvando os dados se tudo estiver correto
        salvar_dados_na_sessao(nome, data_nascimento, cpf, celular, email, senha, cep)
        return redirect(url_for('verify_email'))

@app.route('/verify_email', methods=['POST', 'GET'])
def verify_email():
    email = session.get('email')  # Obtém o e-mail da sessão
    if request.method == 'POST':
        # Combine os valores dos quatro campos do formulário para formar o código completo
        codigo_inserido = (
            request.form.get('code-1') +
            request.form.get('code-2') +
            request.form.get('code-3') +
            request.form.get('code-4')
        )
        
        # Verifica se o código inserido é o mesmo que foi enviado ao usuário
        if codigo_inserido == session.get('codigo_aleatorio'):
            # Salva o usuário no banco de dados e retorna a instância do usuário
            usuario = salvar_usuario_no_bd()
            if usuario:
                login_user(usuario)  # Autentica o usuário após cadastro
                return redirect(url_for('index'))
            else:
                flash('Erro ao salvar o usuário no banco de dados.', 'error')
        else:
            flash('Código de verificação incorreto.', 'error')
    else:
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
    app.run(debug=True, host='0.0.0.0', port=80)

