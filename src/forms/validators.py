import re
from flask import session, flash, request
from models.usuario import Usuario, db  # Importação do modelo e db
from services.cpf_validator import cpf_validador
from services.password_validator import validar_senha
from sqlalchemy.exc import IntegrityError
from services.idade import calcular_idade

def validar_formulario(nome_completo, data_nascimento, cpf, celular, email, confirmar_email, senha, confirmar_senha):
    erros = {}

    # Validação de e-mail
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.(com|edu|gov|org)(\.br)?$', email):
        erros['email_erro'] = "E-mail inválido."

    # Verificar se os e-mails coincidem
    if email != confirmar_email:
        erros['confirmar_email_erro'] = "Os e-mails não coincidem."
    
    # Validação do CPF usando o serviço
    if not cpf_validador(cpf):
        erros['cpf_invalido'] = "CPF inválido."
    
    # Verificar se o CPF já está registrado no banco de dados
    if Usuario.query.filter_by(cpf=cpf).first():
        erros['cpf_existente'] = "Esse CPF já está cadastrado."
    
    # Validação da senha
    if not validar_senha(senha):
        erros['senha_erro'] = "Senha não atende os critérios de segurança."

    # Verificar se as senhas coincidem
    if senha != confirmar_senha:
        erros['confirmar_senha_erro'] = "As senhas não coincidem."

    if not calcular_idade(data_nascimento):
        erros['idade_menor'] = "Menor de idade."

    return erros  # Retorna dicionário de erros

def salvar_dados_na_sessao(nome_completo, data_nascimento, cpf, celular, email, senha):
    """Salva os dados temporariamente na sessão do Flask"""
    session['nome_completo'] = nome_completo
    session['data_nascimento'] = data_nascimento
    session['cpf'] = cpf
    session['celular'] = celular
    session['email'] = email
    session['senha'] = senha

def salvar_usuario_no_bd():
    """Salva o usuário no banco de dados após validação e captura dos dados da sessão"""
    nome_completo = session.get('nome_completo')
    data_nascimento = session.get('data_nascimento')
    cpf = session.get('cpf')
    celular = session.get('celular')
    email = session.get('email')
    senha = session.get('senha')

    if not all([nome_completo, data_nascimento, cpf, celular, email, senha]):
        flash("Erro ao salvar usuário: Dados incompletos.", 'error')
        return False

    usuario = Usuario(
        nome=nome_completo,
        data_nascimento=data_nascimento,
        cpf=cpf,
        celular=celular,
        email=email,
        senha=senha
    )

    db.session.add(usuario)
    try:
        db.session.commit()  # Comita as mudanças no banco de dados
        flash("Usuário cadastrado com sucesso!", 'success')
        return True
    except IntegrityError:
        db.session.rollback()  # Reverte em caso de erro de integridade
        flash("Erro ao cadastrar usuário. Tente novamente.", 'error')
        return False
