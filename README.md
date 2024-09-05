# Contabilize Bem - PMI

## Instalação
Execute os seguintes comandos para instalar as dependências necessárias:
- pip install Flask Flask-SQLAlchemy
- pip install SQLAlchemy
- pip install numpy
- pip install cryptography

## Iniciar

- Antes de iniciar o projeto, você deve ajustar a string de conexão do banco de dados no arquivo config/config.py para a sua configuração.

## Estrutura de Pastas
1. config
    - Contém as configurações do banco de dados e a secret key.

2. forms 
    - Gerencia os formulários HTML
        1. Adiciona usuários ao banco de dados.

3. models
    - Define a estrutura do banco de dados.

4. services
    - Funções úteis para o projeto.
        1. cpf_validator: Verifica se o CPF é válido.
        2. email_service: Cria o corpo do e-mail.
        3. password_validator: Verifica se a senha segue as diretrizes de segurança.
        4. send_verification_email: Envia o e-mail de verificação.

5. templates 
    - Arquivos do frontend (HTML).

6. sql
    - Scripts SQL.

