from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/bin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Modelo da Tabela
class ImagemBinaria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    binario = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)  # LONGBLOB para grandes arquivos binários

# Rota para a página inicial (formulário de upload)
@app.route('/')
def index():
    return render_template('enviar.html')

# Rota para processar o upload da imagem e armazenar no banco de dados
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'nome' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    nome = request.form['nome']

    if file.filename == '':
        return redirect(request.url)

    # Armazena a imagem em binário
    binario = file.read()

    # Cria uma nova instância do modelo com o nome e a imagem em binário
    imagem = ImagemBinaria(nome=nome, binario=binario)
    
    # Insere no banco de dados
    db.session.add(imagem)
    db.session.commit()

    # Imprime no terminal o conteúdo em binário (opcional)
    print(f"Nome: {nome}")
    print(f"Binário: {binario[:60]}...")  # Imprime os primeiros 60 bytes para evitar sobrecarga no terminal

    return "Upload e armazenamento concluídos!"

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
