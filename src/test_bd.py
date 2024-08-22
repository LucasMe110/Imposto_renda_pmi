from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_connection():
    try:
        # Configuração da conexão com o driver pyodbc para SQL Server
        DATABASE_URI = 'mssql+pyodbc://sa:Nicolas12345@localhost:1433/pmifinal?driver=ODBC+Driver+17+for+SQL+Server'
        engine = create_engine(DATABASE_URI)

        # Tentativa de conectar
        with engine.connect() as connection:
            print("Conexão bem-sucedida com o banco de dados SQL Server!")

            # Executando uma consulta SQL
            result = connection.execute(text("SELECT DB_NAME()"))
            db_name = result.scalar()
            print(f"Conectado ao banco de dados: {db_name}")

            # Executando outra consulta SQL
            result = connection.execute(text("SELECT GETDATE()"))
            current_time = result.scalar()
            print(f"Current time: {current_time}")

    except SQLAlchemyError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()
            print("Conexão ao banco de dados foi encerrada.")

if __name__ == "__main__":
    test_connection()
