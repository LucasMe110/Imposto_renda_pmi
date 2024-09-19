from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/bin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ImagemBinaria(db.Model):
    __tablename__ = 'imagem_binaria'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    binario = db.Column(db.LargeBinary, nullable=False)

@app.route('/')
def index():
    imagens = ImagemBinaria.query.all()
    return render_template('aparecer.html', imagens=imagens)

@app.route('/imagem/<int:id>')
def imagem(id):
    imagem = ImagemBinaria.query.get_or_404(id)
    return send_file(
        io.BytesIO(imagem.binario),
        mimetype='image/jpeg',  # Altere o mimetype se necessário
        as_attachment=False,
        # Substitua `filename` por `attachment_filename` se estiver usando uma versão mais recente do Flask
        # filename=imagem.nome  
    )

if __name__ == '__main__':
    app.run(debug=True)
