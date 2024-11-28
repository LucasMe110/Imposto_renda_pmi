from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
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
import base64


app = Flask(__name__, static_folder='src/static', template_folder='src/templates')
lm = LoginManager(app)
lm.login_view = 'login'
app.config.from_object(Config)

db.init_app(app)

@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

with app.app_context():
    db.create_all()





@app.route("/compartilhado/<string:codigo>", methods=['GET'])
@login_required
def compartilhado(codigo):
    usuario_id = current_user.id  # Obtém o ID do usuário autenticado

    try:
        # Extrai o ID do usuário compartilhado do código
        id_compartilhado = ""
        for char in codigo[6:]:  # Começa no 7º caractere
            if char.isdigit():
                id_compartilhado += char
            else:
                break  # Para ao encontrar a próxima letra
        id_compartilhado = int(id_compartilhado)  # Converte para inteiro
        
    except ValueError:
        return "Código inválido.", 400

    # Busca o usuário compartilhado no banco de dados
    usuario_compartilhado = db.session.query(Usuario).filter_by(id=id_compartilhado).first()

    if not usuario_compartilhado:
        return f"Usuário com ID {id_compartilhado} não encontrado.", 404

    # Suponha que o compartilhamento envolva "notas" ou algo relacionado ao usuário compartilhado
    notas = db.session.query(Notas, Classe.nome).join(Classe, Notas.classe_id == Classe.id).filter(
        Notas.usuario_id == id_compartilhado
    ).all()

    # Processa as notas e organiza as informações
    arquivos = []
    categorias = set()

    for nota, categoria in notas:
        categorias.add(categoria)  # Adiciona a categoria
        if nota.binario:
            # Converte para Base64
            imagem_base64 = base64.b64encode(nota.binario).decode('utf-8')
            arquivos.append({
                'url': f"data:image/png;base64,{imagem_base64}",
                'nome': f"Arquivo {nota.id}",
                'categoria': categoria,
                'id': nota.id  # Adiciona o ID aqui
            })

    # Prepara a lista de categorias para filtros
    categorias = list(categorias)

    return render_template(
        'compartilhado.html',
        usuario_compartilhado=usuario_compartilhado,
        arquivos=arquivos,
        categorias=categorias,
        categorias_dropdown=[{'value': cat, 'label': cat} for cat in categorias]  # Para o dropdown
    )



@app.route('/logout')
@login_required  
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route("/home", methods=['GET'])
@login_required
def home():
    usuario_id = current_user.id
    
    # Consulta para contar o número de notas por classe e pegar imagens associadas
    notas = db.session.query(
        Classe.nome,
        Notas.binario
    ).join(Notas, Classe.id == Notas.classe_id)\
     .filter(Notas.usuario_id == usuario_id)\
     .all()
    
    imagens_por_classe = {}
    for classe_nome, binario in notas:
        if classe_nome not in imagens_por_classe and binario:
            # Pega apenas a primeira imagem por classe, convertendo para Base64
            imagens_por_classe[classe_nome.lower()] = base64.b64encode(binario).decode('utf-8')
    
    contagem_classes = {
        classe.lower(): sum(1 for c, _ in notas if c.lower() == classe.lower())
        for classe, _ in notas
    }
    
    bens = contagem_classes.get("bens", 0)
    despesas_dedutiveis = contagem_classes.get("despesas dedutiveis", 0)
    gastos_tributaveis = contagem_classes.get("gastos tributaveis", 0)
    
    return render_template(
        'home.html', 
        imagens_por_classe=imagens_por_classe,
        bens=bens, 
        despesas_dedutiveis=despesas_dedutiveis, 
        gastos_tributaveis=gastos_tributaveis
    )








@app.route('/delete_file', methods=['POST'])
@login_required
def delete_file():
    data = request.get_json()
    file_id = data.get('file_id')

    if not file_id:
        return jsonify({"error": "ID do arquivo não fornecido"}), 400

    # Localiza e exclui a imagem
    nota = Notas.query.filter_by(id=file_id, usuario_id=current_user.id).first()
    if nota:
        try:
            db.session.delete(nota)
            db.session.commit()
            return jsonify({"message": "Arquivo excluído com sucesso!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Erro ao excluir o arquivo"}), 500
    else:
        return jsonify({"error": "Arquivo não encontrado"}), 404





@app.route("/notas", methods=['GET'])
@login_required
def notas():
    usuario_id = current_user.id
    codigo = gerar_string_com_id(usuario_id)
    # Consulta as notas do usuário
    notas = db.session.query(Notas, Classe.nome).join(Classe, Notas.classe_id == Classe.id).filter(
        Notas.usuario_id == usuario_id
    ).all()
    
    # Prepara os dados para o template
    arquivos = []
    categorias = set()
    
    for nota, categoria in notas:
        categorias.add(categoria)  # Adiciona a categoria
        if nota.binario:
            # Converte para Base64
            imagem_base64 = base64.b64encode(nota.binario).decode('utf-8')
            arquivos.append({
                'url': f"data:image/png;base64,{imagem_base64}",
                'nome': f"Arquivo {nota.id}",
                'categoria': categoria,
                'id': nota.id  # Adiciona o ID aqui
            })
    
    # Prepara a lista de categorias para filtros
    categorias = list(categorias)

    return render_template(
        'notas.html',
        codigo=codigo,
        arquivos=arquivos,
        categorias=categorias,
        categorias_dropdown=[{'value': cat, 'label': cat} for cat in categorias]  # Para o dropdown
    )

@app.route("/")
def index():
    return render_template('index.html')  

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    # Verifica se os campos obrigatórios foram enviados
    if 'arquivo' not in request.files or 'categoria' not in request.form:
        flash("Arquivo e categoria são obrigatórios.", "error")
        return redirect(request.url)

    arquivo = request.files['arquivo']
    categoria_nome = request.form['categoria']

    # Verifica se o arquivo tem um nome válido
    if arquivo.filename == '':
        flash("Nenhum arquivo selecionado.", "error")
        return redirect(request.url)

    # Lê o conteúdo do arquivo como binário
    binario = arquivo.read()

    # Verifica ou cria a categoria
    categoria = Classe.query.filter_by(nome=categoria_nome).first()
    if not categoria:
        categoria = Classe(nome=categoria_nome)
        db.session.add(categoria)
        db.session.commit()

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
            pass  # Pode adicionar ações ou logs específicos aqui se necessário

        flash("Arquivo enviado e armazenado com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
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

