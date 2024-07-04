# mysql://root:12345@localhost:3306/Teste
# mysql+aiomysql://root:12345pedro.@localhost:3306/meubancodedados
from datetime import datetime

from sqlalchemy import (
    MetaData,
    Table,
    create_engine,
    delete,
    insert,
    select,
    update,
)

metadata = MetaData()
engine = create_engine(
    'mysql://root:12345@localhost:3306/pmi'
)

#definindo a tabela 
tabela_usuario = Table('usuario', metadata, autoload_with=engine)


#Insert usario  
criar_usuario = (
    insert(tabela_usuario).values(
        name='Ana'
        cpf='127.950.499-45'
        #...
    )
)


#update usuario
update_telefone = (
        update(tabela_usuario)
        .where(
            tabela_usuario.c.id == '2',
            tabela_usuario.c.nome == 'cpf',
            tabela_usuario.c.senha == 'senha',
        )
        .values(telefone='48988027807')
)

#deletar conta
deletar_conta = delete(tabela_usuario).where(
        tabela_usuario.c.name == 'joao...',
        tabela_usuario.c.id == '2',
        tabela_usuario.c.senha == 'senha',
        tabela_usuario.c.cpf == '12795049945',
)

#select no email do usuario
email_usuario = select(tabela_usuario).where(
        tabela_usuario.c.name == 'joao...',
        tabela_usuario.c.id == '2',
        tabela_usuario.c.senha == 'senha',
)
results = con.execute(email_usuario)
print(results.email())
#print(results.all())

#https://github.com/dunossauro/live-de-python/blob/main/codigo/Live258/slide_codes/exemplo_12.py


# mysql://root:12345@localhost:3306/pmi