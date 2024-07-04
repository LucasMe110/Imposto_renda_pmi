from asyncio import run
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine('mysql+aiomysql://root:1234.@localhost:3306/Teste', 
                             echo=True)

async def view():
    try:
        async with engine.connect() as con:
            sql = text('select * from Usuario')
            result = await con.execute(sql)

            for row in result:
                print(row)

    except Exception as e:
        print(f"An error occurred: {e}")

async def add_user(new_user):
    """Inserts a new user into the 'Usuario' table.

    Args:
        new_user (dict): A dictionary containing user information (e.g., {'nome': 'John Doe', 'email': 'john.doe@example.com'}).
    """

    try:
        async with engine.connect() as con:
            # Prepare the INSERT statement with placeholders
            sql = text("INSERT INTO Usuario (nome, senha, celular, email, cpf) "
                       "VALUES (:nome, :senha, :celular, :email, :cpf)")

            # Create a dictionary with user data for insertion
            user_data = {
                "nome": new_user["nome"],
                "senha": new_user["senha"],  # Replace with secure password hashing
                "celular": new_user.get("celular", None),  # Optional field
                "email": new_user["email"],
                "cpf": new_user["cpf"]
            }

            # Execute the INSERT statement with user data
            await con.execute(sql, user_data)
            await con.commit()  # Commit the transaction

            print(f"User '{new_user['nome']}' added successfully!")

    except Exception as e:
        await con.rollback()  # Rollback in case of errors
        print(f"An error occurred: {e}")

async def delete_user(user_id):
    """Deletes a user from the 'Usuario' table.

    Args:
        user_id (int): The ID of the user to delete.
    """

    try:
        async with engine.connect() as con:
            # Delete related documents (assuming 'documento_id' is the primary key in documentos table)
            sql = text("DELETE FROM documentos WHERE id_usuario = :user_id")
            user_data = {"user_id": user_id}
            await con.execute(sql, user_data)

            # Delete the user
            sql = text("DELETE FROM Usuario WHERE id_usuario = :user_id")
            await con.execute(sql, user_data)
            await con.commit()

            print(f"User with ID {user_id} deleted successfully!")

    except Exception as e:
        await con.rollback()
        print(f"An error occurred: {e}")

async def update_user(user_id, updated_data):
    """Updates a user's information in the 'Usuario' table.

    Args:
        user_id (int): The ID of the user to update.
        updated_data (dict): A dictionary containing updated user information (e.g., {'nome': 'New Name'}).
    """

    try:
        async with engine.connect() as con:
            # Prepare the UPDATE statement with placeholders
            sql = text("UPDATE Usuario SET "
                       "nome = :nome, senha = :senha, celular = :celular, email = :email, cpf = :cpf "
                       "WHERE id_usuario = :user_id")

            # Combine updated data with user ID for the query
            update_data = dict(updated_data)
            update_data["user_id"] = user_id

            # Execute the UPDATE statement with user data
            await con.execute(sql, update_data)
            await con.commit()  # Commit the transaction

            print(f"User with ID {user_id} updated successfully!")

    except Exception as e:
        await con.rollback()  # Rollback in case of errors
        print(f"An error occurred: {e}")

# Example usage
new_user = {
    "nome": "Lucas Mello",
    "senha": "Albinismo123",  # Replace with a secure hashed password
    "email": "Lucas.Branquelo333@gmail.com",
    "cpf": "32165498799"
}

user_id_to_delete = 1  # Replace with the actual user ID to delete
run(delete_user(user_id_to_delete))

user_id_to_update = 2  # Replace with the actual user ID to update
updated_data = {"nome": "Pedrin Kwai", "email": "pedrinkwai@novoemail.com"}
run(update_user(user_id_to_update, updated_data))