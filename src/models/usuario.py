from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    celular = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(8))
    data_nascimento = db.Column(db.Date)
    data_create = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
