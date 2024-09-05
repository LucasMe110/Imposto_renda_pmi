# Contabilize Bem - PMI

## Install

- pip install Flask Flask-SQLAlchemy
- pip install SQLAlchemy
- pip install numpy
- pip install cryptography

## Iniciar

- Mudar o string de banco de dados para a sua propria, essa fica loalizado na pasta config/config.py

## Folder
1. config
    - Configuração com o banco de dados, e secret key 

2. forms 
    - Gerenciador de formularios html.
        - add usuario nobanco

3. models
    - Estrutura bd

4. services
    - Funções
        1. cpf_validator: verifica se o cpf é valido.
        2. email_service: faz o corpo do email.
        3. password_validator: verifica se a senha condiz com as diretrizes de segurança.
        4. send_verification_email: envia o email.

5. templates 
    - front
