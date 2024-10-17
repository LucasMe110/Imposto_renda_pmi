# Contabilize Bem - PMI

## Link para visualização do site: [contabilizebem](https://contabilizebem.squareweb.app)

## Instalação
Execute os seguintes comandos para instalar as dependências necessárias:

```r 
- pip install -r requirements.txt
```
####  OU

```r 
- pip install Flask Flask-SQLAlchemy
```
```r
- pip install SQLAlchemy
```
```r 
- pip install numpy
```
```r 
- pip install cryptography
```

```r 
- pip install python-dotenv
```

```r 
-pip install flask-login
```

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
        5. idade: contem um calculo de idade.

5. templates 
    - Arquivos do frontend (HTML).

7. static
    - Arquivos CSS e JavaScript(Voltado ao Front)

6. sql
    - Scripts SQL.