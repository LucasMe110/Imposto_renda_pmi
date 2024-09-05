from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    senha = db.Column(db.String(150))
    celular = db.Column(db.VARCHAR(17))
    email = db.Column(db.String(150))
    cpf = db.Column(db.String(150), unique=True)
