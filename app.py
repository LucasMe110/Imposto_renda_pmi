from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from src.models.usuario import Usuario, db  # Corrigido para incluir o prefixo 'src'
from src.forms.validators import validar_formulario, salvar_dados_na_sessao, salvar_usuario_no_bd  # Corrigido para incluir o prefixo 'src'
from src.services.send_verification_email import send_verification_email  # Corrigido para incluir o prefixo 'src'
from src.config.config import Config
import random
from src.models.usuario import Classe
from src.models.usuario import Notas
from src.services.gerar_link import gerar_string_com_id



app = Flask(__name__, static_folder='src/static', template_folder='src/templates')
lm = LoginManager(app)
lm.login_view = 'login'
app.config.from_object(Config)

db.init_app(app)

@app.route("/gerar_codigo_usuario", methods=["GET"])  # Alterado o endpoint
@login_required
def gerar_codigo_usuario():  # Nome da função alterado para evitar conflito
    # Obtém o ID do usuário atual
    usuario_id = current_user.id
    # Gera o código com base no ID do usuário
    codigo = gerar_string_com_id(usuario_id)
    print(codigo)
    return f"Código gerado: {codigo}"


@app.route("/front")
def front():
    return render_template('main.html')



@app.route("/compartilhado/<string:codigo>")
def compartilhado(codigo):

    try:
        # Extrai o ID: começa no 7º caractere e termina antes da próxima letra
        id_usuario = ""
        print(codigo)
        for char in codigo[6:]:  # Começa no 7º caractere
            if char.isdigit():
                id_usuario += char
            else:
                break  # Para ao encontrar a próxima letra
            print(id_usuario)
        id_usuario = int(id_usuario)  # Converte para inteiro
        
    except ValueError:
        return "Código inválido.", 400

    # Busca o usuário no banco de dados
    usuario = db.session.query(Usuario).filter_by(id=id_usuario).first()

    if not usuario:
        return f"Usuário com ID {id_usuario} não encontrado.", 404

    return render_template("compartilhado.html", usuario=usuario)


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

@app.route("/home", methods=['GET'])
@login_required
def home():
    # Obtém o ID do usuário atual
    usuario_id = current_user.id
    # Gera o código com base no ID do usuário
    codigo = gerar_string_com_id(usuario_id)
    # Renderiza o template com o código gerado
    return render_template('home.html', codigo=codigo)


@app.route("/notas", methods=['POST', 'GET'])
@login_required
def notas():
    # Consulta as notas enviadas pelo usuário atual
    notas_usuario = Notas.query.filter_by(usuario_id=current_user.id).all()
    
    return render_template('notas.html', notas=notas_usuario)

@app.route("/")
def index():
    return render_template('index.html')  

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    # Verifica se os campos obrigatórios foram enviados
    if 'arquivo' not in request.files or 'categoria' not in request.form:
        flash("Arquivo e categoria são obrigatórios.", "error")
        print("Erro: Arquivo ou categoria não enviados.")
        return redirect(request.url)

    arquivo = request.files['arquivo']
    categoria_nome = request.form['categoria']

    # Verifica se o arquivo tem um nome válido
    if arquivo.filename == '':
        flash("Nenhum arquivo selecionado.", "error")
        print("Erro: Nenhum arquivo selecionado.")
        return redirect(request.url)

    # Lê o conteúdo do arquivo como binário
    binario = arquivo.read()
    print(f"Arquivo recebido: {arquivo.filename}")
    print(f"Categoria recebida: {categoria_nome}")
    print(f"Conteúdo binário do arquivo (primeiros 50 bytes): {binario[:50]}...")

    # Verifica ou cria a categoria
    categoria = Classe.query.filter_by(nome=categoria_nome).first()
    if not categoria:
        print(f"Categoria '{categoria_nome}' não encontrada. Criando nova categoria.")
        categoria = Classe(nome=categoria_nome)
        db.session.add(categoria)
        db.session.commit()
    else:
        print(f"Categoria '{categoria_nome}' encontrada: ID {categoria.id}")

    # Cria a nova entrada na tabela Notas
    usuario_atual = current_user  # Usuário autenticado
    nova_nota = Notas(
        usuario_id=usuario_atual.id, 
        classe_id=categoria.id, 
        binario=binario
    )

    # Adiciona e salva no banco de dados
    try:
        db.session.add(nova_nota)
        db.session.commit()

        # Consulta o registro recém-criado no banco de dados
        nota_salva = Notas.query.filter_by(id=nova_nota.id).first()
        if nota_salva:
            print(f"Nota salva no banco: ID {nota_salva.id}, UsuarioID {nota_salva.usuario_id}, ClasseID {nota_salva.classe_id}")
        else:
            print("Erro: Nota não encontrada no banco após commit.")

        flash("Arquivo enviado e armazenado com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        print("Erro ao salvar no banco de dados:", e)
        flash("Erro ao salvar o arquivo no banco de dados.", "error")
        return redirect(request.url)

    return redirect(url_for('home'))


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
        return redirect(url_for('home'))

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
                return redirect(url_for('login'))
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

