from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = 'sua_chave_secreta'

## Strings de Conexão
#- Mello = 'mysql+pymysql://root:12345@localhost:3306/Teste'
#- Nicolas = 'mssql+pyodbc://sa:Nicolas12345@localhost:1433/pmifinal?driver=ODBC+Driver+17+for+SQL+Server'
#- Eduardo = 'mysql+pymysql://root:eduardo12345.@localhost:3306/pmi'
#- Pedro = 'mysql+pymysql://root:12345.@localhost:3306/meubancodedados'