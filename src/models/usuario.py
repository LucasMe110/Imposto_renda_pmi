from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(15), unique=True, nullable=False)  
    celular = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(10))
    data_nascimento = db.Column(db.Date)
    data_create = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)

class Classe(db.Model):
    __tablename__ = 'Classe'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

class Notas(db.Model):
    __tablename__ = 'Notas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id', ondelete='CASCADE'), nullable=False)
    classe_id = db.Column(db.Integer, db.ForeignKey('Classe.id', ondelete='CASCADE'), nullable=False)
    binario = db.Column(db.LargeBinary, nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('notas', cascade='all, delete'))
    classe = db.relationship('Classe', backref=db.backref('notas', cascade='all, delete'))
