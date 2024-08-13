#Mello 'mysql://root:12345@localhost:3306/Teste'
#Pedro 'mysql://root:12345pedro.@localhost:3306/meubancodedados'


#      'banco://root:senha@localhost:porta(padrao 3306)/banco que deseja usar'

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

#pip install pymysql


def test_connection():
    try:
        # Configuração da conexão com o driver pymysql
        DATABASE_URI = 'mysql+pymysql://root:12345@localhost:3306/Teste'
        engine = create_engine(DATABASE_URI)

        # Tentativa de conectar
        with engine.connect() as connection:
            print("Conexão bem-sucedida com o banco de dados MySQL!")
            result = connection.execute("SELECT DATABASE();")
            db_name = result.fetchone()
            print(f"Conectado ao banco de dados: {db_name[0]}")

    except SQLAlchemyError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()
            print("Conexão ao banco de dados foi encerrada.")

if __name__ == "__main__":
    test_connection()
