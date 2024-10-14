import re
from flask import session, flash, request
from models.usuario import Usuario, db  # Importação do modelo e db
from services.cpf_validator import cpf_validador
from services.password_validator import validar_senha
from sqlalchemy.exc import IntegrityError
from services.idade import calcular_idade

def validar_formulario(nome_completo, data_nascimento, cpf, celular, email, confirmar_email, senha, confirmar_senha, cep):
    erros = {}

    # Validação de e-mail
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.(com|edu|gov|org)(\.br)?$', email):
        erros['email_erro'] = "E-mail inválido."

    # Verificar se os e-mails coincidem
    if email != confirmar_email:
        erros['confirmar_email_erro'] = "Os e-mails não coincidem."
    
    # Verificar se o e-mail já está registrado no banco de dados
    if Usuario.query.filter_by(email=email).first():
        erros['email_existente'] = "Esse e-mail já está cadastrado."
    
    # Validação do CPF usando o serviço
    if not cpf_validador(cpf):
        erros['cpf_invalido'] = "CPF inválido."
    
    # Verificar se o CPF já está registrado no banco de dados
    if Usuario.query.filter_by(cpf=cpf).first():
        erros['cpf_existente'] = "Esse CPF já está cadastrado."
    
    # Validação do CEP
    if not re.match(r'^\d{5}-?\d{3}$', cep):  # Verifica formato 12345-678 ou 12345678
        erros['cep_erro'] = "CEP inválido."

    # Verificar se o CEP já está registrado no banco de dados
    # Supondo que você tenha um campo de CEP no modelo Usuario
    if Usuario.query.filter_by(cep=cep).first():
        erros['cep_existente'] = "Esse CEP já está cadastrado."
    
    # Validação da senha
    if not validar_senha(senha):
        erros['senha_erro'] = "Senha não atende os critérios de segurança."

    # Verificar se as senhas coincidem
    if senha != confirmar_senha:
        erros['confirmar_senha_erro'] = "As senhas não coincidem."

    # Verificar a idade
    if not calcular_idade(data_nascimento):
        erros['idade_menor'] = "Menor de idade."

    return erros  # Retorna dicionário de erros

def salvar_dados_na_sessao(nome_completo, data_nascimento, cpf, celular, email, senha, cep):
    """Salva os dados temporariamente na sessão do Flask"""
    session['nome_completo'] = nome_completo
    session['data_nascimento'] = data_nascimento
    session['cpf'] = cpf
    session['celular'] = celular
    session['email'] = email
    session['senha'] = senha
    session['cep'] = cep  # Adiciona CEP à sessão

def salvar_usuario_no_bd():
    """Salva o usuário no banco de dados após validação e captura dos dados da sessão"""
    nome_completo = session.get('nome_completo')
    data_nascimento = session.get('data_nascimento')
    cpf = session.get('cpf')
    celular = session.get('celular')
    email = session.get('email')
    senha = session.get('senha')
    cep = session.get('cep')  # Obtém o CEP da sessão

    if not all([nome_completo, data_nascimento, cpf, celular, email, senha, cep]):
        flash("Erro ao salvar usuário: Dados incompletos.", 'error')
        return None

    usuario = Usuario(
        nome=nome_completo,
        data_nascimento=data_nascimento,
        cpf=cpf,
        celular=celular,
        email=email,
        senha=senha,
        cep=cep  # Adiciona CEP ao modelo do usuário
    )

    db.session.add(usuario)
    try:
        db.session.commit()  # Comita as mudanças no banco de dados
        flash("Usuário cadastrado com sucesso!", 'success')
        
        return usuario  # Retorna a instância do usuário
    except IntegrityError:
        db.session.rollback()  # Reverte em caso de erro de integridade
        flash("Erro ao cadastrar usuário. Tente novamente.", 'error')
        return None
