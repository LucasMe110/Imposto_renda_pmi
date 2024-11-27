CREATE TABLE "Usuario" (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    CPF VARCHAR(15) UNIQUE NOT NULL, 
    Celular VARCHAR(15),
    Email VARCHAR(255) UNIQUE,
    Senha VARCHAR(255) NOT NULL,
    CEP VARCHAR(10),
    Data_nascimento DATE,
    Data_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Classe (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE Notas (
    ID SERIAL PRIMARY KEY,
    UsuarioID INT NOT NULL REFERENCES "Usuario"(ID) ON DELETE CASCADE,
    ClasseID INT NOT NULL REFERENCES Classe(ID) ON DELETE CASCADE,
    Binario BYTEA NOT NULL
);