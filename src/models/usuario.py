from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    celular = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(8))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.Integer)
    complemento = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    data_nascimento = db.Column(db.Date)
    data_create = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
