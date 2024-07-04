import re
import random
import asyncio
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from send_verification_email import send_verification_email
from cpf_validator import cpf_validador  

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/Teste'
app.secret_key = 'sua_chave_secreta'  

db = SQLAlchemy(app)

class Usuario(db.Model):
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    senha = db.Column(db.String(150))
    celular = db.Column(db.VARCHAR(17))
    email = db.Column(db.String(150))
    cpf = db.Column(db.String(150), unique=True)

@app.route('/', methods=['POST'])
def index():
    return "index"

@app.route('/addimg')
def addimg():
    return "Oi, imagem adicionada!"








if __name__ == '__main__':
    app.run(debug=True)
