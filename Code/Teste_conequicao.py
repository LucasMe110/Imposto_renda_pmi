from sqlalchemy import create_engine, text

engine = create_engine(
    'mysql://root:12345@localhost:3306/Teste',
    echo=True,
)

with engine.connect() as con:
    sql = text('select * from Usuario')
    result = con.execute(sql)

primeito_valor = result.fetchone()
todos_os_valores = result.fetchall()

print(primeito_valor)
print(todos_os_valores)