import re
from flask import session, flash
from models.usuario import Usuario, db  # Importe o db junto com o modelo
from services.cpf_validator import cpf_validador
from services.password_validator import validar_senha
from sqlalchemy.exc import IntegrityError

def validar_formulario(nome, senha, celular, email, cpf):
    erros = {}

    # Validação de e-mail
    if not re.match(r'.*@.*\.(com|edu|gov|org)(\.br)?$', email):
        erros['email_erro'] = "E-mail inválido"
    
    # Validação do CPF
    if not cpf_validador(cpf):
        erros['cpf_invalido'] = "CPF inválido"
    
    # Verificar se o CPF já está registrado
    if Usuario.query.filter_by(cpf=cpf).first():
        erros['cpf_existente'] = "Esse CPF já foi usado"
    
    # Validação da senha
    if not validar_senha(senha):
        erros['senha_erro'] = "Senha não atende os critérios de segurança"

    return erros

def salvar_dados_na_sessao(nome, senha, celular, email, cpf):
    session['nome'] = nome
    session['senha'] = senha
    session['celular'] = celular
    session['email'] = email
    session['cpf'] = cpf

def salvar_usuario_no_bd():
    nome = session.get('nome')
    senha = session.get('senha')
    celular = session.get('celular')
    email = session.get('email')
    cpf = session.get('cpf')

    usuario = Usuario(
        nome=nome,
        senha=senha,
        celular=celular,
        email=email,
        cpf=cpf
    )

    db.session.add(usuario)
    try:
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash("Erro ao cadastrar usuário.", 'error')
        return False
